"""
services.py — NBA API abstraction layer.
All nba_api calls are centralized here with error handling and timeouts.
"""
import logging
from datetime import datetime

from nba_api.stats.static import players as static_players
from nba_api.stats.static import teams as static_teams
from nba_api.stats.endpoints import (
    commonplayerinfo,
    playercareerstats,
    playergamelog,
    commonteamroster,
    teamdetails,
    leaguegamefinder,
    leaguestandingsv3,
    teamyearbyyearstats,
    boxscoresummaryv2,
    boxscoretraditionalv2,
)

from .models import CachedPlayer, CachedTeam

logger = logging.getLogger(__name__)

# Timeout for all NBA API requests (seconds)
API_TIMEOUT = 15


def get_current_season():
    """Auto-detect the current NBA season string (e.g. '2024-25')."""
    now = datetime.now()
    if now.month >= 10:
        start_year = now.year
    else:
        start_year = now.year - 1
    end_year_short = str(start_year + 1)[-2:]
    return f"{start_year}-{end_year_short}"


# ─── Search (local DB) ───────────────────────────────────────────────

def search_players(query):
    """Search cached players by name."""
    return CachedPlayer.search(query)


def search_teams(query):
    """Search cached teams by name, city, or abbreviation."""
    return CachedTeam.search(query)


# ─── Player endpoints ────────────────────────────────────────────────

def get_player_info(player_id):
    """Fetch player biographical info from CommonPlayerInfo endpoint."""
    try:
        info = commonplayerinfo.CommonPlayerInfo(
            player_id=player_id,
            timeout=API_TIMEOUT,
        )
        data = info.common_player_info.get_data_frame()
        if data.empty:
            return None
        row = data.iloc[0].to_dict()

        # Enrich with headshot URL
        row['HEADSHOT_URL'] = get_player_headshot_url(player_id)

        return row
    except Exception as e:
        logger.error(f"Error fetching player info for {player_id}: {e}")
        return None


def get_player_career_stats(player_id):
    """Fetch career stats (season-by-season + career totals)."""
    try:
        career = playercareerstats.PlayerCareerStats(
            player_id=player_id,
            per_mode36='PerGame',
            timeout=API_TIMEOUT,
        )
        season_totals = career.season_totals_regular_season.get_data_frame()
        career_totals = career.career_totals_regular_season.get_data_frame()

        return {
            'seasons': season_totals.to_dict('records') if not season_totals.empty else [],
            'career': career_totals.iloc[0].to_dict() if not career_totals.empty else None,
        }
    except Exception as e:
        logger.error(f"Error fetching career stats for {player_id}: {e}")
        return {'seasons': [], 'career': None}


def get_player_game_log(player_id, season=None, last_n=10):
    """Fetch recent games for a player (including playoffs)."""
    if season is None:
        season = get_current_season()
    try:
        finder = leaguegamefinder.LeagueGameFinder(
            player_id_nullable=player_id,
            season_nullable=season,
            timeout=API_TIMEOUT,
        )
        df = finder.league_game_finder_results.get_data_frame()
        if df.empty:
            return []
        # Filter out preseason games (SEASON_ID starts with '1')
        df = df[~df['SEASON_ID'].str.startswith('1')]
        return df.head(last_n).to_dict('records')
    except Exception as e:
        logger.error(f"Error fetching game log for {player_id}: {e}")
        return []


# ─── Team endpoints ──────────────────────────────────────────────────

def get_team_info(team_id):
    """Fetch team background info from TeamDetails endpoint."""
    try:
        details = teamdetails.TeamDetails(
            team_id=team_id,
            timeout=API_TIMEOUT,
        )
        bg = details.team_background.get_data_frame()
        if bg.empty:
            return None
        row = bg.iloc[0].to_dict()
        row['LOGO_URL'] = get_team_logo_url(team_id)
        return row
    except Exception as e:
        logger.error(f"Error fetching team info for {team_id}: {e}")
        return None


def get_team_roster(team_id, season=None):
    """Fetch current team roster."""
    if season is None:
        season = get_current_season()
    try:
        roster = commonteamroster.CommonTeamRoster(
            team_id=team_id,
            season=season,
            timeout=API_TIMEOUT,
        )
        df = roster.common_team_roster.get_data_frame()
        if df.empty:
            return []
        records = df.to_dict('records')
        # Add headshot URLs
        for player in records:
            pid = player.get('PLAYER_ID')
            if pid:
                player['HEADSHOT_URL'] = get_player_headshot_url(pid)
        return records
    except Exception as e:
        logger.error(f"Error fetching roster for team {team_id}: {e}")
        return []


def get_team_season_record(team_id, season=None):
    """Fetch team W-L record using LeagueGameFinder."""
    if season is None:
        season = get_current_season()
    try:
        finder = leaguegamefinder.LeagueGameFinder(
            team_id_nullable=team_id,
            season_nullable=season,
            timeout=API_TIMEOUT,
        )
        df = finder.league_game_finder_results.get_data_frame()
        if df.empty:
            return {'wins': 0, 'losses': 0, 'games': [], 'win_pct': 0}

        # Calculate W-L record based ONLY on Regular Season games
        rs_df = df[df['SEASON_ID'].str.startswith('2')]
        wins = len(rs_df[rs_df['WL'] == 'W'])
        losses = len(rs_df[rs_df['WL'] == 'L'])
        total = wins + losses
        win_pct = round(wins / total, 3) if total > 0 else 0

        # Recent games should exclude preseason (starting with '1') but include playoffs
        games_df = df[~df['SEASON_ID'].str.startswith('1')].copy()
        if 'PTS' in games_df.columns and 'PLUS_MINUS' in games_df.columns:
            games_df['PLUS_MINUS'] = games_df['PLUS_MINUS'].fillna(0)
            games_df['PTS'] = games_df['PTS'].fillna(0)
            games_df['OPP_PTS'] = (games_df['PTS'] - games_df['PLUS_MINUS']).astype(int)
        recent_games = games_df.head(10).to_dict('records')

        return {
            'wins': wins,
            'losses': losses,
            'win_pct': win_pct,
            'games': recent_games,
        }
    except Exception as e:
        logger.error(f"Error fetching season record for team {team_id}: {e}")
        return {'wins': 0, 'losses': 0, 'games': [], 'win_pct': 0}


def get_team_history(team_id):
    """Fetch year-by-year history for a team."""
    try:
        history = teamyearbyyearstats.TeamYearByYearStats(
            team_id=team_id,
            timeout=API_TIMEOUT,
        )
        df = history.team_stats.get_data_frame()
        if df.empty:
            return []
        # Return descending so newest season is first
        return df.sort_values(by='YEAR', ascending=False).to_dict('records')
    except Exception as e:
        logger.error(f"Error fetching team history for {team_id}: {e}")
        return []


def get_team_season_games(team_id, season):
    """Fetch ALL games for a team in a specific season (Playoffs included)."""
    try:
        finder = leaguegamefinder.LeagueGameFinder(
            team_id_nullable=team_id,
            season_nullable=season,
            timeout=API_TIMEOUT,
        )
        df = finder.league_game_finder_results.get_data_frame()
        if df.empty:
            return []
        # Exclude preseason (SEASON_ID starting with '1')
        df = df[~df['SEASON_ID'].str.startswith('1')].copy()
        
        # Calculate opponent points if PTS and PLUS_MINUS are available
        if 'PTS' in df.columns and 'PLUS_MINUS' in df.columns:
            # Drop rows with missing PTS or PLUS_MINUS to avoid errors, or fill them
            df['PLUS_MINUS'] = df['PLUS_MINUS'].fillna(0)
            df['PTS'] = df['PTS'].fillna(0)
            df['OPP_PTS'] = (df['PTS'] - df['PLUS_MINUS']).astype(int)
        else:
            df['OPP_PTS'] = 0

        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Error fetching team games for {team_id} season {season}: {e}")
        return []


# ─── Static URL builders ─────────────────────────────────────────────

def get_player_headshot_url(player_id):
    """NBA CDN headshot URL pattern."""
    return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"


def get_team_logo_url(team_id):
    """NBA CDN team logo URL pattern."""
    return f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"


# ─── Cache population ────────────────────────────────────────────────

def populate_player_cache():
    """Populate the CachedPlayer table from nba_api static data."""
    all_players = static_players.get_players()
    count = 0
    for p in all_players:
        _, created = CachedPlayer.objects.update_or_create(
            nba_id=p['id'],
            defaults={
                'first_name': p.get('first_name', ''),
                'last_name': p.get('last_name', ''),
                'full_name': p.get('full_name', ''),
                'is_active': p.get('is_active', False),
            }
        )
        count += 1
    return count


def populate_team_cache():
    """Populate the CachedTeam table from nba_api static data."""
    all_teams = static_teams.get_teams()
    count = 0
    for t in all_teams:
        _, created = CachedTeam.objects.update_or_create(
            nba_id=t['id'],
            defaults={
                'full_name': t.get('full_name', ''),
                'abbreviation': t.get('abbreviation', ''),
                'nickname': t.get('nickname', ''),
                'city': t.get('city', ''),
                'state': t.get('state', ''),
                'year_founded': t.get('year_founded'),
            }
        )
        count += 1
    return count


# ─── Game detail ──────────────────────────────────────────────────────

def get_game_boxscore(game_id):
    try:
        from nba_api.stats.endpoints import boxscoresummaryv3, boxscoretraditionalv3, boxscoremiscv3

        s = boxscoresummaryv3.BoxScoreSummaryV3(game_id=game_id, timeout=API_TIMEOUT).get_dict()['boxScoreSummary']
        t = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id, timeout=API_TIMEOUT).get_dict()['boxScoreTraditional']
        m = boxscoremiscv3.BoxScoreMiscV3(game_id=game_id, timeout=API_TIMEOUT).get_dict()['boxScoreMisc']
        
        home_team_id = s['homeTeamId']
        visitor_team_id = s['awayTeamId']
        
        game_info = {
            'game_date': s.get('gameEt', '').split('T')[0],
            'game_status': s.get('gameStatusText', ''),
            'home_team_id': home_team_id,
            'visitor_team_id': visitor_team_id,
        }
        
        def map_line(team_summary):
            periods = team_summary.get('periods', [])
            q1 = periods[0]['score'] if len(periods) > 0 else 0
            q2 = periods[1]['score'] if len(periods) > 1 else 0
            q3 = periods[2]['score'] if len(periods) > 2 else 0
            q4 = periods[3]['score'] if len(periods) > 3 else 0
            return {
                'TEAM_ID': team_summary.get('teamId'),
                'TEAM_ABBREVIATION': team_summary.get('teamTricode'),
                'TEAM_CITY_NAME': team_summary.get('teamCity'),
                'TEAM_NICKNAME': team_summary.get('teamName'),
                'TEAM_WINS_LOSSES': f"{team_summary.get('teamWins', 0)}-{team_summary.get('teamLosses', 0)}",
                'PTS': team_summary.get('score'),
                'PTS_QTR1': q1,
                'PTS_QTR2': q2,
                'PTS_QTR3': q3,
                'PTS_QTR4': q4,
            }
        
        home_line = map_line(s['homeTeam'])
        visitor_line = map_line(s['awayTeam'])
        
        def map_players(team_trad):
            players = []
            for p in team_trad.get('players', []):
                st = p.get('statistics', {})
                players.append({
                    'TEAM_ID': team_trad.get('teamId'),
                    'PLAYER_NAME': f"{p.get('firstName', '')} {p.get('familyName', '')}".strip() or p.get('nameI', ''),
                    'START_POSITION': p.get('position', ''),
                    'COMMENT': p.get('comment', ''),
                    'MIN': st.get('minutes', '0:00').split('.')[0] if st.get('minutes') else None,
                    'PTS': st.get('points'),
                    'REB': st.get('reboundsTotal'),
                    'AST': st.get('assists'),
                    'STL': st.get('steals'),
                    'BLK': st.get('blocks'),
                    'FGM': st.get('fieldGoalsMade'),
                    'FGA': st.get('fieldGoalsAttempted'),
                    'FG3M': st.get('threePointersMade'),
                    'FG3A': st.get('threePointersAttempted'),
                    'FTM': st.get('freeThrowsMade'),
                    'FTA': st.get('freeThrowsAttempted'),
                    'PLUS_MINUS': st.get('plusMinusPoints'),
                })
            return players
            
        home_players = map_players(t['homeTeam'])
        visitor_players = map_players(t['awayTeam'])
        
        def map_totals(team_trad):
            st = team_trad.get('statistics', {})
            return {
                'TEAM_ID': team_trad.get('teamId'),
                'MIN': st.get('minutes', '0:00').split('.')[0] if st.get('minutes') else '0:00',
                'PTS': st.get('points'),
                'REB': st.get('reboundsTotal'),
                'AST': st.get('assists'),
                'STL': st.get('steals'),
                'BLK': st.get('blocks'),
                'FGM': st.get('fieldGoalsMade'),
                'FGA': st.get('fieldGoalsAttempted'),
                'FG3M': st.get('threePointersMade'),
                'FG3A': st.get('threePointersAttempted'),
                'FTM': st.get('freeThrowsMade'),
                'FTA': st.get('freeThrowsAttempted'),
                'PLUS_MINUS': st.get('plusMinusPoints'),
            }
            
        home_team_totals = map_totals(t['homeTeam'])
        visitor_team_totals = map_totals(t['awayTeam'])
        
        def map_other(team_misc, team_trad):
            mst = team_misc.get('statistics', {})
            tst = team_trad.get('statistics', {})
            is_home = team_misc.get('teamId') == home_team_id
            
            # Try to get biggestLead from postgameCharts (v3 location)
            pgc = s.get('postgameCharts', {})
            team_pgc = pgc.get('homeTeam' if is_home else 'awayTeam', {})
            biggest_lead = team_pgc.get('statistics', {}).get('biggestLead', 0)
            
            return {
                'TEAM_ID': team_misc.get('teamId'),
                'TEAM_CITY': team_misc.get('teamCity'),
                'TEAM_ABBREVIATION': team_misc.get('teamTricode'),
                'PTS_PAINT': mst.get('pointsPaint'),
                'PTS_2ND_CHANCE': mst.get('pointsSecondChance'),
                'PTS_FB': mst.get('pointsFastBreak'),
                'PTS_OFF_TO': mst.get('pointsOffTurnovers'),
                'LARGEST_LEAD': biggest_lead,
                'TEAM_TURNOVERS': tst.get('turnovers'),
            }
            
        home_other = map_other(m['homeTeam'], t['homeTeam'])
        visitor_other = map_other(m['awayTeam'], t['awayTeam'])
        
        officials_data = []
        for off in s.get('officials', []):
            officials_data.append({
                'FIRST_NAME': off.get('firstName', ''),
                'LAST_NAME': off.get('familyName', ''),
            })
            
        return {
            'game_info': game_info,
            'home_line': home_line,
            'visitor_line': visitor_line,
            'home_players': home_players,
            'visitor_players': visitor_players,
            'home_team_totals': home_team_totals,
            'visitor_team_totals': visitor_team_totals,
            'home_other': home_other,
            'visitor_other': visitor_other,
            'officials': officials_data,
        }
    except Exception as e:
        logger.error(f"Error fetching boxscore for game {game_id}: {e}")
        return None

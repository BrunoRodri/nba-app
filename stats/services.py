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
        games_df = df[~df['SEASON_ID'].str.startswith('1')]
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
        df = df[~df['SEASON_ID'].str.startswith('1')]
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

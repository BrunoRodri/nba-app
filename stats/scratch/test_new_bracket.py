from nba_api.stats.endpoints import leaguegamefinder, commonplayoffseries
import collections

def build_bracket():
    season = "2025-26"
    print("Fetching CommonPlayoffSeries...")
    try:
        ps = commonplayoffseries.CommonPlayoffSeries(league_id='00', season=season)
        series_data = ps.get_dict()['resultSets'][0]
        rows = [dict(zip(series_data['headers'], row)) for row in series_data['rowSet']]
        
        series_info = {}
        for r in rows:
            sid = r['SERIES_ID']
            if sid not in series_info:
                series_info[sid] = {
                    'HOME_TEAM_ID': r['HOME_TEAM_ID'],
                    'VISITOR_TEAM_ID': r['VISITOR_TEAM_ID'],
                    'HOME_WINS': 0,
                    'VISITOR_WINS': 0
                }

        print("Fetching LeagueGameFinder...")
        gf = leaguegamefinder.LeagueGameFinder(season_nullable=season, season_type_nullable='Playoffs')
        games = gf.get_data_frames()[0]
        
        # Count wins
        # A game has two rows, one for each team. If WL == 'W', that team won.
        if not games.empty:
            winners = games[games['WL'] == 'W']
            for _, row in winners.iterrows():
                gid = str(row['GAME_ID'])
                sid = gid[:9] # e.g. 004250010
                team_id = row['TEAM_ID']
                if sid in series_info:
                    if series_info[sid]['HOME_TEAM_ID'] == team_id:
                        series_info[sid]['HOME_WINS'] += 1
                    elif series_info[sid]['VISITOR_TEAM_ID'] == team_id:
                        series_info[sid]['VISITOR_WINS'] += 1

        print("--- BRACKET ---")
        for sid, info in series_info.items():
            print(f"Series {sid}: Team {info['HOME_TEAM_ID']} ({info['HOME_WINS']}) vs Team {info['VISITOR_TEAM_ID']} ({info['VISITOR_WINS']})")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    build_bracket()

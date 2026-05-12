from nba_api.stats.endpoints import commonplayoffseries

def test_playoff_bracket():
    season = "2023-24" # Previous season as sample
    print(f"Testing for season: {season}")
    try:
        series = commonplayoffseries.CommonPlayoffSeries(
            season=season,
            league_id='00'
        )
        df = series.get_data_frames()[0]
        if df.empty:
            print("No playoff series found.")
            return

        print("Columns:", df.columns.tolist())
        print("Data sample (first 5 series):")
        # Standard columns in CommonPlayoffSeries:
        # GAME_ID, HOME_TEAM_ID, VISITOR_TEAM_ID, SERIES_ID, GAME_NUM, etc.
        # But actually it returns summary of series.
        
        # In fact, CommonPlayoffSeries returns a list of series with their status.
        print(df[['SERIES_ID', 'TEAM_ID', 'OPPONENT_ID', 'SERIES_LEADER']].head(10))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_playoff_bracket()

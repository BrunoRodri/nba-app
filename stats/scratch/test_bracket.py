import os
import django
import sys

# Setup django environment
sys.path.append('/home/bruno/pessoal/nba/nba-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nba_explorer.settings')
django.setup()

from nba_api.stats.endpoints import commonplayoffseries
from stats import services

def test_playoff_bracket():
    season = services.get_current_season()
    print(f"Testing for season: {season}")
    try:
        series = commonplayoffseries.CommonPlayoffSeries(
            season=season,
            league_id='00'
        )
        df = series.get_data_frames()[0]
        if df.empty:
            print("No playoff series found for current season. (Expected if in regular season)")
            # Try previous season to see data structure
            prev_season = "2023-24"
            print(f"Testing for previous season: {prev_season}")
            series = commonplayoffseries.CommonPlayoffSeries(
                season=prev_season,
                league_id='00'
            )
            df = series.get_data_frames()[0]
            
        print("Columns:", df.columns.tolist())
        print("Data sample:")
        print(df.head(10))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_playoff_bracket()

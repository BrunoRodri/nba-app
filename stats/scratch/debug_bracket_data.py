from nba_api.stats.endpoints import playoffpicture
import json

def debug_playoff_data():
    try:
        pp = playoffpicture.PlayoffPicture(league_id='00')
        data = pp.get_dict()['resultSets']
        
        east = [dict(zip(data[0]['headers'], row)) for row in data[0]['rowSet']]
        west = [dict(zip(data[1]['headers'], row)) for row in data[1]['rowSet']]
        
        print("--- EAST RAW DATA ---")
        for m in east:
            print(f"{m['HIGH_SEED_RANK']} {m['HIGH_SEED_TEAM']} vs {m['LOW_SEED_RANK']} {m['LOW_SEED_TEAM']} | Series: {m.get('HIGH_SEED_SERIES_W')}-{m.get('HIGH_SEED_SERIES_L')}")
            
        print("\n--- WEST RAW DATA ---")
        for m in west:
            print(f"{m['HIGH_SEED_RANK']} {m['HIGH_SEED_TEAM']} vs {m['LOW_SEED_RANK']} {m['LOW_SEED_TEAM']} | Series: {m.get('HIGH_SEED_SERIES_W')}-{m.get('HIGH_SEED_SERIES_L')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_playoff_data()

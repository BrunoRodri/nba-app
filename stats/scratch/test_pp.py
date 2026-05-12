from nba_api.stats.endpoints import playoffpicture

def test_playoff_picture():
    season = "2023-24" # Previous season
    print(f"Testing PlayoffPicture for season: {season}")
    try:
        pp = playoffpicture.PlayoffPicture(
            league_id='00'
        )
        # PlayoffPicture doesn't take a season parameter usually? 
        # Actually it takes SeasonID
        
        # Let's try to list all result sets
        results = pp.get_dict()['resultSets']
        for i, rs in enumerate(results):
            print(f"Set {i}: {rs['name']}")
            print(f"Headers: {rs['headers']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_playoff_picture()

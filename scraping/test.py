from src.get_tt_races import process_race_sync
import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="make a test call")
    parser.add_argument("url", type=str, help="URL of the race to process")
    args = parser.parse_args()
    url = args.url
    result = process_race_sync(url, verbose=True)
    
    print(json.dumps(result, indent=4))
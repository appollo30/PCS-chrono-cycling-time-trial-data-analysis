import asyncio
import aiohttp
from get_tt_specialists import get_all_tt_specialists, process_rider
from get_tt_results import process_results
from get_tt_races import process_race
import pandas as pd
from typing import List, Dict, Set, Tuple

async def main():
    all_riders = get_all_tt_specialists()
    
    riders_data = []
    results_data = []
    races_data = []
    race_urls = set()
    
    async with aiohttp.ClientSession() as session:
        for name, url in all_riders:
            rider_info = await process_rider(name, url, session)
            if not rider_info:
                continue
            riders_data.append(rider_info)
            rider_url = rider_info["url"]
            results = await process_results(rider_url + "/results/last-tt-results", session)
            if not results:
                continue
            results_data.extend(results)
            for result in results:
                race_url = result["race_url"]
                if race_url in race_urls:
                    continue
                race_urls.add(race_url)
                race_info = await process_race(race_url, session)
                if not race_info:
                    continue
                races_data.append(race_info)
            
    riders_df = pd.DataFrame(riders_data)
    riders_df = riders_df.sort_values(["last_name","first_name"])
    riders_df.to_csv("data/riders.csv",index=False)
    
    results_df = pd.DataFrame(results_data)
    results_df = results_df.sort_values("rider_url")
    results_df.to_csv("data/results.csv",index=False)
    
    races_df = pd.DataFrame(races_data)
    races_df = races_df.sort_values("date",ascending=False)
    races_df.to_csv("data/races.csv",index=False)

if __name__ == "__main__":
    asyncio.run(main())
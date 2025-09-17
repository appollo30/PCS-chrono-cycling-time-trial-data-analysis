import asyncio
import aiohttp
from src.get_tt_specialists import get_all_tt_specialists, process_rider, process_rider_sync
from src.get_tt_results import process_results
from src.get_tt_races import process_race
import pandas as pd
from typing import List, Dict, Set, Tuple
from tqdm.asyncio import tqdm

async def main(to_csv=True, to_sqlite=True, to_mysql=False):
    # Collecting all time trial specialists
    all_riders = get_all_tt_specialists()
    
    async with aiohttp.ClientSession() as session:
        # Process all riders concurrently with progress bar
        riders_tasks = [process_rider(name, url, session, verbose=False) for name, url in all_riders]
        print()
        riders_data = await tqdm.gather(*riders_tasks, desc="Processing riders")
        # Filter out None results
        riders_data = [rider for rider in riders_data if rider]
        
        # Process all results concurrently with progress bar
        results_tasks = [
            process_results(rider["url"] + "/results/last-tt-results", session, verbose=False) 
            for rider in riders_data
        ]
        print()
        results_data = await tqdm.gather(*results_tasks, desc="Processing results")
        # Flatten the list of lists and filter out None results
        results_data = [result for sublist in results_data if sublist for result in sublist]
        
        # Collect all unique race URLs
        race_urls = set()
        for result in results_data:
            race_urls.add(result["race_url"])
        
        # Process all races concurrently with progress bar
        print(len(race_urls))
        races_tasks = [process_race(url, session, verbose=False) for url in list(race_urls)]
        print()
        races_data = await tqdm.gather(*races_tasks, desc="Processing races", )
        # Filter out None results
        races_data = [race for race in races_data if race]
        
    # Save data to CSV files        
    riders_df = pd.DataFrame(riders_data)
    riders_df = riders_df.sort_values(["last_name","first_name"])
    
    results_df = pd.DataFrame(results_data)
    results_df = results_df.sort_values(["rider_url","race_url"])
    
    races_df = pd.DataFrame(races_data)
    races_df["date"] = pd.to_datetime(races_df["date"])
    races_df = races_df.sort_values("date",ascending=False)
    
    if to_csv:
        riders_df.to_csv("data/riders.csv",index=False)
        results_df.to_csv("data/results.csv",index=False)
        races_df.to_csv("data/races.csv",index=False)

if __name__ == "__main__":
    asyncio.run(main())
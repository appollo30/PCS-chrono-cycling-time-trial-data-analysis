import asyncio
import aiohttp
from get_tt_specialists import get_all_tt_specialists, process_rider
from get_tt_results import process_results
from get_tt_races import process_race
import pandas as pd
from typing import List, Dict, Set, Tuple

async def main():
    # Collecting all time trial specialists
    all_riders = get_all_tt_specialists()
    
    async with aiohttp.ClientSession() as session:
        # Process all riders concurrently
        riders_tasks = [process_rider(name, url, session) for name, url in all_riders]
        riders_data = await asyncio.gather(*riders_tasks)
        # Filter out None results
        riders_data = [rider for rider in riders_data if rider]
        
        # Process all results concurrently
        results_tasks = [
            process_results(rider["url"] + "/results/last-tt-results", session) 
            for rider in riders_data
        ]
        results_data = await asyncio.gather(*results_tasks)
        # Flatten the list of lists and filter out None results
        results_data = [result for sublist in results_data if sublist for result in sublist]
        
        # Collect all unique race URLs
        race_urls = set()
        for result in results_data:
            race_urls.add(result["race_url"])
        
        # Process all races concurrently
        races_tasks = [process_race(url, session) for url in list(race_urls)]
        races_data = await asyncio.gather(*races_tasks)
        # Filter out None results
        races_data = [race for race in races_data if race]
        
    # Save data to CSV files        
    riders_df = pd.DataFrame(riders_data)
    riders_df = riders_df.sort_values(["last_name","first_name"])
    riders_df.to_csv("data/riders.csv",index=False)
    
    results_df = pd.DataFrame(results_data)
    results_df = results_df.sort_values(["rider_url","race_url"])
    results_df.to_csv("data/results.csv",index=False)
    
    races_df = pd.DataFrame(races_data)
    races_df = races_df.sort_values("date",ascending=False)
    races_df.to_csv("data/races.csv",index=False)

if __name__ == "__main__":
    asyncio.run(main())
import pandas as pd
from utils import fetch_async
from datetime import datetime
import aiohttp
import asyncio

allowed_classes = {"2.UWT","2.Pro", "2.1", "WC", "NC", "CC", "Olympics"}
pnt = [None, 100, 70, 50, 40, 32, 26, 22, 18, 14, 10, 8, 6, 4, 2, 1]

async def get_time_trials_per_rider(rider_url, session, verbose=True) -> pd.DataFrame:
    if verbose:
        print("Processing rider time trial results")
    
    data = list()
    
    time_trials_url = f"{rider_url}/results/last-tt-results"
    soup = await fetch_async(time_trials_url, session)
    
    base_url = "https://www.procyclingstats.com/"
    
    all_lines = soup.select("body > div.wrapper > div.content > div.page-content > div > div.mt10 > table > tbody > tr")
    for line in all_lines:
        date_str = line.select_one("td:nth-child(1)").get_text()
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.year < 2020:
            break
        race_class = line.select_one("td:nth-child(4)").get_text()
        if race_class not in allowed_classes:
            continue
        result_str = line.select_one("td:nth-child(3)").text
        if not result_str.isdigit():
            continue
        result = int(result_str)
        if result > 20:
            continue
        race = line.select_one("td:nth-child(2) > a")
        race_name = race.text
        race_url =  base_url + race.get("href")
        if result <= 15:
            pnt_score = pnt[result]
        else:
            pnt_score = 0
        seconds_lost = minutes_to_seconds(line.select_one("td:nth-child(6)").text)
        data.append({"rider_url" : rider_url, "race_url" : race_url ,"race_name" : race_name, "result" : result, "seconds_lost" : seconds_lost, "pnt" : pnt_score})
    
    df = pd.DataFrame(data)
        
    return df

def minutes_to_seconds(time_in_minutes : str):
    split = time_in_minutes.split(":")
    return int(split[0])*60 + int(split[1])



if __name__ == "__main__":
    async def main():
        riders_df = pd.read_csv("data/riders.csv")
        results_df = pd.DataFrame(columns=["rider_url", "race_url", "race_name", "result", "seconds_lost", "pnt"])
        
        async with aiohttp.ClientSession() as session:
            for i, rider in riders_df.iterrows():
                print(f"Processing rider {rider.full_name}")
                rider_url = rider["url"]
                rider_results = await get_time_trials_per_rider(rider_url=rider_url, session=session)
                results_df = pd.concat([results_df, rider_results])
        
        results_df.to_csv("data/results.csv",index=False)
    
    asyncio.run(main())
    
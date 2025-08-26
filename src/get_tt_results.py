import pandas as pd
from src.utils import fetch, fetch_async, minutes_to_seconds
from datetime import datetime
import aiohttp
import asyncio
from typing import List, Dict

BASE_URL = "https://www.procyclingstats.com/"
allowed_classes = {"2.UWT","2.Pro", "2.1", "WC", "NC", "CC", "Olympics"}
pnt = [None, 100, 70, 50, 40, 32, 26, 22, 18, 14, 10, 8, 6, 4, 2, 1]
# Races that are forbidden to enter the database, for simplicity's sake
forbidden_races = {
    "https://www.procyclingstats.com/race/nc-denmark-itt/2024", # Title stripped, then allowed, complicated shit, + half the info is missing
    "https://www.procyclingstats.com/race/volta-ao-algarve/2020/stage-5", # The length of the TT is 0km for some reason, even though it was like 20kms in reality.
    "https://www.procyclingstats.com/race/giro-d-italia/2022/stage-21", # Same goes for the next TTs
    "https://www.procyclingstats.com/race/giro-d-italia/2021/stage-21",
    "https://www.procyclingstats.com/race/giro-d-italia/2020/stage-21",
    "https://www.procyclingstats.com/race/tirreno-adriatico/2021/stage-7",
    "https://www.procyclingstats.com/race/tirreno-adriatico/2020/stage-8",
    "https://www.procyclingstats.com/race/tour-de-romandie/2021/stage-5",
    "https://www.procyclingstats.com/race/nc-czech-republic-itt/2022",
    "https://www.procyclingstats.com/race/volta-a-portugal/2020/stage-8",
    "https://www.procyclingstats.com/race/nc-romania-itt/2021",
    "https://www.procyclingstats.com/race/nc-romania-itt/2023",
    "https://www.procyclingstats.com/race/nc-panama-itt/2024",
    "https://www.procyclingstats.com/race/etoile-de-besseges/2021/stage-5",
    "https://www.procyclingstats.com/race/etoile-de-besseges/2020/stage-5",
    "https://www.procyclingstats.com/race/ruta-del-sol/2020/stage-5",
    "https://www.procyclingstats.com/race/nc-panama-itt/2024/result",
    "https://www.procyclingstats.com/race/nc-romania-itt/2023/result",
    "https://www.procyclingstats.com/race/nc-romania-itt/2021/result",
    "https://www.procyclingstats.com/race/nc-czech-republic-itt/2022/result",
    ""
}

async def process_results(url, session, verbose=True):
    soup = await fetch_async(url, session, verbose=verbose)
    
    data = parse_results(url, soup, verbose=verbose)
    return data

def process_results_sync(url, verbose=True):
    soup = fetch(url, verbose=verbose)
    
    data = parse_results(url, soup, verbose=verbose)
    return data

def parse_results(url, soup, verbose=True):
    if verbose:
        print("Processing rider time trial results")
        
    data = list()
    
    all_lines = soup.select("body > div.wrapper > div.content > div.page-content > div > div.mt10 > table > tbody > tr")
    for line in all_lines:
        rider_result = dict()
        
        date_str = line.select_one("td:nth-child(1)").get_text()
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.year < 2020:
            break
        
        race_class = line.select_one("td:nth-child(4)").get_text()
        if race_class not in allowed_classes:
            continue
        
        rider_result["rider_url"] = url
        
        result_str = line.select_one("td:nth-child(3)").text
        if not result_str.isdigit():
            continue
        result = int(result_str)
        if result > 20:
            continue
        rider_result["result"] = result
        
        if result <= 15:
            pnt_score = pnt[result]
        else:
            pnt_score = 0
        rider_result["pnt"] = pnt_score
        
        rider_result["seconds_lost"] = minutes_to_seconds(line.select_one("td:nth-child(6)").text)
        
        race = line.select_one("td:nth-child(2) > a")
        race_url =  BASE_URL + race.get("href")
        if race_url in forbidden_races:
            continue
        rider_result["race_url"] = race_url
        
        data.append(rider_result)
    
    return data

if __name__ == "__main__":
    async def main():
        riders_df = pd.read_csv("data/riders.csv")
        data = []
        
        async with aiohttp.ClientSession() as session:
            for i, rider in riders_df.iterrows():
                results_url = rider["url"] + "/results/last-tt-results"
                rider_results = await process_results(results_url,session)
                data.extend(rider_results)
        
        results_df = pd.DataFrame(data)
        results_df = results_df.sort_values("rider_url")
        results_df.to_csv("data/results.csv",index=False)
    
    asyncio.run(main())
    
"""
Module to scrape time trial race information from pcs
"""

import asyncio
from typing import Dict, Union
import re
from time import perf_counter
import pandas as pd
import aiohttp
from bs4 import BeautifulSoup
from src.utils import fetch, fetch_async, to_numeric, minutes_to_seconds

BASE_URL = "https://www.procyclingstats.com/"

async def process_race(url : str, session : aiohttp.ClientSession, verbose=True) -> Dict:
    """
    Async function to process a race's page and extract relevant information.
    Args:
        url (str): URL
        session (aiohttp.ClientSession): Reusable session for connection pooling.
        verbose (bool): Whether to print progress messages. Defaults to True.
    Returns:    
        Dict: A dictionary containing race information.
    """
    soup = await fetch_async(url,session, verbose=verbose)

    result = parse_race(soup, verbose=verbose)
    result["url"] = url
    return result

def process_race_sync(url : str, verbose=True) -> Dict:
    """
    Synchronous function to process a race's page and extract relevant information.
    Args:
        url (str): URL
        verbose (bool): Whether to print progress messages. Defaults to True.
    Returns:    
        Dict: A dictionary containing race information.
    """
    soup = fetch(url, verbose=verbose)

    result = parse_race(soup,verbose=verbose)
    result["url"] = url
    return result

def parse_race(soup : BeautifulSoup, verbose=True) -> Dict:
    result = {}
    
    result["race_title"] = soup.select_one("head > title").get_text().replace(" results", "")
    if verbose :
        print(f"Parsing race {result["race_title"]}")
    
    
    overall_info = soup.select_one("div.borderbox.w30.right.mb_w100")
    race_info = overall_info.select("ul.list.keyvalueList.lineh16.fs12 li > div.value")  
    values = [info.get_text() for info in race_info]
    
    result.update({
        "date" : values[0],
        "departure" : values[12],
        "arrival" : values[13],
        "class" : values[3],
        "distance" : to_numeric(values[5].split()[0]),
        "vertical_meters" : to_numeric(values[11]),
        "startlist_quality" : handle_startlist_quality(values[15]),
        "profile_score" : to_numeric(values[10])
    })
                
    temperature_str = values[17]
    if len(temperature_str.strip()) == 0:
        result["temperature"] = None
    else:
        result["temperature"] = to_numeric(values[17].split()[0])
    
    result["race_ranking"] = to_numeric(values[14])
    
    winner_time_str = soup.select_one("#resultsCont").select_one("td.time.ar > span").get_text()
    result["winner_time"] = minutes_to_seconds(winner_time_str, sep = ":" if ":" in winner_time_str else ".") # in seconds
    result["winner_speed"] = round(3600*result["distance"]/result["winner_time"],3) # in km/h
    
    profile_image_url_extension = overall_info.select_one("div.mt10 img")
    if profile_image_url_extension:
        result["profile_image_url"] = BASE_URL + profile_image_url_extension.get("src")
    else:
        result["profile_image_url"] = None
    
    return result

def handle_startlist_quality(s : str) -> Union[int, None]:
    split = s.split()
    if len(split) == 0:
        return None
    if len(split) == 1:
        return to_numeric(split[0])
    if len(split) == 2:
        return to_numeric(re.sub(r"[()]", "", split[1]))


if __name__ == "__main__":
    async def main():
        results_df = pd.read_csv('data/results.csv')
        url_set = set(results_df["race_url"].unique())
        url_list = list(url_set)
        async with aiohttp.ClientSession() as session:
            tasks = [process_race(url,session) for url in url_list]
            data = await asyncio.gather(*tasks)

        races_df = pd.DataFrame(data)
        races_df["date"] = pd.to_datetime(races_df["date"])
        races_df = races_df.sort_values("date",ascending=False)
        races_df.to_csv("data/races.csv",index=False)

    asyncio.run(main())
    #test_race("http://procyclingstats.com/race/tour-de-romandie/2023/stage-3")

from src.utils import fetch, fetch_async, minutes_to_seconds, to_numeric
import pandas as pd
import aiohttp
import asyncio
from time import perf_counter

BASE_URL = "https://www.procyclingstats.com/"

async def process_race(url, session, verbose=True):
    soup = await fetch_async(url,session, verbose=verbose)
    
    result = parse_race(soup, verbose=verbose)
    result["url"] = url
    return result

def process_race_sync(url, verbose=True):
    soup = fetch(url, verbose=verbose)
    
    result = parse_race(soup,verbose=verbose)
    result["url"] = url
    return result

def parse_race(soup, verbose=True):
    result = dict()
    
    result["race_title"] = soup.select_one("head > title").get_text().replace(" results", "")
    if verbose :
        print(f"Parsing race {result["race_title"]}")
    
    overall_info = soup.select_one("body > div.wrapper > div.content > div.page-content.noSideNav > div > div.borderbox.w30.right.mb_w100")
    
    race_info = overall_info.select_one("div.left.w70 > ul")

    result["date"] = race_info.select_one("li:nth-child(1) > div.value").get_text()
    result["departure"] = race_info.select_one("li:nth-child(13) > div.value > a").get_text()
    result["arrival"] = race_info.select_one("li:nth-child(14) > div.value > a").get_text()
    result["class"] = race_info.select_one("li:nth-child(4) > div.value").get_text()
    result["distance"] = float(race_info.select_one("li:nth-child(6) > div.value").get_text().split()[0]) # in km
    
    vertical_meters = race_info.select_one("li:nth-child(12) > div.value").get_text() # in m
    result["vertical_meters"] = to_numeric(vertical_meters)
    
    startlist_quality = race_info.select_one("li:nth-child(16) > div.value > a").get_text()
    result["startlist_quality"] = to_numeric(startlist_quality)
    
    profile_score = race_info.select_one("li:nth-child(11) > div.value").get_text()
    result["profile_score"] = to_numeric(profile_score)
    
    temperature = race_info.select_one("li:nth-child(18) > div.value > a").get_text().split(" ")[0] # in °C
    result["temperature"] = to_numeric(temperature)
    
    race_ranking = race_info.select_one("li:nth-child(15) > div.value > a").get_text()
    result["race_ranking"] = to_numeric(race_ranking)
    
    winner_time_str = soup.select_one("#resultsCont > div:nth-child(1) > div > table > tbody > tr:nth-child(1) > td.time.ar").get_text()
    if ":" in winner_time_str:
        result["winner_time"] = minutes_to_seconds(winner_time_str,sep=":") # in seconds
    else:  
        result["winner_time"] = minutes_to_seconds(winner_time_str.split(",")[0],sep=".") # in seconds
        
    result["winner_speed"] = round(3600*result["distance"]/result["winner_time"],3) # in km/h
    
    profile_image_url_extension = overall_info.select_one("div:nth-child(4) > ul > li > div > a > img")
    
    if profile_image_url_extension:
        result["profile_image_url"] = BASE_URL + profile_image_url_extension.get("src")
    else:
        result["profile_image_url"] = None
    
    return result

def test_race(url):
    result = process_race_sync(url, verbose=True)
    print(result)

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
import pandas as pd
import asyncio
import aiohttp
from src.utils import fetch, fetch_async
from typing import List, Dict, Set, Tuple

BASE_URL = "https://www.procyclingstats.com/"

async def process_rider(full_name, url, session, verbose=True):
    soup = await fetch_async(url,session, verbose=verbose)
    
    result = parse_rider(full_name, soup, verbose=verbose)
    result["url"] = url
    return result

def process_rider_sync(full_name, url, verbose=True):
    soup = fetch(url, verbose=verbose)
    
    result = parse_rider(full_name, soup, verbose=verbose)
    result["url"] = url
    return result

def parse_rider(full_name : str, soup, verbose=True) -> Dict:
    
    result = dict()
    first_name, last_name = process_name(full_name)
    result["first_name"] = first_name
    result["last_name"] = last_name
    result["full_name"] = first_name + " " + last_name
    
    if verbose:
        print(f"Processing rider {full_name}")
    
        
    rider_info = soup.select_one("body > div.wrapper > div.content > div.page-content.noSideNav > div > div.borderbox.left.w40.mb_w100 > div.borderbox.left.w65")
    result["nationality"] = rider_info.select_one("div:nth-child(3) > ul > li > div:nth-child(3) > a").get_text()
    result["birth_year"] = int(rider_info.select_one("div:nth-child(2) > ul > li > div:nth-child(4)").get_text())
    
    rider_dimensions = rider_info.select_one(f"div:nth-child(4) > ul > li")
    result["height"] = float(rider_dimensions.select_one(f"div:nth-child(5)").get_text())
    result["weight"] = float(rider_dimensions.select_one(f"div:nth-child(2)").get_text())
    
    result["onedayraces"] = int(rider_info.select_one("ul > li:nth-child(1) > div.xvalue.ac").get_text())
    result["gc"] = int(rider_info.select_one("ul > li:nth-child(2) > div.xvalue.ac").get_text())
    result["tt"] = int(rider_info.select_one("ul > li:nth-child(3) > div.xvalue.ac").get_text())
    result["sprint"] = int(rider_info.select_one("ul > li:nth-child(4) > div.xvalue.ac").get_text())
    result["climber"] = int(rider_info.select_one("ul > li:nth-child(5) > div.xvalue.ac").get_text())
    result["hills"] = int(rider_info.select_one("ul > li:nth-child(6) > div.xvalue.ac").get_text())
    
    result["photo_url"] = BASE_URL + soup.select_one("body > div.wrapper > div.content > div.page-content.noSideNav > div > div.borderbox.left.w40.mb_w100 > div.borderbox.left.w30.mr5 > div > a > img").get("src")
    
    return result

def process_name(full_name : str) -> Tuple[str,str]:
    split = full_name.strip().split(" ")
    last_name = ""
    for i, word in enumerate(split):
        if word == word.upper():
            last_name += word.capitalize() + " "
        else:
            break
    last_name = last_name.strip()
    first_name = " ".join(split[i:])
    return first_name, last_name

def get_all_tt_specialists_per_year(year : int=2025, verbose : bool=True) -> Set[Tuple[str,str]]:
    result = set()
    
    rider_specialties_url = f"https://www.procyclingstats.com/rankings.php?date={year-1}-12-31&nation=&age=&zage=&page=smallerorequal&team=&offset=0&filter=Filter&p=me&s=time-trial"
    if verbose:
        print(f"Accessing the list of riders for {year}")
    soup = fetch(rider_specialties_url)
    
    all_rows = soup.select("body > div.wrapper > div.content > div.page-content > div > div:nth-child(4) > table > tbody > tr")
    for i in range(0, 50):
        if i < len(all_rows):
            rider_link = all_rows[i].select_one("td:nth-child(4) > a")
            if rider_link:
                result.add((rider_link.text, BASE_URL + rider_link.get("href"))) # (name, url) tuple
    return result

def get_all_tt_specialists() -> Set[Tuple[str,str]]:
    tt_specialists_set = set()
    for year in range(2020,2025):
        tt_specialists_set = tt_specialists_set | get_all_tt_specialists_per_year(year)
    
    return tt_specialists_set

if __name__ == "__main__":
    async def main():
        all_riders = get_all_tt_specialists()
        
        async with aiohttp.ClientSession() as session:
            tasks = [process_rider(name, url, session) for name, url in all_riders]
            data = await asyncio.gather(*tasks)
        riders_df = pd.DataFrame(data)
        riders_df = riders_df.sort_values(["last_name","first_name"])
        riders_df.to_csv("data/riders.csv",index=False)
    
    asyncio.run(main())
    

    
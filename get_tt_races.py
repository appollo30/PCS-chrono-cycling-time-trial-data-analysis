from utils import fetch_async, minutes_to_seconds
import aiohttp
import asyncio

async def parse_race(url, session, verbose=True):
    soup = await fetch_async(url, session)
    
    result = dict()
    
    result["race_title"] = soup.select_one("head > title").get_text().replace(" results", "")
    if verbose :
        print(f"Processing race {result["race_title"]}")
    
    base_url = "https://www.procyclingstats.com/"
    
    overall_info = soup.select_one("body > div.wrapper > div.content > div.page-content.noSideNav > div > div.borderbox.w30.right.mb_w100")
    
    race_info = overall_info.select_one("div.left.w70 > ul")
    
    result["date"] = race_info.select_one("li:nth-child(1) > div.value").get_text()
    result["departure"] = race_info.select_one("li:nth-child(12) > div.value > a").get_text()
    result["arrival"] = race_info.select_one("li:nth-child(13) > div.value > a").get_text()
    result["class"] = race_info.select_one("li:nth-child(4) > div.value").get_text()
    result["distance"] = float(race_info.select_one("li:nth-child(6) > div.value").get_text().split()[0])
    result["vertical_meters"] = int(race_info.select_one("li:nth-child(11) > div.value").get_text())
    result["startlist_quality"] = int(race_info.select_one("li:nth-child(15) > div.value > a").get_text())
    result["profile_score"] = int(race_info.select_one("li:nth-child(10) > div.value").get_text())
    result["temperature"] = float(race_info.select_one("li:nth-child(17) > div.value > a").get_text().split(" ")[0])
    result["race_ranking"] = int(race_info.select_one("li:nth-child(14) > div.value > a").get_text())
    
    result["winner_time"] = minutes_to_seconds(soup.select_one("#resultsCont > div:nth-child(1) > div > table > tbody > tr:nth-child(1) > td.time.ar").get_text().split(",")[0],sep=".")
    
    result["profile_image_url"] = base_url + overall_info.select_one("div:nth-child(4) > ul > li > div > a > img").get("src")
    
    return result

if __name__ == "__main__":
    async def main():
        url = "https://www.procyclingstats.com/race/giro-d-italia/2025/stage-10"
        async with aiohttp.ClientSession() as session:
            result = await parse_race(url, session)
        print(result)
    asyncio.run(main())
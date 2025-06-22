from bs4 import BeautifulSoup
import requests
import pandas as pd


def collect_time_trial_specialists(year=2025, verbose=True):
    result = dict()
    
    base_url = "https://www.procyclingstats.com/"
    rider_specialties_url = f"https://www.procyclingstats.com/rankings.php?date={year-1}-12-31&nation=&age=&zage=&page=smallerorequal&team=&offset=0&filter=Filter&p=me&s=time-trial"
    if verbose:
        print(f"Accessing the list of riders for {year}")
    response = requests.get(rider_specialties_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    all_rows = soup.select("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > span > table > tbody > tr")

    for i in range(0, 50):
        if i < len(all_rows):
            rider_link = all_rows[i].select_one("td:nth-child(4) > a")
            if rider_link:
                result[rider_link.text] = base_url + rider_link.get("href") # URL : name key-value pairs
    return result

def get_tt_specialists():
    tt_specialists_dict = dict()
    for year in range(2020,2025):
        tt_specialists_dict = tt_specialists_dict | collect_time_trial_specialists(year)
    
    return tt_specialists_dict
    
def process_name(full_name):
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

def parse_rider(full_name, url, verbose=True):
    if verbose:
        print(f"Processing rider {full_name}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    result = dict()
    result["url"] = url
    first_name, last_name = process_name(full_name)
    result["first_name"] = first_name
    result["last_name"] = last_name
    result["full_name"] = first_name + " " + last_name
    
    result["nationality"] = soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont > a").get_text()
    
    # shittiest code ever
    info = soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont")
    split_info = info.get_text().split()
    n = len(split_info)
    result["birth_year"] = None
    result["height"] = None
    result["weight"] = None
    for i, info in enumerate(split_info):
        if i > 1:
            if info == "kg":
                result["weight"] = float(split_info[i-1])
                continue
        if i < n-1:
            if info == "Height:":
                result["height"] = float(split_info[i+1])
        if i < n-4:
            if info == "birth:" and split_info[i+4].endswith("Nationality:"):
                result["birth_year"] = int(split_info[i+3])
                continue
        
    result["onedayraces"] = int(soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont > span:nth-child(8) > span > div.pps > ul > li:nth-child(1) > div.pnt").get_text())
    result["gc"] = int(soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont > span:nth-child(8) > span > div.pps > ul > li:nth-child(1) > div.pnt").get_text())
    result["tt"] = int(soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont > span:nth-child(8) > span > div.pps > ul > li:nth-child(3) > div.pnt").get_text()) 
    result["sprint"] = int(soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont > span:nth-child(8) > span > div.pps > ul > li:nth-child(4) > div.pnt").get_text())
    result["climber"] = int(soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont > span:nth-child(8) > span > div.pps > ul > li:nth-child(5) > div.pnt").get_text()) 
    result["hills"] = int(soup.select_one("body > div.wrapper > div.content > div.page-content.page-object.default > div:nth-child(2) > div.left.w75.mb_w100 > div.left.w50.mb_w100 > div.rdr-info-cont > span:nth-child(8) > span > div.pps > ul > li:nth-child(6) > div.pnt").get_text())
    
    
    return result



if __name__ == "__main__":
    tt_specialists_dict = get_tt_specialists()
    data = [parse_rider(name,url) for name, url in tt_specialists_dict.items()]
    df = pd.DataFrame(data)
    df.to_csv("data/riders.csv",index=False)
    
    # url = "https://www.procyclingstats.com/rider/vincenzo-nibali"
    # name = "NIBALI Vincenzo"
    # print(parse_rider(full_name=name,url=url))
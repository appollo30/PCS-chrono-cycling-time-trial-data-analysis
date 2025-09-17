import requests
from bs4 import BeautifulSoup

def fetch(url, headers=None, parser="html.parser", verbose=True):
    """
    Fetches the content of a URL and returns a BeautifulSoup object.

    Args:
        url (str): The URL to fetch.
        headers (dict, optional): Optional HTTP headers to send with the request.
        parser (str, optional): The parser to use with BeautifulSoup. Defaults to "html.parser".

    Returns:
        BeautifulSoup: Parsed HTML content.
    """
    response = requests.get(url, headers=headers)
    if verbose:
        print("Accessing page : ", url)
    response.raise_for_status()
    return BeautifulSoup(response.text, parser)

async def fetch_async(url, session, headers=None, parser="html.parser", verbose=True):
    """
    Asynchronously fetches the content of a URL and returns a BeautifulSoup object.

    Args:
        url (str): The URL to fetch.
        session (aiohttp.ClientSession): Reusable session for connection pooling.
        headers (dict, optional): Optional HTTP headers to send with the request.
        parser (str, optional): The parser to use with BeautifulSoup. Defaults to "html.parser".

    Returns:
        BeautifulSoup: Parsed HTML content.
    """
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        text = await response.text()
        if verbose:
            print("Accessing page : ", url)
        return BeautifulSoup(text, parser)
    
def minutes_to_seconds(time_in_minutes : str, sep = ":"):
    split = time_in_minutes.split(sep)
    if len(split) == 3:
        return int(split[0])*3600 + int(split[1])*60 + int(split[2])
    return int(split[0])*60 + int(split[1])

def to_numeric(s : str):
    """
    Takes a string, checks if it is numeric, if so, it gives the numeric version, if not it gives None
    """
    s = s.strip()
    if s.lower() == "n/a":
        return None
    if s.replace('.', '', 1).isdigit():
        if '.' in s:
            return float(s)
        else:
            return int(s)
    return None
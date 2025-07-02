import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

def fetch(url, headers=None, parser="html.parser"):
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
    response.raise_for_status()
    return BeautifulSoup(response.text, parser)

async def fetch_async(url, session, headers=None, parser="html.parser"):
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
        return BeautifulSoup(text, parser)
    
def minutes_to_seconds(time_in_minutes : str, sep = ":"):
    split = time_in_minutes.split(sep)
    return int(split[0])*60 + int(split[1])
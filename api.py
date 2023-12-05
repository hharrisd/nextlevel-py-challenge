import asyncio
import itertools
import random
from pprint import pprint

import requests
from environs import Env, EnvError

env = Env()
env.read_env()  # Read .env file, if exisists
API_TOKEN = ""

try:
    API_TOKEN = env("API_TOKEN")
except EnvError as e:
    print("Set the environment variable API_TOKEN to use this app.")
    raise EnvError(e)

# A few handy JSON types
JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]

BASE_URL: str = "https://the-one-api.dev/v2"


def send_get_request(url: str) -> JSONObject | None:
    """Executes a synchronous GET request"""
    print("Sending HTTP request")

    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json',
    }
    res = requests.request("GET", url, headers=headers)
    # Check if the response status code is 200 (OK)
    if res.status_code == 200:
        try:
            return res.json()  # Try to decode JSON
        except requests.exceptions.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None  # Return None or handle the error accordingly
    else:
        print(f"Request failed with status code: {res.status_code}")
        print(res.text)
        return None  # Return None or handle the error accordingly


async def send_async_request(url: str) -> JSONObject:
    """Executes an asynchronous GET request"""
    return await asyncio.to_thread(send_get_request, url)


async def get_characters(limit: int, page: int) -> JSONList:
    """Executes an asynchronous request to the API to get characters

    Args:
    - limit: int - The number of characters to
    - page: int - The page number of the request

    Returns:
    - characters_list: JSONList - A list of characters
    """
    characters_url = f"{BASE_URL}/character?limit={limit}&page={page}"
    characters_list = await send_async_request(characters_url)
    return characters_list["docs"]


async def get_all_characters() -> JSONList:
    """Get all characters in three request with a limit of 333 characters per page.
    Concatenates the responses and returns a list of JSON objects

    Returns:
    - characters_list: JSONList a list of characters objects
    """
    characters_response = await asyncio.gather(*[get_characters(limit=333, page=page) for page in range(1, 4)])
    characters = list(itertools.chain.from_iterable(characters_response))
    return characters


async def get_random_quoute_by_character(char_id: str) -> str | None:
    """
    Get the quoute by character

    Args:
    - char_id: str - Character ID

    Returns:
    - quote: list[str] - List of quotes
    """
    quoutes_url = f"{BASE_URL}/character/{char_id}/quote"
    quoute_list = await send_async_request(quoutes_url)
    print(f"quoute_list total: {quoute_list['total']}")
    if not quoute_list["total"]:
        return ""
    return random.choice(quoute_list["docs"])["dialog"]


async def get_quotes(limit: int, page: int) -> JSONList:
    """Executes an asynchronous request to the API to get quotes

    Args:
    - limit: int - The number of characters to
    - page: int - The page number of the request

    Returns:
    - quotes: JSONList - The List of quotes
    """
    characters_url = f"{BASE_URL}/quote?limit={limit}&page={page}"
    quote_list = await send_async_request(characters_url)
    return quote_list["docs"]


async def get_all_quotes() -> JSONList:
    """Get all quotes in five request with a limit of 500 quotes per page.
    Concatenates the responses and returns a list of JSON objects

    Returns:
    - quotes: JSONList a list of characters objects
    """
    quotes_response = await asyncio.gather(*[get_quotes(limit=500, page=page) for page in range(1, 6)])
    quotes = list(itertools.chain.from_iterable(quotes_response))
    return quotes


def get_movies() -> JSONList:
    """Executes an asynchronous request to the API to get quotes

    Returns:
    - quotes: JSONList - The List of quotes
    """
    movies_url = f"{BASE_URL}/movie"
    quote_list = send_get_request(movies_url)
    return quote_list["docs"]


if __name__ == '__main__':
    # quote = asyncio.run(get_random_quoute_by_character(char_id="5cdbdecb6dc0baeae48cfa9b"))
    # quote = asyncio.run(get_all_quotes())
    quote = get_movies()
    pprint(quote)

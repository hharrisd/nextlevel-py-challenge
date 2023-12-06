import logging
import os
from typing import Collection, Generator

import csv

import aiofiles

from api import get_all_characters, get_all_quotes, get_movies
from models import Character, Quote, Movie

CSV_FILES = ["characters.csv", "quotes.csv", "movies.csv"]


class CSVFileCreator:
    """Asynchronous context manager class that creates a CSV file in the data directory."""

    def __init__(self, file_name, headers):
        self.file_name: str = file_name
        self.headers: list[str] = headers

    async def __aenter__(self):
        directory = 'data'
        file_path = os.path.join(directory, self.file_name)
        self.file = await aiofiles.open(file=file_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=self.headers)
        await self.writer.writeheader()
        return self.writer

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.file.close()
        if exc_type is not None:
            # Handle exceptions here if needed
            logging.exception(f"Exception occurred: {exc_type}, {exc_value}, {traceback}")
            # Return False to propagate the exception
            return False


def check_file_exists(file_name: str) -> bool:
    """Check if a file exists in the data directory"""
    directory = 'data'
    file_path = os.path.join(directory, file_name)
    return os.path.isfile(file_path)


def check_files_exists(files: Collection[str]) -> bool:
    """Ckecks if all the files are present in the data directory"""
    return all((check_file_exists(file_name) for file_name in files))


async def create_files():
    characters_headers = ["id", "name", "gender", "race", "realm"]
    quotes_headers = ["id", "dialog", "movie", "character"]
    movies_headers = ["id", "name"]

    characters_json = await get_all_characters()
    quotes_json = await get_all_quotes()
    movies_json = get_movies()

    async with CSVFileCreator(file_name="characters.csv", headers=characters_headers) as csv_file:
        for character_dict in characters_json:
            character = Character(id=character_dict.get("_id"), name=character_dict.get("name"))
            character.gender = character_dict.get("gender", None)
            character.race = character_dict.get("race", None)
            character.realm = character_dict.get("realm", None)

            await csv_file.writerow(character.as_dict())

    async with CSVFileCreator(file_name="quotes.csv", headers=quotes_headers) as quotes_file:
        for quote_dict in quotes_json:
            quote = Quote(id=quote_dict.get("id"),
                          dialog=quote_dict.get("dialog"),
                          movie=quote_dict.get("movie"),
                          character=quote_dict.get("character"))

            await quotes_file.writerow(quote.__dict__)

    # This is a synchronous operation because movie's data is small
    with open("data/movies.csv", mode='w') as movies_file:
        movies_file = csv.DictWriter(movies_file, fieldnames=movies_headers)
        movies_file.writeheader()
        for movie_dict in movies_json:
            movie = Movie(id=movie_dict.get("_id"), name=movie_dict.get("name"))
            movies_file.writerow(movie.__dict__)

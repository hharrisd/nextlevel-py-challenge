import asyncio
import random
from pprint import pprint
from typing import AsyncGenerator

from models import Character, CharacterSet
from api import get_all_characters, get_random_quoute_by_character


async def load_characters() -> CharacterSet:
    character_set = CharacterSet()
    characters_json = await get_all_characters()

    for char_dict in characters_json:
        character = Character(id=char_dict.get("_id"), name=char_dict.get("name"))
        character.gender = char_dict.get("gender", None)
        character.race = char_dict.get("race", None)
        character.realm = char_dict.get("realm", None)
        character_set.characters.append(character)

    return character_set


async def get_random_quoutes(character_list: list[Character]) -> AsyncGenerator[dict, None]:
    for character in character_list:
        print(f"{character.id}")
        yield character.id, await get_random_quoute_by_character(character.id)


async def main() -> None:
    characters = await load_characters()
    random_charactes = random.choices(characters.characters, k=10)
    async for char_quoute in get_random_quoutes(random_charactes):
        print(char_quoute)

    get_random_quoutes(random_charactes)


if __name__ == '__main__':
    asyncio.run(main())

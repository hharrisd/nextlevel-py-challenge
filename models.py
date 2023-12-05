import functools
from dataclasses import dataclass, field
from itertools import groupby
from operator import attrgetter


@dataclass(kw_only=True, slots=True)
class Character:
    """
    Represents a character from the Lord of the Rings
    Attributes:
        - id: str - The character's unique identifier.
        - name: str - The character's name.
        - race: str - The character's race.
        - gender: str - The character's gender.
        - realm: str - The character's realm or place of origin.
    """
    id: str
    name: str
    _gender: str = field(default=None)
    _realm: str = field(default=None)
    _race: str = field(default=None)

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        if value != '' and value is not None and value != 'NaN':
            self._gender = value
        else:
            self._gender = "No Gender"

    @property
    def race(self) -> str | None:
        return self._race

    @race.setter
    def race(self, value: str) -> None:
        if value != '' and value is not None and value != 'NaN':
            self._race = value
        else:
            self._race = "No Race"

    @property
    def realm(self) -> str | None:
        return self._realm

    @realm.setter
    def realm(self, value: str) -> None:
        if value != '' and value is not None and value != 'NaN':
            self._realm = value
        else:
            self._realm = "No Realm"

    def __str__(self) -> str:
        return f"{self.name}, {self.race} from the realm of {self.realm}"


@dataclass
class CharacterSet:
    """
    Class that represents a set of characters

    Attributes:
    - characters: list[Character] - List of characters
    """
    characters: list[Character] = field(default_factory=list)

    def count_characters_by_attribute(self, attribute: str) -> dict[str, int]:
        """
        Travers the list of characters and returns a dictionary with the count of characters
        by a given attribute.

        Args:
        - attribute: str - The attribute by which characters will be counted.

        Returns:
        - dict: A dictionary containing counts of characters grouped by the specified attribute.
        """
        sorted_chars = sorted(self.characters, key=attrgetter(attribute))
        grouped_chars = groupby(sorted_chars, key=attrgetter(attribute))
        count_dict = {key: len(list(group)) for key, group in grouped_chars}
        return count_dict

    """ Usage of functools.partialmethod to create methods from count_characters_by_attribute
        and simplify their calling.
     """
    count_by_race = functools.partialmethod(count_characters_by_attribute, attribute="race")
    count_by_realm = functools.partialmethod(count_characters_by_attribute, attribute="realm")
    count_by_gender = functools.partialmethod(count_characters_by_attribute, attribute="gender")

    def __str__(self) -> str:
        return f"Set of: {len(self.characters)} characters."


@dataclass
class Movie:
    id: str
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class Quote:
    id: str
    dialog: str
    movie: str
    character: str

    def __str__(self) -> str:
        return self.dialog

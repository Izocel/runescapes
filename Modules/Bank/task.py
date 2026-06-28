from dataclasses import dataclass, field
from typing import Literal, Tuple

from Services.Logger import Logger
from Tasks.Task import Task

Location = Tuple[int, int, int]  # (x, y, z)
Region = Literal["auto", "varrock", "falador"]
Map = Literal["auto", "world", "dungeon", "wilderness", "minigame"]


@dataclass(frozen=True)
class Bank:
    map: Map
    region: Region
    location: Location

    def __post_init__(self):
        # Validate map
        valid_maps: tuple[Map, ...] = (
            "auto",
            "world",
            "dungeon",
            "wilderness",
            "minigame",
        )
        if self.map not in valid_maps:
            raise ValueError(f"Invalid map '{self.map}' for Bank")

        # Validate region
        valid_regions: tuple[Region, ...] = ("auto", "varrock", "falador")
        if self.region not in valid_regions:
            raise ValueError(f"Invalid region '{self.region}' for Bank")

        # Validate location
        if len(self.location) != 3:
            raise ValueError("Location must be a tuple of (x, y, z)")

        if not all(isinstance(v, int) for v in self.location):
            raise ValueError("Location values must be integers")


BANKS: dict[Region, Bank] = {
    "auto": Bank(
        map="auto",
        region="auto",
        location=(0, 0, 0),
    ),
    "varrock": Bank(
        map="world",
        region="varrock",
        location=(3200, 3200, 0),
    ),
    "falador": Bank(
        map="world",
        region="falador",
        location=(3000, 3000, 0),
    ),
}


@dataclass
class BankTask(Task):
    path: str
    enable: bool = field(init=False)
    bank: Bank = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        # Load enable flag
        self.enable = self.settings.get("enable", False)

        # Load bank key from settings
        bank_key = self.settings.get("bank", "auto")

        # Resolve bank object
        self.bank = BANKS.get(bank_key, BANKS["auto"])

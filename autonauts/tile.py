#!/usr/bin/python
##-------------------------------##
## Autonauts Save Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## World: Tile                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Generator
from enum import IntEnum

## Constants
__all__: tuple[str, ...] = ("Tile", "decompress_tile_ids")
BUILTIN_NAME_LOOKUP: dict[int, str] = {
    0: "Grass",
    1: "Soil",
    2: "Tilled Soil",
    3: "Holed Soil",
    4: "Orange Soil",
    5: "Soil(Dung)",
    6: "Fresh Water",
    7: "Fresh Water(Deep)",
    8: "Sea Water",
    9: "Sea Water(Deep)",
    10: "Sand",
    11: "Dredged Land",
    12: "Swamp Water",
    13: "Turfed Metal Ore Deposit",
    14: "Trace Metal Ore Deposit",
    15: "Metal Ore Deposit",
    16: "Rich Metal Ore Deposit",
    17: "Used Metal Ore Deposit",
    18: "Turfed Clay Deposit",
    19: "Clay Deposit",
    20: "Rich Clay Deposit",
    21: "Used Clay Deposit",
    22: "Turfed Coal Deposit",
    23: "Trace Coal Deposit",
    24: "Coal Deposite",
    25: "Rich Coal Deposit",
    26: "Pure Coal Deposit",
    27: "Used Coal Deposit",
    28: "Turfed Stone",
    29: "Stone",
    30: "Rich Stone",
    31: "Used Stone",
}


## Functions
def decompress_tile_ids(tile_data: list[int]) -> Generator[int, None, None]:
    """
    Generator for creating Tile list by getting tile id and count and expanding
    [i + 0] = id
    [i + 1] = count
    """
    for i in range(0, len(tile_data), 2):
        _id: int = tile_data[i]
        count: int = tile_data[i + 1]
        for _ in range(count):
            yield _id


## Classes
class Tile:
    """
    Autonauts Tile
    - Stores terrain type and objects attached to position
    """

    # -Constructor
    def __init__(self, _id: int) -> None:
        self.id: int = _id

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"Tile(id={self.id})"

    def __str__(self) -> str:
        return BUILTIN_NAME_LOOKUP.get(self.id, f"(unknown id={self.id})")

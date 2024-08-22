#!/usr/bin/python
##-------------------------------##
## Autonauts Save Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## World: Plot                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum
from typing import ClassVar

## Constants
__all__: tuple[str, ...] = (
    "Plot", "Tile",
    "tile_compression_generator", "tile_decompression_generator",
)


## Functions
def tile_compression_generator(
    tiles: list[Tile]
) -> Generator[tuple[int, int], None, None]:
    """
    Generator for creating tile id and count list by narrowing list down
    """
    pass


def tile_decompression_generator(
    tile_data: list[int]
) -> Generator[Tile, None, None]:
    """
    Generator for creating Tile list by getting tile id and count and expanding
    [i + 0] = tile type
    [i + 1] = tile count
    """
    for i in range(0, len(tile_data), 2):
        _type: Tile = tile_data[i]
        count: int = tile_data[i + 1]
        for _ in range(count):
            yield Tile(_type)


## Classes
class Plot:
    """
    """

    # -Constructor
    def __init__(self, visible: bool, tiles: list[Tile]) -> None:
        self.visible: bool = visible
        self.tiles: list[Tile] = tiles

    # -Dunder Methods
    def __getitem__(self, key: tuple[int, int]) -> None:
        x: int = key[0]
        y: int = key[1]

    def __setitem__(self, key: tuple[int, int], value) -> None:
        x: int = key[0]
        y: int = key[1]

    # -Class Methods
    @classmethod
    def from_position(cls, index: int, size: tuple[int, int], visible: bool, tile_data: list[int]) -> Plot:
        '''
        Returns a plot of land with a list of tiles
        Gets tile content from passed in tile list through generator
        '''
        tiles: list[Tile] = []
        pos_x: int = index % (size[0] // Plot.Width)
        pos_y: int = index // (size[0] // Plot.Width)
        tile_gen = tile_decompression_generator(tile_data)
        for row in range(0, size[1]):
            for column in range(0, size[0] // Plot.Width):
                tile_row = [next(tile_gen) for _ in range(Plot.Width)]
                if column != pos_x:
                    continue
                if row >= pos_y * Plot.Height and row < pos_y * Plot.Height + Plot.Height:
                    tiles.extend(tile_row)
        return cls(visible, tiles)

    # -Class Properties
    Width: ClassVar[int] = 21
    Height: ClassVar[int] = 10


class Tile(IntEnum):
    """Enum for Tile Type <-> Tile Id conversion"""
    Grass = 0
    Dirt = 1
    TilledDirt = 2
    HoledDirt = 3
    OrangeDirt = 4
    SoilDung = 5
    FreshWater = 6
    DeepFreshWater = 7
    SeaWater = 8
    DeepSeaWater = 9
    Sand = 10
    Dredged = 11
    Swamp = 12
    TurfedMetalOre = 13
    TraceMetalOre = 14
    MetalOre = 15
    RichMetalOre = 16
    UsedMetalOre = 17
    TurfedClay = 18
    Clay = 19
    RichClay = 20
    UsedClay = 21
    TurfedCoal = 22
    TraceCoal = 23
    Coal = 24
    RichCoal = 25
    PureCoal = 26
    UsedCoal = 27
    TurfedStone = 28
    Stone = 29
    RichStone = 30
    UsedStone = 31

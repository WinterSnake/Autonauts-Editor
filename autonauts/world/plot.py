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

## Constants
PLOT_WIDTH: int = 21
PLOT_HEIGHT: int = 12


## Functions
"""
Create a function that takes a list of plots and returns the plot visible and tuple of tiles

Tile compression method:
    [0] = tile type
    [1] = tile count
"""
def tile_decompression_generator(tiles: list[int]) -> Generator[Tile, int, None]:
    ''''''
    pass


## Classes
class Plot:
    """
    """

    # -Constructor
    def __init__(self, visible: bool, tiles: list) -> None:
        self.visible: bool = visible
        self.tiles: list = tiles

    # -Dunder Methods
    def __getitem__(self, key: tuple[int, int]) -> None:
        pass

    def __setitem__(self, key: tuple[int, int], value) -> None:
        pass

    # -Instance Methods

    # -Class Methods
    @classmethod
    def from_position(cls, index: int, size: tuple[int, int], visible: bool, tiles: list[int]) -> Plot:
        '''
        '''
        tile_gen = tile_decompression_generator(tiles)
        return cls(visible, tiles)

    # -Static Methods

    # -Properties

    # -Class Properties


class Tile(IntEnum):
    """
    """

    Grass = 0
    Dirt = 1

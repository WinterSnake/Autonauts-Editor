#!/usr/bin/python
##-------------------------------##
## Autonauts Save Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## World: Plot                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterable
from typing import ClassVar

from .tile import Tile

## Constants
__all__: tuple[str] = ("Tile", "compress_plots")


## Functions
def compress_plots(plots: Iterable[Plot]) -> tuple[tuple[bool], tuple[int]]:
    """
    Returns divided plot visibility and chunked tile list to be stored back to game
    """
    pass


## Classes
class Plot:
    """
    Autonauts Plot
    - Stores list of tiles associated with plot in addition to
    if plot is visible to player
    """

    # -Constructor
    def __init__(self, visible: bool, tiles: tuple[Tile]) -> None:
        self.visible: bool = visible
        self._tiles: tuple[Tile] = tiles

    # -Dunder Methods
    def __getitem__(self, key: tuple[int, int]) -> Tile:
        '''(X,Y) index to tile array relative to plot origin'''
        x: int = key[0]
        y: int = key[1]

    # -Class Methods
    @classmethod
    def from_index(
        cls, index: int, size: tuple[int, int],
        visible: bool, tiles: Iterable[Tile]
    ) -> Plot:
        '''Returns a plot of land by given index with a list of tiles attached to plot'''
        assert size[0] * size[1] == len(tiles)
        _tiles: list[Tile] = []
        pos_x: int = (index % (size[0] // Plot.Width)) * Plot.Width
        pos_y: int = (index // (size[0] // Plot.Width)) * Plot.Height
        for y in range(Plot.Height):
            idx: int = pos_x + y * size[0]
            _tiles.extend(tiles[idx : idx + Plot.Width])
        return cls(visible, tuple(_tiles))

    # -Class Properties
    Width: ClassVar[int] = 21
    Height: ClassVar[int] = 10

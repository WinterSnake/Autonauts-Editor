#!/usr/bin/python
##-------------------------------##
## Autonauts Save Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## World                         ##
##-------------------------------##

## Imports
from __future__ import annotations
import json
from collections.abc import Generator
from enum import Enum, Flag, auto
from pathlib import Path

from .plot import Plot
from .tile import Tile, compress_tile_ids, decompress_tile_ids

## Constants
__all__: tuple[str, ...] = (
    "Gamemode", "GameOptions", "World",
)


## Classes
class World:
    """
    Autonauts World
    - Stores list of plots and tiles as well as settings, flags
    objects, storage, bots, and scripts
    """

    # -Constructor
    def __init__(
            self, name: str, size: tuple[int, int], gamemode: Gamemode, spawn: list[int],
            flags: GameOptions, plots: tuple[Plot, ...]
    ) -> None:
        self.name: str = name
        self.size: tuple[int, int] = size
        self.gamemode: Gamemode = gamemode
        self.spawn: list[int] = spawn
        self.options: GameOptions = flags
        self.plots: tuple[Plot, ...] = plots

    # -Dunder Methods
    def __len__(self) -> int:
        '''Returns count of tiles'''
        return self.size[0] * self.size[1]

    def __getitem__(self, key: tuple[int, int]) -> Tile:
        '''(X,Y) index to plot->tile array relative to world origin'''
        x, y = key
        idx = x // Plot.Width + (y // Plot.Height) * (self.size[0] // Plot.Width)
        return self.plots[idx][x % Plot.Width, y % Plot.Height]

    # -Instance Methods
    def expand_tiles(self) -> Generator[Tile, None, None]:
        '''Expands all plot->tiles into a 1d generator'''
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                yield self[x, y]

    def to_dict(self) -> dict:
        ''''''
        data: dict = {
            'AutonautsWorld': 1,
            'Version': "140.2",
            'External': 0,  # -Always 0
            'GameOptions': {
                'Name': self.name,
                'GameModeName': self.gamemode.value,
                'StartPositionX': self.spawn[0],
                'StartPositionY': self.spawn[1],
                # --Flags
                'BadgeUnlocksEnabled': GameOptions.BadgeUnlocks in self.options,
                'BotLimitEnabled': GameOptions.BotLimit in self.options,
                'BotRechargingEnabled': GameOptions.BotRecharging in self.options,
                'RandomObjectsEnabled': GameOptions.RandomObjects in self.options,
                'RecordingEnabled': GameOptions.Recording in self.options,
                'TutorialEnabled': GameOptions.Tutorial in self.options,
            },
            # --Plots
            'Plots': {
                'PlotsVisible': tuple(int(plot.visible) for plot in self.plots)
            }
        }
        # -Tiles
        _tiles = data['Tiles'] = {
            'TilesHigh': self.size[1],
            'TilesWide': self.size[0],
            'TileTypes': tuple(
                value
                for compressed_id in compress_tile_ids(self.expand_tiles())
                for value in compressed_id
            )
        }
        return data

    def to_file(self, file: Path) -> None:
        ''''''
        pass

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> World:
        ''''''
        # -Options
        _options = data['GameOptions']
        name: str = _options['Name']
        gamemode = Gamemode(_options['GameModeName'])
        spawn: list[int] = [_options['StartPositionX'], _options['StartPositionY']]
        # --Flags
        flags: GameOptions = GameOptions(0)
        if _options['BadgeUnlocksEnabled']:
            flags |= GameOptions.BadgeUnlocks
        if _options['BotLimitEnabled']:
            flags |= GameOptions.BotLimit
        if _options['BotRechargingEnabled']:
            flags |= GameOptions.BotRecharging
        if _options['RandomObjectsEnabled']:
            flags |= GameOptions.RandomObjects
        if _options['RecordingEnabled']:
            flags |= GameOptions.Recording
        if _options['TutorialEnabled']:
            flags |= GameOptions.Tutorial
        # -Tiles
        _tiles = data['Tiles']
        print(len(_tiles['TileTypes']))
        tiles: tuple[Tile, ...] = tuple(
            Tile(_id) for _id in decompress_tile_ids(_tiles['TileTypes'])
        )
        size: tuple[int, int] = (_tiles['TilesWide'], _tiles['TilesHigh'])
        # --Objects
        for obj in data['Objects']:
            pass
        # --Plots
        plots: tuple[Plot, ...] = tuple(
            Plot.from_index(i, size, bool(visible), tiles)
            for i, visible in enumerate(data['Plots']['PlotsVisible'])
        )
        assert (size[0] // Plot.Width) * (size[1] // Plot.Height) == len(plots)
        return cls(name, size, gamemode, spawn, flags, plots)

    @classmethod
    def from_file(cls, file: Path) -> World:
        with file.open('r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    # -Properties
    @property
    def height(self) -> int:
        return self.size[1]

    @property
    def width(self) -> int:
        return self.size[0]


class Gamemode(Enum):
    Creative = "ModeCreative"
    Campaign = "ModeCampaign"


class GameOptions(Flag):
    BadgeUnlocks = auto()
    BotLimit = auto()
    BotRecharging = auto()
    RandomObjects = auto()
    Recording = auto()
    Tutorial = auto()

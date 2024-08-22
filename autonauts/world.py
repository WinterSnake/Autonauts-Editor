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

from .game_object import GameObject
from .player import Player
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
            self, name: str, size: tuple[int, int], gamemode: Gamemode,
            spawn: tuple[int, int], flags: GameOptions, plots: tuple[Plot, ...]
    ) -> None:
        self.name: str = name
        self.size: tuple[int, int] = size
        self.gamemode: Gamemode = gamemode
        self.spawn: tuple[int, int] = spawn
        self.options: GameOptions = flags
        self.plots: tuple[Plot, ...] = plots

    # -Dunder Methods
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
        '''Return a save file compatible dict of the world'''
        # -Compute compressed tile ids
        tiles: list[int] = []
        for compressed_id in compress_tile_ids(self.expand_tiles()):
            tiles.extend(compressed_id)
        return {
            'AutonautsWorld': 1,  # -Always 1
            'Version': "140.2",  # -Latest support only
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
            # --Tiles
            'Tiles': {
                'TilesHigh': self.height,
                'TilesWide': self.width,
                'TileTypes': tuple(tiles)
            },
            # --Plots
            'Plots': {
                'PlotsVisible': tuple(int(plot.visible) for plot in self.plots)
            }
        }

    def to_file(self, file: Path, indent: int | None = None) -> None:
        with file.open('w') as f:
            json.dump(self.to_dict(), f, indent=indent)

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> World:
        '''Load world from expected unpacked json'''
        # -Options
        _options = data['GameOptions']
        name: str = _options['Name']
        gamemode: Gamemode = Gamemode(_options['GameModeName'])
        spawn: tuple[int, int] = (_options['StartPositionX'], _options['StartPositionY'])
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
        size: tuple[int, int] = (_tiles['TilesWide'], _tiles['TilesHigh'])
        tiles: tuple[Tile, ...] = tuple(
            Tile(_id) for _id in decompress_tile_ids(_tiles['TileTypes'])
        )
        assert len(tiles) == size[0] * size[1]
        # --Objects
        for obj in data['Objects']:
            pass
        # --Plots
        plots: tuple[Plot, ...] = tuple(
            Plot.from_index(i, size, bool(visible), tiles)
            for i, visible in enumerate(data['Plots']['PlotsVisible'])
        )
        assert len(plots) == (size[0] // Plot.Width) * (size[1] // Plot.Height)
        return cls(name, size, gamemode, spawn, flags, plots)

    @classmethod
    def from_file(cls, file: Path) -> World:
        with file.open('r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    # -Properties
    @property
    def tile_count(self) -> int:
        return self.width * self.height

    @property
    def height(self) -> int:
        return self.size[1]

    @property
    def width(self) -> int:
        return self.size[0]


class Gamemode(Enum):
    Campaign = "ModeCampaign"
    Creative = "ModeCreative"
    Free = "ModeFree"
    Settlement = "ModeSettlement"


class GameOptions(Flag):
    BadgeUnlocks = auto()
    BotLimit = auto()
    BotRecharging = auto()
    RandomObjects = auto()
    Recording = auto()
    Tutorial = auto()

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
from enum import Enum, Flag, auto
from pathlib import Path

from .plot import Plot
from .tile import Tile, decompress_tile_ids

## Constants
__all__: tupler[str, ...] = (
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
            flags: GameOptions, plots: tuple[Plot]
    ) -> None:
        self.name: str = name
        self.size: tuple[int, int] = size
        self.gamemode: Gamemode = gamemode
        self.spawn: list[int] = spawn
        self.options: GameOptions = flags
        self.plots: tuple[Plot] = plots

    # -Dunder Methods
    def __getitem__(self, key: tuple[int, int]) -> Tile:
        '''(X,Y) index to plot->tile array relative to world origin'''
        x, y = key
        idx = x // Plot.Width + (y // Plot.Height) * (self.size[0] // Plot.Width)
        return self.plots[idx][x % Plot.Width, y % Plot.Height]

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> World:
        ''''''
        # -Game options
        _game_options = data['GameOptions']
        name: str = _game_options['Name']
        gamemode = Gamemode(_game_options['GameModeName'])
        spawn = (_game_options['StartPositionX'], _game_options['StartPositionY'])
        # --Game flags
        game_flags: GameOptions = GameOptions(0)
        if _game_options['BadgeUnlocksEnabled']:
            game_flags |= GameOptions.BadgeUnlocks
        if _game_options['BotLimitEnabled']:
            game_flags |= GameOptions.BotLimit
        if _game_options['BotRechargingEnabled']:
            game_flags |= GameOptions.BotRecharging
        if _game_options['RandomObjectsEnabled']:
            game_flags |= GameOptions.RandomObjects
        if _game_options['RecordingEnabled']:
            game_flags |= GameOptions.Recording
        if _game_options['TutorialEnabled']:
            game_flags |= GameOptions.Tutorial
        # -Tiles
        _tiles = data['Tiles']
        tiles: tuple[Tile] = tuple(
            Tile(_id) for _id in decompress_tile_ids(_tiles['TileTypes'])
        )
        size: tuple[int, int] = (_tiles['TilesWide'], _tiles['TilesHigh'])
        # --Plots
        _plots = data['Plots']['PlotsVisible']
        plots: tuple[Plot, ...] = tuple(
            Plot.from_index(i, size, bool(visible), tiles)
            for i, visible in enumerate(_plots)
        )
        return cls(name, size, gamemode, spawn, game_flags, plots)

    @classmethod
    def from_file(cls, file: Path) -> World:
        with file.open('r') as f:
            data = json.load(f)
        return cls.from_dict(data)


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

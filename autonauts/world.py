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
from typing import cast

from .game_object import GameObject, Player, load_game_object
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
        self, name: str, size: tuple[int, int], seed: int, gamemode: Gamemode,
        spawn: tuple[int, int], flags: GameOptions, plots: tuple[Plot, ...],
        player: Player
    ) -> None:
        self.name: str = name
        self.seed: int = seed
        self.size: tuple[int, int] = size
        self.gamemode: Gamemode = gamemode
        self.spawn: tuple[int, int] = spawn
        self.options: GameOptions = flags
        self.plots: tuple[Plot, ...] = plots
        self.player: Player = player

    # -Dunder Methods
    def __getitem__(self, key: tuple[int, int]) -> Tile:
        '''(X,Y) index to plot->tile array relative to world origin'''
        x, y = key
        idx = x // Plot.Width + (y // Plot.Height) * (self.width // Plot.Width)
        return self.plots[idx][x % Plot.Width, y % Plot.Height]

    # -Instance Methods
    def to_dict(self) -> dict:
        '''Return a save file compatible dict of the world'''
        tiles: list[int] = []
        objects: list[dict] = []
        # -Compute compressed tile ids
        compression_gen = compress_tile_ids()
        next(compression_gen)
        for y in range(self.height):
            for x in range(self.width):
                position = (x, y)
                # -Tile
                tile = self[x, y]
                compressed_id = compression_gen.send(tile)
                if compressed_id:
                    tiles.extend(compressed_id)
                    next(compression_gen)
                # -Objects
                for obj in tile.objects:
                    objects.append(obj.to_dict(position))
        tiles.extend(cast(
            tuple[int, int], compression_gen.send(None), 
        ))
        # -Player | Structures
        objects.append(self.player.to_dict())
        # -World format
        return {
            'AutonautsWorld': 1,  # -Always 1
            'Version': "140.2",  # -Latest support only
            'External': 0,  # -Always 0
            'GameOptions': {
                'Name': self.name,
                'Seed': self.seed,
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
            },
            # --Tiles
            'Tiles': {
                'TilesHigh': self.height,
                'TilesWide': self.width,
                'TileTypes': tuple(tiles)
            },
            # --Objects
            'Objects': tuple(objects)
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
        seed: int = _options['Seed']
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
        player: Player
        for obj in data['Objects']:
            (x, y), _obj = load_game_object(obj)
            if isinstance(_obj, Player):
                player = _obj
                continue
            idx: int = x + y * size[0]
            tiles[idx].objects.append(_obj)
        # --Plots
        plots: tuple[Plot, ...] = tuple(
            Plot.from_index(i, size, bool(visible), tiles)
            for i, visible in enumerate(data['Plots']['PlotsVisible'])
        )
        assert len(plots) == (size[0] // Plot.Width) * (size[1] // Plot.Height)
        return cls(name, size, seed, gamemode, spawn, flags, plots, player)

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

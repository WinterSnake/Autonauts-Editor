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

## Constants
__all__: tupler[str, ...] = ("World",)


## Functions
def parse_game_options(data: dict) -> None:
    """
    """
    gamemode = Gamemode(data['GameModeName'])
    print(gamemode)
    pass


## Classes
class World:
    """
    """

    # -Constructor
    def __init__(self, name: str, gamemode: Gamemode, spawn: tuple[int, int], flags: GameOptions) -> None:
        self.name: str = name
        self.gamemode: Gamemode = gamemode
        self.spawn: tuple[int, int] = spawn
        self.options: GameOptions = flags

    # -Dunder Methods

    # -Instance Methods
    def to_dict(self) -> dict:
        ''''''
        pass

    def to_file(self, file: Path) -> None:
        ''''''
        pass

    # -Class Methods

    # -Static Methods

    # -Properties

    # -Class Properties
    @classmethod
    def from_dict(cls, data: dict) -> World:
        ''''''
        print(data.keys())
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
        return cls(name, gamemode, spawn, game_flags)

    @classmethod
    def from_file(cls, file: Path) -> World:
        with file.open('r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class Gamemode(Enum):
    """
    """

    Creative = "ModeCreative"
    Campaign = "ModeCampaign"


class GameOptions(Flag):
    """
    """

    BadgeUnlocks = auto()
    BotLimit = auto()
    BotRecharging = auto()
    RandomObjects = auto()
    Recording = auto()
    Tutorial = auto()

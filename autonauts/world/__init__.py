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
from pathlib import Path

## Constants
__all__: tupler[str, ...] = ("World",)


## Classes
class World:
    """
    """

    # -Constructor
    def __init__(self) -> None:
        pass

    # -Dunder Methods

    # -Instance Methods

    # -Class Methods

    # -Static Methods

    # -Properties

    # -Class Properties
    @classmethod
    def from_dict(cls, data: dict) -> World:
        ''''''
        pass

    @classmethod
    def from_file(cls, file: Path) -> World:
        with file.open('r') as f:
            data = json.load(f)
        return cls.from_dict(data)

#!/usr/bin/python
##-------------------------------##
## Autonauts Save Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Game Object                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import ClassVar

## Constants
__all__: tuple[str] = ("GameObject",)


## Classes
class GameObject:
    """
    """

    # -Constructor
    def __init__(self, uid: int, _id: str) -> None:
        self.uid: int = uid
        self.id: str = _id

    # -Static Methods
    @staticmethod
    def get_uid() -> int:
        value: int = GameObject.Uid
        GameObject.Uid += 1
        return value

    # -Class Properties
    Uid: ClassVar[int] = 1

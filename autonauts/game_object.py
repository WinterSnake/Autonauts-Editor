#!/usr/bin/python
##-------------------------------##
## Autonauts Save Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Game Object                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from typing import ClassVar, Protocol

## Constants
__all__: tuple[str, ...] = (
    "GameObject", "Player", "Structure",
    "load_game_object"
)


## Functions
def load_game_object(data: dict) -> tuple[tuple[int, int], Player | GameObject]:
    '''
    '''
    position: tuple[int, int] = (data['TX'], data['TY'])
    if data['ID'] == Player.Identifier:
        return (position, Player.from_dict(data))
    obj = GameObject.from_dict(data)
    return (position, obj)


## Classes
## -Objects
class GameObject:
    """
    """

    # -Constructor
    def __init__(
        self, _id: str, uid: int | None = None, *properties: GameObjectProperty
    ) -> None:
        self.uid: int = uid if uid else GameObject.get_uid()
        self.id: str = _id
        self.properties: tuple[GameObjectProperty, ...] = properties

    # -Dunder Methods
    def __repr__(self) -> str:
        if self.properties:
            properties = ", ".join(f"({_property})" for _property in self.properties)
        else:
            properties = None
        return f"GameObject(Id=\"{self.id}\", Uid={self.uid}, Properties={properties})"

    def __str__(self) -> str:
        return self.id

    # -Instance Methods
    def to_dict(self, position: tuple[int, int]) -> dict:
        data = {
            'ID': self.id,
            'UID': self.uid,
            'TX': position[0],
            'TY': position[1],
        }
        for _property in self.properties:
            data.update(_property.to_dict())
        return data

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> GameObject:
        # -Object Modifiers
        properties: list[GameObjectProperty] = []
        if DurabilityProperty.data_has_property(data):
            properties.append(DurabilityProperty.from_dict(data))
        return cls(data['ID'], data['UID'], *properties)

    # -Static Methods
    @staticmethod
    def get_uid() -> int:
        value: int = GameObject.Uid
        GameObject.Uid += 1
        return value

    # -Class Properties
    Uid: ClassVar[int] = 1


class Player:
    """
    A GameObject representing a player and their inventory (hands/backpack/upgrades)
    """

    # -Constructor
    def __init__(
        self, position: tuple[int, int], rotation: int,
        uid: int | None = None, **inventory: list[GameObject]
    ) -> None:
        self.uid: int = uid if uid else GameObject.get_uid()
        self.position: tuple[int, int] = position
        self.rotation: int = rotation
        self.hands: list[GameObject] = inventory['hands'] if 'hands' in inventory else []
        self.backpack: list[GameObject] = inventory['backpack'] if 'backpack' in inventory else []
        self.upgrades: list[GameObject] = inventory['upgrades'] if 'upgrades' in inventory else []

    # -Instance Methods
    def to_dict(self) -> dict:
        data = GameObject(Player.Identifier, self.uid).to_dict(self.position)
        data.update({
            'Rotation': self.rotation,
            # -Hands
            'Carry': {
                'CarryObjects': tuple(
                    item.to_dict(self.position) for item in self.hands
                )
            },
            # -Backpack
            'Inv': {
                'InvObjects': tuple(
                    item.to_dict(self.position) for item in self.backpack
                )
            },
            # -Upgrades
            'Up': {
                'UpgradeObjects': tuple(
                    item.to_dict(self.position) for item in self.upgrades
                )
            },
        })
        return data

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> Player:
        uid: int = data['UID']
        position: tuple[int, int] = (data['TX'], data['TY'])
        rotation: int = data['Rotation']
        inventory = {
            'hands': [
                GameObject.from_dict(_data)
                for _data in data['Carry']['CarryObjects']
            ],
            'backpack': [
                GameObject.from_dict(_data)
                for _data in data['Inv']['InvObjects'] if _data['ID']
            ],
            'upgrades': [
                GameObject.from_dict(_data)
                for _data in data['Up']['UpgradeObjects'] if _data['ID']
            ]
        }
        return cls(position, rotation, uid, **inventory)

    # -Properties
    @property
    def x(self) -> int:
        return self.position[0]

    @x.setter
    def x(self, value: int) -> None:
        self.position = (value, self.position[1])

    @property
    def y(self) -> int:
        return self.position[1]

    @y.setter
    def y(self, value: int) -> None:
        self.position = (self.position[0], value)

    # -Class Properties
    Identifier: ClassVar[str] = "FarmerPlayer"


## -Properties
class GameObjectProperty(Protocol):
    # -Instance Methods
    def to_dict(self) -> dict: ...
    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> GameObjectProperty: ...
    # -Static Methods
    @staticmethod
    def data_has_property(data: dict) -> bool: ...


class DurabilityProperty(GameObjectProperty):
    """Game Object Property for items with durability/usage counters"""
    # -Constructor
    def __init__(self, durability: int) -> None:
        self.durability: int = durability

    # -Dunder Method
    def __repr__(self) -> str:
        return f"Uses={self.durability}"

    # -Instance Methods
    def to_dict(self) -> dict:
        return { 'Used': self.durability }

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> DurabilityProperty:
        return cls(data['Used'])

    # -Static Methods
    @staticmethod
    def data_has_property(data: dict) -> bool:
        return 'Used' in data

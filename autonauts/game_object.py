#!/usr/bin/python
##-------------------------------##
## Autonauts Save Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Game Object                   ##
##-------------------------------##

## Imports
from __future__ import annotations
from enum import IntEnum
from typing import ClassVar, Protocol

## Constants
__all__: tuple[str, ...] = (
    "GameObject", "Player", "Structure",
    "GameObjectProperty", "DurabilityProperty", "StageProperty",
    "TreeProperty", "FlowerProperty"
    "load_game_object"
)


## Functions
def load_game_object(data: dict) -> tuple[tuple[int, int], Player | Structure | GameObject]:
    """Load a dict as a game object and return its position"""
    position: tuple[int, int] = (data['TX'], data['TY'])
    if data['ID'] == Player.Identifier:
        return (position, Player.from_dict(data))
    obj = GameObject.from_dict(data)
    return (position, obj)


## Classes
## -Objects
class GameObject:
    """
    An object in the game by a given position (attached to a tile) and properties
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
        # -Object Properties
        properties: list[GameObjectProperty] = []
        for property_check in PROPERTY_CHECKS:
            if property_check.data_has_property(data):
                properties.append(property_check.from_dict(data))
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
    A GameObject representing a player and their inventory (hands/backpack/upgrades/clothes)
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
        self.clothes: list[GameObject] = inventory['clothes'] if 'clothes' in inventory else []

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
            # -Clothes
            'Clothes': {
                'ClothesObjects': tuple()
            }
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


class Structure:
    """
    """

    # -Constructor
    def __init__(self) -> None:
        pass

    # -Class Properties
    Identifiers: ClassVar[tuple[str, ...]] = ("",)

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
    """Game Object Durability Property: uses"""
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


class StageProperty(GameObjectProperty):
    """Game Object Stage Property: stage and stage timer"""
    # -Constructor
    def __init__(self, stage: int, timer: int) -> None:
        self.stage: int = stage
        self.timer: int = timer

    # -Dunder Method
    def __repr__(self) -> str:
        return f"Stage={self.stage};Time={self.timer}"

    # -Instance Methods
    def to_dict(self) -> dict:
        return { 'ST': self.stage, 'STT': self.timer }

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> StageProperty:
        stage: int = data['ST']
        timer: int = data['STT']
        return cls(stage, timer)

    # -Static Methods
    @staticmethod
    def data_has_property(data: dict) -> bool:
        return 'ST' in data and 'STT' in data


class TreeProperty(GameObjectProperty):
    """Game Object Tree Property: <unknown> and bees"""
    # -Constructor
    def __init__(self, bee_uid: int | None) -> None:
        self.bee_uid: int | None = bee_uid

    # -Dunder Method
    def __repr__(self) -> str:
        return f"Bees={self.bee_uid}"

    # -Instance Methods
    def to_dict(self) -> dict:
        data: dict = { 'SL': 0 }  # -Unknown property
        if self.bee_uid is not None:
            data[TreeProperty.BeesKey] = {
                'ID': TreeProperty.BeesKey,
                'UID': self.bee_uid,
                'TX': 0,
                'TY': 0,
            }
        return data

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> TreeProperty:
        unknown: int = data['SL']
        bee_uid: int | None = None
        if TreeProperty.BeesKey in data:
            bee_uid = data[TreeProperty.BeesKey]['UID']
        return cls(bee_uid)

    # -Static Methods
    @staticmethod
    def data_has_property(data: dict) -> bool:
        return 'SL' in data

    # -Class Properties
    BeesKey: ClassVar[str] = "BeesNest"


class FlowerProperty(GameObjectProperty):
    """Game Object Flower Property: type"""
    # -Constructor
    def __init__(self, _type: FlowerProperty.Type) -> None:
        self.type: FlowerProperty.Type = _type

    # -Dunder Method
    def __repr__(self) -> str:
        return f"Type={self.type.name}"

    # -Instance Methods
    def to_dict(self) -> dict:
        return { 'Type': self.type.value }

    # -Class Methods
    @classmethod
    def from_dict(cls, data: dict) -> FlowerProperty:
        return cls(FlowerProperty.Type(data['Type']))

    # -Static Methods
    @staticmethod
    def data_has_property(data: dict) -> bool:
        return 'Type' in data

    # -Sub-Classes
    class Type(IntEnum):
        Aster = 0
        Tulip = 1
        Delphinium = 2
        Primrose = 3
        Rose = 4
        Gladioli = 5
        Chamomile = 6


## Body
PROPERTY_CHECKS: tuple[type[GameObjectProperty], ...] = (
    DurabilityProperty, StageProperty, TreeProperty, FlowerProperty
)

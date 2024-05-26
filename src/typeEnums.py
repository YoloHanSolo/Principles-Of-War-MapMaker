from enum import Enum


class UnitType(Enum):
    MOTORIZED = "motorized"
    INFANTRY = "infantry"
    LEADER = "leader"
    FORTIFICATION = "fortification"
    NAVAL = "naval"
    LIGHT_INFANTRY = "light_infantry"


class TerrainType(Enum):
    GRASS = "grass"
    FOREST = "forest"
    MUD = "mud"
    SAND = "sand"
    SNOW = "snow"
    MOUNTAIN = "mountain"
    WATER = "water"


class LandmarkType(Enum):
    DEFAULT = "default"
    CITY = "city"
    OILFIELD = "oilfield"
    SUPPLY = "supply"
from src.types.enums import UnitType, TerrainType, LandmarkType


class MapObject:

    def __init__(self) -> None:
        self.data = {
            "metadata": {
                "id": "",
                "name": "",
                "filename": "",
                "hash": "",
                "width": 0,
                "height": 0,
                "timestamp": "",
                "creator": "",
                "version": "",
                "type": "",
                "description": "",
            },
            "factions": {},
            "hexagons": [],
            "landmarks": {
                "city": [],
                "oilfield": [],
                "supply": [],
            },
            "time": {"day": 0, "month": 0, "year": 0, "increment": 0, "seasons": {}},
            "turn": {"duration": 0},
            "unit_types": {},
            "units": [],
            "unit_icons": {},
        }

    def create_unit_type(
        self,
        id,
        name,
        description,
        faction,
        branch,
        icon,
        attack,
        defense,
        movement,
        cost,
        fuel_consumption,
        frequency,
    ):

        if faction not in self.data["factions"]:
            print(f"[ERROR] create_unit_type: faction '{faction}' does not exist")
            return

        if branch not in {unit_type.value for unit_type in UnitType}:
            print(f"[ERROR] create_unit_type: invalid branch '{branch}'")
            return

        if icon not in self.data["unit_icons"]:
            print(f"[WARN] create_unit_type: unit icon '{icon}' does not exist")
            print(
                f"[WARN] create_unit_type: unit icon '{icon}' fallback to 'unknown.png'"
            )
            self.create_unit_icon(icon, self.data["unit_icons"]["unknown"])

        self.data["unit_types"][id] = {
            "id": id,
            "name": name,
            "description": description,
            "faction": faction,
            "branch": branch,
            "icon": icon,
            "attack": attack,
            "defense": defense,
            "movement": movement,
            "cost": cost,
            "fuel_consumption": fuel_consumption,
            "frequency": frequency,
        }

    def create_unit_icon(self, icon_key, icon_value):
        self.data["unit_icons"][icon_key] = icon_value

    def create_unit(self, x, y, faction, unit_type, attack, defense, movement):

        if x < 0 or x >= self.data["metadata"]["width"]:
            print(f"[ERROR] create_unit: unit coordinate x '{x}' out of bounds")
            return

        if y < 0 or y >= self.data["metadata"]["height"]:
            print(f"[ERROR] create_unit: unit coordinate y '{y}' out of bounds")
            return

        if faction not in self.data["factions"]:
            print(f"[ERROR] create_unit: faction '{faction}' does not exist")
            return

        if unit_type not in self.data["unit_types"]:
            print(self.data["unit_types"])
            print(f"[ERROR] create_unit: unit type '{unit_type}' does not exist")
            return

        self.data["units"].append(
            {
                "x": x,
                "y": y,
                "faction": faction,
                "type": unit_type,
                "attack": attack,
                "defense": defense,
                "movement": movement,
            }
        )

    def create_faction(
        self,
        id,
        name,
        units_cap,
        manpower_points,
        manpower_cap,
        manpower_income,
        fuel_points,
        fuel_cap,
        fuel_income,
        airpower_points,
        airpower_cap,
        airpower_income,
    ):

        self.data["factions"][name] = {
            "id": id,
            "name": name,
            "units": {"cap": units_cap},
            "manpower": {
                "points": manpower_points,
                "income": manpower_income,
                "cap": manpower_cap,
            },
            "fuel": {"points": fuel_points, "income": fuel_income, "cap": fuel_cap},
            "airpower": {
                "points": airpower_points,
                "income": airpower_income,
                "cap": airpower_cap,
            },
        }

    def create_landmark(self, landmark_type, x, y, **kwargs):

        if x < 0 or x >= self.data["metadata"]["width"]:
            print(f"[ERROR] create_landmark: landmark coordinate x '{x}' out of bounds")
            return

        if y < 0 or y >= self.data["metadata"]["height"]:
            print(f"[ERROR] create_landmark: landmark coordinate y '{y}' out of bounds")
            return

        if landmark_type not in {landmark_type.value for landmark_type in LandmarkType}:
            print(f"[ERROR] create_landmark: invalid landmark type '{landmark_type}'")
            return

        match landmark_type:
            case LandmarkType.CITY.value:
                if (
                    "faction" not in kwargs
                    or "name" not in kwargs
                    or "population" not in kwargs
                ):
                    print(f"[ERROR] create_landmark: city: missing parameters")
                    return

                if (
                    kwargs["faction"] != "neutral"
                    and kwargs["faction"] not in self.data["factions"]
                ):
                    print(
                        f"[ERROR] create_landmark: city: faction '{kwargs['faction']}' does not exist"
                    )
                    return

                self.data["landmarks"]["city"].append(
                    {
                        "x": x,
                        "y": y,
                        "name": kwargs["name"],
                        "faction": kwargs["faction"],
                        "population": kwargs["population"],
                    }
                )
            case LandmarkType.OILFIELD.value:
                if "production" not in kwargs:
                    print(f"[ERROR] create_landmark: oilfield: missing parameters")
                    return

                self.data["landmarks"]["oilfield"].append(
                    {
                        "x": x,
                        "y": y,
                        "production": kwargs["production"],
                    }
                )
            case LandmarkType.SUPPLY.value:
                if "faction" not in kwargs:
                    print(f"[ERROR] create_landmark: supply: missing parameters")
                    return

                if (
                    kwargs["faction"] != "neutral"
                    and kwargs["faction"] not in self.data["factions"]
                ):
                    print(
                        f"[ERROR] create_landmark: supply: faction '{kwargs['faction']}' does not exist"
                    )
                    return

                self.data["landmarks"]["supply"].append(
                    {
                        "x": x,
                        "y": y,
                        "faction": kwargs["faction"],
                    }
                )
            case _:
                print(
                    f"[ERROR] create_landmark: invalid landmark type '{landmark_type}'"
                )
                return

    def create_time(self, day, month, year, increment, seasons=None):
        if not seasons:
            print(f"[WARN] create_time: seasons missing")
        else:
            try:
                for key, value in seasons.items():
                    season_day, season_month = key.split("-")
                    if not (1 <= int(season_day) <= 31):
                        raise
                    if not (1 <= int(season_month) <= 12):
                        raise
                    for key2, value2 in value.items():
                        if key2 not in {
                            terrain_type.value for terrain_type in TerrainType
                        }:
                            raise
                        if not ("probability" in value2 and "to" in value2):
                            raise
            except:
                print(f"[ERROR] create_time: invalid seasons data")
                seasons = None

        self.data["time"] = {
            "day": day,
            "month": month,
            "year": year,
            "increment": increment,
            "seasons": seasons,
        }

    def create_hexagon(
        self,
        x,
        y,
        terrain,
        faction,
        landmark_type="default",
        railway=False,
        river=[False, False, False, False, False, False],
        port=False,
        objective_f0=False,
        objective_f1=False,
    ):

        if terrain not in {terrain_type.value for terrain_type in TerrainType}:
            print(f"[ERROR] create_hexagon: invalid terrain '{terrain}'")
            return

        if faction != "neutral" and faction not in self.data["factions"]:
            print(f"[ERROR] create_hexagon: faction '{faction}' does not exist")
            return

        if landmark_type not in {landmark_type.value for landmark_type in LandmarkType}:
            print(f"[ERROR] create_hexagon: invalid landmark type '{landmark_type}'")
            return

        self.data["hexagons"].append(
            {
                "x": x,
                "y": y,
                "terrain": terrain,
                "faction": faction,
                "landmark": landmark_type,
                "railway": railway,
                "river": river,
                "port": port,
                "objective": {"faction_0": objective_f0, "faction_1": objective_f1},
            }
        )

    def create_turn(self, duration):
        self.data["turn"]["duration"] = duration

    def create_metadata(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.data["metadata"]:
                print(f"[ERROR] create_metadata: invalid metadata key '{key}'")
                continue
            self.data["metadata"][key] = value

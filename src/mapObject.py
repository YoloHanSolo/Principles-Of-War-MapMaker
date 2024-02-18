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
                "version": 2,
                "type": ""
            },
            "factions": {},
            "hexagons": [],
            "landmarks": {
                "city": [],
                "oilfield": [],
                "supply": [],
            },
            "time": {
                "day": 0,
                "month": 0,
                "year": 0,
                "increment": 0,
                "seasons": {}
            },
            "turn": {
                "duration": 0
            },
            "unit_types": {},
            "units": [],
            "unit_icons": {}
        }

    def createUnitType(self, 
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
            frequency):
        
        if faction not in self.data["factions"]:
            print(f"ERROR: createUnitType: faction '{faction}' does not exist")
            return 

        if branch not in ["fortification", "infantry", "mechanized", "naval", "light_infantry"]:
            print(f"ERROR: createUnitType: invalid branch '{branch}'")
            return
        
        if icon not in self.data["unit_icons"]:
            print(f"ERROR: createUnitType: unit icon '{icon}' does not exist")
            return

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
            "frequency": frequency
        }

    def createUnitIcon(self, icon_key, icon_value):
        self.data["unit_icons"][icon_key] = icon_value

    def createUnit(self, x, y, faction, unit_type, attack, defense, movement):

        if x < 0 or x >= self.data["metadata"]["width"]:
            print(f"ERROR: createUnit: unit coordinate x '{x}' out of bounds")
            return

        if y < 0 or y >= self.data["metadata"]["height"]:
            print(f"ERROR: createUnit: unit coordinate y '{y}' out of bounds")
            return

        if faction not in self.data["factions"]:
            print(f"ERROR: createUnit: faction '{faction}' does not exist")
            return 
        
        if unit_type not in self.data["unit_types"]:
            print(f"ERROR: createUnit: unit type '{unit_type}' does not exist")
            return 

        self.data["units"].append({
            "x": x,
            "y": y,
            "faction": faction,
            "type": unit_type,
            "attack": attack,
            "defense": defense,
            "movement": movement
        })

    def createFaction(self, 
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
            airpower_income):
        
        self.data["factions"][name] = {
            "id": id,
            "name": name,
            "units": {
                "cap": units_cap
            },
            "manpower": {
                "points": manpower_points,
                "income": manpower_income,
                "cap": manpower_cap
            },
            "fuel": {
                "points": fuel_points,
                "income": fuel_income,
                "cap": fuel_cap
            },
            "airpower": {
                "points": airpower_points,
                "income": airpower_income,
                "cap": airpower_cap
            }
        }

    def createLandmark(self, landmark_type, x, y, **kwargs):

        if x < 0 or x >= self.data["metadata"]["width"]:
            print(f"ERROR: createLandmark: landmark coordinate x '{x}' out of bounds")
            return

        if y < 0 or y >= self.data["metadata"]["height"]:
            print(f"ERROR: createLandmark: landmark coordinate y '{y}' out of bounds")
            return
        
        if landmark_type not in ["city", "oilfield", "supply"]:
            print(f"ERROR: createLandmark: invalid landmark type '{landmark_type}'")
            return

        match landmark_type:
            case "city":
                if "faction" not in kwargs or "name" not in kwargs or "population" not in kwargs:
                    print(f"ERROR: createLandmark: city: missing parameters")
                    return                     

                if kwargs["faction"] != "neutral" and kwargs["faction"] not in self.data["factions"]:
                    print(f"ERROR: createLandmark: city: faction '{kwargs['faction']}' does not exist")
                    return 

                self.data["landmarks"]["city"].append({
                    "x": x,
                    "y": y,
                    "name": kwargs["name"],
                    "faction": kwargs["faction"],
                    "population": kwargs["population"]
                })
            case "oilfield":
                if "production" not in kwargs:
                    print(f"ERROR: createLandmark: oilfield: missing parameters")
                    return   

                self.data["landmarks"]["oilfield"].append({
                    "x": x,
                    "y": y,
                    "production": kwargs["production"],
                })                
            case "supply":
                if "faction" not in kwargs:
                    print(f"ERROR: createLandmark: supply: missing parameters")
                    return   

                if kwargs["faction"] != "neutral" and kwargs["faction"] not in self.data["factions"]:
                    print(f"ERROR: createLandmark: supply: faction '{kwargs['faction']}' does not exist")
                    return 

                self.data["landmarks"]["supply"].append({
                    "x": x,
                    "y": y,
                    "faction": kwargs["faction"],
                })                 
            case _:
                print(f"ERROR: createLandmark: invalid landmark type '{landmark_type}'")
                return
            
    def createTime(self, day, month, year, increment, seasons=None):
        if not seasons:
            print(f"WARNING: createTime: seasons missing")
            return    

        self.data["time"] = {
            "day": day,
            "month": month,
            "year": year,
            "increment": increment,
            "seasons": seasons
        }

    def createHexagon(self, 
            x, 
            y, 
            terrain, 
            faction, 
            landmark_type="default", 
            railway=False, 
            river=[False, False, False, False, False, False], 
            port=False, 
            objective_f0=False, 
            objective_f1=False):

        if terrain not in ["grass", "sand", "mountain", "water", "mud", "snow", "forest"]:
            print(f"ERROR: createHexagon: invalid terrain '{terrain}'")
            return 

        if faction != "neutral" and faction not in self.data["factions"]:
            print(f"ERROR: createHexagon: faction '{faction}' does not exist")
            return 

        if landmark_type not in ["default", "city", "oilfield", "supply"]:
            print(f"ERROR: createHexagon: invalid landmark type '{landmark_type}'")
            return 

        self.data["hexagons"].append({
            "x": x,
            "y": y,
            "terrain": terrain,
            "faction": faction,
            "landmark": landmark_type,
            "railway": railway,
            "river": river,
            "port": port,
            "objective": {
                "faction_0": objective_f0,
                "faction_1": objective_f1
            }
        })

    def createTurn(self, duration):
        self.data["turn"]["duration"] = duration

    def createMetadata(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.data["metadata"]:
                print(f"ERROR: createMetadata: invalid metadata key '{key}'")
                continue 
            self.data["metadata"][key] = value

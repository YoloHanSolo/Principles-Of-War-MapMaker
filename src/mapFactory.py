from os import listdir
from json import load, dump, dumps
from base64 import b64encode
from sys import exit, argv
from time import time
from hashlib import md5
from xml.etree import ElementTree
from mapObject import MapObject

cy = None
cx = None

class MapFactory:

    def __init__(self, map_id):

        self.map = MapObject()

        self.path = f"../mapsData/{map_id}/"

        try: 
            self.tree_root = ElementTree.parse(self.path + "map.tmx").getroot()
        except:
            print(f"ERROR: error when parsing ../mapsData/{map_id}/map.tmx")
            exit()

        try:
            metadata = self.getXmlElement("objectgroup", "metadata").find("properties")
        except:
            print(f"ERROR: missing or invalid 'metadata' layer in ../mapsData/{map_id}/map.tmx")
            exit()

        factions_data = load(open(self.path + "factions.json")) 
        unit_types = load(open(self.path + "unit_types.json", 'r'))
        units_data = load(open(self.path + "units.json")) 
        time_data = load(open(self.path + "time.json")) 
        turn_data = load(open(self.path + "turn.json"))
        landmark_detail_data = load(open(self.path + "landmarks.json"))

        terrain_data = self.getXmlArray("layer", "terrain", 1)
        front_data = self.getXmlArray("layer", "front", 8)
        landmark_data = self.getXmlArray("layer", "landmark", 11)
        railway_data = self.getXmlArray("layer", "railway", 15)
        river_data = self.getXmlArray("layer", "river", 17)
        port_data = self.getXmlArray("layer", "port", 27)
        obj_f0_data = self.getXmlArray("layer", "objective_faction_0", 25)
        obj_f1_data = self.getXmlArray("layer", "objective_faction_1", 25)

        self.map.createMetadata(id=self.getXmlProperties(metadata, "id"))
        self.map.createMetadata(filename=self.getXmlProperties(metadata, "filename"))
        self.map.createMetadata(name=self.getXmlProperties(metadata, "name"))
        self.map.createMetadata(creator=self.getXmlProperties(metadata, "creator"))
        self.map.createMetadata(width=int(self.tree_root.attrib["width"]))
        self.map.createMetadata(height=int(self.tree_root.attrib["height"]))
        self.map.createMetadata(type="original")

        self.map.createTime(**time_data)
        self.map.createTurn(**turn_data)     

        for faction in factions_data.values():
            self.map.createFaction(**faction)

        for filename in listdir(self.path + "unitIcons"):
            if not filename.endswith(".png"):
                continue
            with open(self.path + "unitIcons/" + filename, "rb") as icon:
                icon_binary = icon.read()
                self.map.createUnitIcon(filename[:-4], b64encode(icon_binary).decode('utf-8'))
        
        for unit_type in unit_types.values():
            self.map.createUnitType(**unit_type)

        for unit in units_data:
            self.map.createUnit(**unit)   

        for y in range(self.map.data["metadata"]["height"]):
            for x in range(self.map.data["metadata"]["width"]):
                global cx
                global cy
                cx = x
                cy = y
                self.map.createHexagon(x, y,
                    self.getTerrainByValue(terrain_data[y][x]),
                    self.getFactionByValue(front_data[y][x]),
                    self.getLandmarkByValue(landmark_data[y][x]),
                    self.getRailwayByValue(railway_data[y][x]),
                    self.getRiverByValue(river_data[y][x]),
                    self.getPortByValue(port_data[y][x]),
                    self.getObjectiveByValue(obj_f0_data[y][x]),
                    self.getObjectiveByValue(obj_f1_data[y][x]))

        for city in landmark_detail_data["city"]:
            self.map.createLandmark(landmark_type="city", **city)
        for oilfield in landmark_detail_data["oilfield"]:
            self.map.createLandmark(landmark_type="oilfield", **oilfield)
        for supply in landmark_detail_data["supply"]:
            self.map.createLandmark(landmark_type="supply", **supply)

        hash = md5(dumps(self.map.data, sort_keys=True).encode('utf8')).hexdigest()
        self.map.createMetadata(hash=hash)
        self.map.createMetadata(timestamp=int(time()))

    def getXmlProperties(self, properties, key):
        for property in properties.findall('property'):
            if property.attrib.get('name') == key:
                return property.attrib.get('value')
        print(f"WARNING: getXmlProperties: could not find property with name '{key}'")
        return ""
    
    def getXmlElement(self, tag, name):
        for child in self.tree_root:
            if child.tag == tag and child.attrib["name"] == name:
                return child

    def getXmlArray(self, tag, name, value_offset):
        for child in self.tree_root:
            if child.tag == tag and child.attrib["name"] == name:
                data = child.find('data').text
                return [[(int(num) - value_offset) for num in row.split(',') if num] for row in data.strip().split('\n')]

    def getTerrainByValue(self, value):
        match value:
            case 0:
                return "grass"    
            case 1:
                return "water"
            case 2:
                return "mountain"
            case 3:
                return "sand"
            case 4:
                return "mud"
            case 5:
                return "snow"
            case 6:
                return "forest"
            case _:
                print(f"ERROR: getTerrainByValue: invalid terrain value {value} (y={cy}, x={cx})")

    def getFactionByValue(self, value):
        match value:
            case 0:
                return "neutral"    
            case 1:
                for dict_value in self.map.data["factions"].values():
                    if dict_value.get("id") == "faction_0":
                        return dict_value.get("name")
            case 2:
                for dict_value in self.map.data["factions"].values():
                    if dict_value.get("id") == "faction_1":
                        return dict_value.get("name")
            case _:
                print(f"ERROR: getFactionByValue: invalid faction value {value} (y={cy}, x={cx})")

    def getLandmarkByValue(self, value):
        match value:
            case 0:
                return "default"    
            case 1:
                return "city"
            case 2:
                return "supply"
            case 3:
                return "oilfield"
            case _:
                print(f"ERROR: getLandmarkByValue: invalid landmark value {value} (y={cy}, x={cx})")

    def getRailwayByValue(self, value):
        match value:
            case 0:
                return True   
            case 1:
                return False
            case _:
                print(f"ERROR: getRailwayByValue: invalid railway value {value} (y={cy}, x={cx})")

    def getRiverByValue(self, value):
        match value:
            case 0:
                return [False, False, False, False, False, False]
            case 1:
                return [True, False, False, False, False, False]
            case 2:
                return [False, True, False, False, False, False]
            case 3:
                return [False, False, True, False, False, False]
            case 4:
                return [True, True, False, False, False, False]
            case 5:
                return [True, False, True, False, False, False]
            case 6:
                return [False, True, True, False, False, False]
            case 7:
                return [True, True, True, False, False, False]
            case _:
                print(f"ERROR: getRiverByValue: invalid river value {value} (y={cy}, x={cx})")

    def getObjectiveByValue(self, value):
        match value:
            case 0:
                return False   
            case 1:
                return True
            case _:
                print(f"ERROR: getObjectiveByValue: invalid objective value {value} (y={cy}, x={cx})")

    def getPortByValue(self, value):
        match value:
            case 0:
                return False   
            case 1:
                return True
            case _:
                print(f"ERROR: getPortByValue: invalid port value {value} (y={cy}, x={cx})")

if __name__ == "__main__":
    if len(argv) == 1:
        map_id = input("Enter map_id: ")
    else:
        map_id = argv[1]

    if map_id not in listdir("../mapsData"):
        print(f"ERROR: invalid map id '{map_id}'")
        exit()

    map_factory = MapFactory(map_id)
    filename = map_factory.map.data["metadata"]["filename"]
    with open("../maps/" + filename, 'w+') as file:
        dump(map_factory.map.data, file)
        print(f"INFO: output '../maps/{filename}")

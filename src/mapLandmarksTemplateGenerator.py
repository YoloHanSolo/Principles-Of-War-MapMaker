from json import dump
from xml.etree import ElementTree
from sys import argv, exit
from os import listdir, path


if __name__ == "__main__":

    if len(argv) == 1:
        map_id = input("Enter map_id: ")
    else:
        map_id = argv[1]

    if map_id not in listdir("../mapsData"):
        print(f"ERROR: invalid map id '{map_id}'")
        exit()

    if path.exists(f"../mapsData/{map_id}/landmarks.json"):
        print(f"ERROR: '../mapsData/{map_id}/landmarks.json' already exists")
        exit()

    tree_root = None
    try: 
        tree_root =  ElementTree.parse(f"../mapsData/{map_id}/map.tmx").getroot()
    except:
        print(f"ERROR: error when parsing '../mapsData/{map_id}/map.tmx'")
        exit()

    xml_element = None
    for child in tree_root:
        if child.tag == "layer" and child.attrib["name"] == "landmark":
            xml_element = child.find('data').text
            break

    if not xml_element:
        print("ERROR: xml_element is None")
        exit()    

    output = {
        "city": [],
        "supply": [],
        "oilfield": []
    }

    try:    
        width = int(tree_root.attrib["width"])
        height = int(tree_root.attrib["height"])

        for y, line in enumerate(xml_element.splitlines()[1:]):
            for x, element in enumerate(line.split(",")[:width]):
                match element:
                    case "11":
                        continue
                    case "12":
                        output["city"].append({
                            "x": x,
                            "y": y,
                            "name": "CITY_NAME",
                            "faction": "FACTION",
                            "population": 0
                        })
                    case "13":
                        output["supply"].append({
                            "x": x,
                            "y": y,
                            "faction": "FACTION"
                        })
                    case "14":
                        output["oilfield"].append({
                            "x": x,
                            "y": y,
                            "production": 0
                        })
    except:
        print(f"ERROR: failed to create landmarks.json template")
        exit()    

    with open(f"../mapsData/{map_id}/landmarks.json", 'w+') as file:
        dump(output, file)

    print(f"INFO: template generated '../mapsData/{map_id}/landmarks.json'")
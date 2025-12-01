from os import listdir, path
from json import load
from inquirer import List, prompt
from PIL import Image, ImageFont, ImageDraw

BASE_DIR = path.dirname(path.abspath(__file__))
ROOT_DIR = path.abspath(path.join(BASE_DIR, ".."))
MAPS_DIR = path.join(ROOT_DIR, "maps")
MAPS_DATA_DIR = path.join(ROOT_DIR, "maps_data")
RESOURCES_DIR = path.join(ROOT_DIR, "resources")


class MapPreview:

    def __init__(self, map_id, day):
        self.map_id = map_id
        self.day = day

        self.hexagons = []
        self.cities = []

        self.hexagon_w = 0
        self.hexagon_h = 0
        self.pixel_w = 0
        self.pixel_h = 0

        self.images = {"terrain": {}, "landmark": {}, "river": []}

        self.river_map = [
            [False, False, False, False, False, False],
            [True, False, False, False, False, False],
            [False, True, False, False, False, False],
            [False, False, True, False, False, False],
            [True, True, False, False, False, False],
            [True, False, True, False, False, False],
            [False, True, True, False, False, False],
            [True, True, True, False, False, False],
        ]

    def load_terrain_images(self):
        for image_filename in listdir(path.join(RESOURCES_DIR, "terrain")):
            image = Image.open(
                path.join(RESOURCES_DIR, "terrain", image_filename)
            ).convert("RGBA")
            key = image_filename[:-4]
            self.images["terrain"][key] = image

        for image_filename in listdir(path.join(RESOURCES_DIR, "landmark")):
            image = Image.open(
                path.join(RESOURCES_DIR, "landmark", image_filename)
            ).convert("RGBA")
            key = image_filename[:-4]
            self.images["landmark"][key] = image

        for image_filename in listdir(path.join(RESOURCES_DIR, "river")):
            image = Image.open(
                path.join(RESOURCES_DIR, "river", image_filename)
            ).convert("RGBA")
            self.images["river"].append(image)

    def load_map_data(self):
        with open(f"{MAPS_DIR}/{self.map_id}.json", "r") as file:
            data = load(file)
        self.hexagons = data["hexagons"]
        self.cities = data["landmarks"]["city"]
        self.hexagon_w = data["metadata"]["width"]
        self.hexagon_h = data["metadata"]["height"]
        self.pixel_w = self.hexagon_w * 120 + 60
        self.pixel_h = self.hexagon_h * 107 + 33

    def generate_preview(self):

        canvas = Image.new("RGBA", (self.pixel_w, self.pixel_h), (0, 0, 0, 0))

        draw = ImageDraw.Draw(canvas)

        font = ImageFont.truetype("arial.ttf", 40)

        for hexagon in self.hexagons:
            ix = hexagon["x"]
            iy = hexagon["y"]
            terrain = hexagon["terrain"]
            landmark = hexagon["landmark"]
            river = hexagon["river"]

            px = ix * 120 + (iy % 2) * 60
            py = iy * 107

            river_index = 0

            for i in range(8):
                if not all(x == y for x, y in zip(river, self.river_map[i])):
                    continue
                river_index = i
                break

            canvas.paste(
                self.images["terrain"][terrain],
                (px, py),
                self.images["terrain"][terrain],
            )

            if landmark != "default":
                canvas.paste(
                    self.images["landmark"][landmark],
                    (px, py),
                    self.images["landmark"][landmark],
                )

            if river_index > 0:
                canvas.paste(
                    self.images["river"][river_index],
                    (px, py),
                    self.images["river"][river_index],
                )

        for city in self.cities:
            ix = city["x"]
            iy = city["y"]
            name = city["name"]

            bbox = draw.textbbox((0, 0), name, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            px = ix * 120 + (iy % 2) * 60 + 60 - text_w // 2
            py = iy * 107

            draw.rectangle(
                (px, py + 80, px + text_w, py + 80 + text_h + 10),
                fill=(0, 0, 0, 255),
            )
            draw.text((px, py + 80), name, fill=(255, 255, 255, 255), font=font)

        canvas.save(path.join(MAPS_DATA_DIR, self.map_id, "preview.png"))


def run():

    values = prompt(
        [
            List("map_id", "map", listdir(MAPS_DATA_DIR)),
        ]
    )

    map_id = values["map_id"]

    map_preview = MapPreview(map_id, 0)
    map_preview.load_terrain_images()
    map_preview.load_map_data()
    map_preview.generate_preview()

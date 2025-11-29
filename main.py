from sys import exit
from os import listdir
from inquirer import List, prompt
from src.mapFactory import run as mapCompile

commands = [
    {
        "name": "mapCompile",
        "fun": mapCompile
    },
]

if __name__ == "__main__":

    values = prompt([
        List(
            "command",
            "command"
        ),
        List(
            "map_id",
            "map",
            listdir("../mapsData")
        ),
    ])

    map_id = values["map_id"]
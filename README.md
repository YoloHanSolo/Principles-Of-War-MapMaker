# Principles Of War - Map Maker

Welcome to the Map Maker Instructions for Principles Of War! This guide will help you create and customize maps for our game. Follow these steps to get started:

## Getting Started

For creating maps we use a combination of Tiled map maker software, data stored in .json files and .png hexagon icons.
   
1. **Tiled**: For creating maps layers such as terrain we use free software [Tiled Level Editor](https://www.mapeditor.org/).
2. **Json Files**: You can edit .json files with any text editor. We use [VSCode](https://code.visualstudio.com/download).
3. **PNG Icons**: Use any tool that can create transparent background. We use [Paint.NET](https://www.getpaint.net/download.html).

## Required Files

1. **Create a new folder for your map in './mapsData' and name it same as your <MAP_ID>**
2. **Inside create new folder'./mapsData/<MAP_ID/unitIcons' and put your .PNG unit icons there** 
3. **Add following files inside your map folder:**
    - **map.tmx** (created with Tiled Level Editor)
    - **factions.json**
    - **landmarks.json**
    - **time.json**
    - **turn.json**
    - **unit_types.json**
    - **units.json**
4. **Inspect and learn from existing maps in './mapsData/...' folder**

## Build your map file

Run 'src/mapFactory.py' to create a single .json file which packs all map data. Output is generated in './maps' folder.

## Publish your map

Run 'src/mapUpload.py' to pubčlish your game to our web server. You need obtain a "map_maker" role first by sending a request to me (jnpelicon@gmail.com).

## Contributing

If you encounter any bugs or have suggestions for improving the Map Maker, feel free to contact us.

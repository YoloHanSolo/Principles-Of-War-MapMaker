# Principles of War – Scenario Maker

Welcome to the **Principles of War Scenario Maker**! This guide will walk you through creating, editing, compiling, and publishing scenarios for the game. Follow the steps carefully to get started.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Creating a New Scenario](#creating-a-new-scenario)
4. [Workflow](#workflow)
5. [Available Commands](#available-commands)
6. [Contributing & Support](#contributing--support)

---

## Requirements

Before starting, ensure you have the following installed:

- **Python 3** ([Download here](https://www.python.org/downloads/))
- **Tiled Level Editor** ([Download here](https://www.scenarioeditor.org/))
- **VSCode** or any text editor for `.json` files ([Download here](https://code.visualstudio.com/download))
- **Paint.NET** or any image editor that supports transparent `.png` icons ([Download here](https://www.getpaint.net/download.html))

---

## Setup

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. Create a Python virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **Linux / macOS**:

     ```bash
     source venv/bin/activate
     ```

4. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the main script (all commands are executed through `main.py`):

   ```bash
   python main.py
   ```

> You can also use `main.bat` (Windows) or `main.sh` (Linux/macOS) to run the script.

---

## Creating a New Scenario

1. **Create a new scenario folder**

   Inside `./scenarios_data`, create a folder for your scenario and name it using a `<scenario_ID>` format, e.g.:

   ```
   ./scenarios_data/scenario_new
   ```

2. **Create a unit icon folder**

   Inside your scenario folder, create a `unit_icons` folder for all your `.png` unit icons:

   ```
   ./scenarios_data/scenario_new/unit_icons
   ```

3. **Prepare required JSON files**

   Your scenario folder should contain:

   ```
   unit_icons/...
   description.json
   factions.json
   landmarks.json
   scenario.tmx # Scenario created with Tiled
   time.json
   turn.json
   unit_types.json
   units.json
   ```

> Tip: Inspect existing scenarios in `./scenarios_data/` to understand structure and formatting.

---

## Workflow

Follow these steps to create, edit, and publish a scenario:

1. **Create the virtual environment and activate it** (as shown in Setup).

2. **Create a new empty scenario**:

   ```bash
   python main.py
   ```

   - Select `Create New Scenario`
   - Enter a `<scenario_ID>` (e.g., `scenario_new`)

3. **Use Tiled to design the scenario**
   - Open `scenario.tmx` in Tiled.
   - Design terrain layers (plains, mountains, rivers, etc.).

4. **Place landmarks**
   - Cities, oilfields, supply depots, etc.
   - After placing landmarks, run:

     ```bash
     python main.py
     ```

     - Select `Generate Landmarks Template`
     - This populates `landmarks.json` automatically.

5. **Continue working on the scenario**
   - Add units, set factions, define turns and time, etc.
   - Edit `.json` files in a text editor as needed.

6. **Compile your scenario**

   When your scenario is ready:

   ```bash
   python main.py
   ```

   - Select `Compile Scenario`
   - This generates a single `.json` file in `./scenarios`.

7. **Upload to server (optional)**

   To publish your scenario:

   ```bash
   python main.py
   ```

   - Select `Upload Scenario`
   - You need a **scenario_maker** role. Contact: [jnpelicon@gmail.com](mailto:jnpelicon@gmail.com)

---

## Available Commands (via `main.py`)

| Command                     | Description                                              |
| --------------------------- | -------------------------------------------------------- |
| Create New Scenario         | Initialize a new empty scenario folder and default files |
| Generate Landmarks Template | Scan `scenario.tmx` and generate `landmarks.json`        |
| Compile Scenario            | Build a single JSON file containing all scenario data    |
| Upload Scenario             | Publish scenario to the game server                      |
| Exit                        | Close the script                                         |

> All commands are interactive: first select a command, then parameters are collected using Inquirer prompts.

---

## Contributing & Support

- If you encounter bugs or issues, please open an issue or contact **[jnpelicon@gmail.com](mailto:jnpelicon@gmail.com)**
- Suggestions for improvement are welcome.
- Review existing scenarios in `./scenarios_data/` for guidance and examples.

---

## Quick Start Example

```bash
# 1. Setup virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a new scenario
python main.py  # Select "Create New Scenario" -> scenario_new

# 4. Edit scenario in Tiled

# 5. Generate landmarks template
python main.py  # Select "Generate Landmarks Template"

# 6. Compile scenario
python main.py  # Select "Compile Scenario"

# 7. Optionally upload
python main.py  # Select "Upload Scenario"

# 8. Deactivate venv
deactivate
```

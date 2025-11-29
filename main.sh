#!/bin/bash
set -e

# Activate the virtual environment
source venv/bin/activate

# Run the main Python script
python main.py

# Optional: deactivate the venv
deactivate

# Wait for user input to keep terminal open
read -p "Press [Enter] key to exit..."

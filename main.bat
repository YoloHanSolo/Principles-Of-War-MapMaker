@echo off
REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run the main Python script
python main.py

REM Optional: Deactivate after running
call deactivate

REM Pause to keep the CMD window open
pause
@echo off
py -m venv venv
call venv\Scripts\activate.bat
py -m pip install -r requirements.txt
py app.py
pause

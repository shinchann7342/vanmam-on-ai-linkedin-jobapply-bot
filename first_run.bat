@echo off
TITLE Job Bot - First Run Setup
color 0a

echo ==================================================
echo      INSTALLING REQUIRED LIBRARIES...
echo ==================================================
pip install -r requirements.txt

echo.
echo ==================================================
echo      STARTING CONFIGURATION FORM...
echo ==================================================
echo Please fill in your details in the browser window that opens.
echo.

python app.py

pause
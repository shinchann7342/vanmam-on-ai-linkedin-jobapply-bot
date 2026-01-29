@echo off
TITLE Job Bot - Auto Execution
color 0c

echo.
echo ==================================================
echo      STARTING JOB APPLICATION PROTOCOL...
echo ==================================================
echo.
:: Try to run the manager script
python telegram_manager.py

:: Check if the previous command failed (Error Level not equal to 0)
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo      CRITICAL ERROR ENCOUNTERED
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo.
    echo Opening error report...
    
    :: Open the alert HTML file in the default browser
    start alert.html
    
    pause
    exit /b
)

echo.
echo ==================================================
echo      PROCESS COMPLETE
echo ==================================================
pause
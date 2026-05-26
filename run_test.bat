@echo off
REM MQTTX Test Helper for Windows
REM Usage: run_test.bat [scenario] [count]

setlocal enabledelayedexpansion

cls
echo.
echo ====================================================================
echo   MQTTX Dashboard Test Helper
echo ====================================================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Install Python from python.org or add it to your PATH
    pause
    exit /b 1
)

REM Show scenarios if no argument
if "%1"=="" (
    echo Available test scenarios:
    echo.
    echo   run_test.bat normal        - Normal air quality
    echo   run_test.bat clean         - Clean air
    echo   run_test.bat polluted      - High pollution
    echo   run_test.bat hot           - Hot and humid
    echo   run_test.bat cold          - Cold and dry
    echo.
    echo Example:
    echo   run_test.bat normal 5      - Publish 5 normal quality messages
    echo.
    pause
    exit /b 0
)

REM Run the Python script
set SCENARIO=%1
set COUNT=%2
if "%COUNT%"=="" set COUNT=1

echo Running: python mqttx_helper.py %SCENARIO% %COUNT%
echo.

python mqttx_helper.py %SCENARIO% %COUNT%

if errorlevel 1 (
    echo.
    echo ERROR: Failed to publish messages
    echo Check your internet connection and try again
)

echo.
pause

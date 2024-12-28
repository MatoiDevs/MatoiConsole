@echo off
SETLOCAL

REM Check if Python 3.12.7 is installed
python --version 2>nul | findstr /i "Python 3.12.7" >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python 3.12.7 is not installed.
    echo Opening Microsoft Store to download Python 3.12.7...
    start ms-windows-store://pdp/?ProductId=9ncvdn91xzqp
    exit /b 1
)

echo Python 3.12.7 is installed.

REM Check if requirements.txt exists
IF NOT EXIST "requirements.txt" (
    echo requirements.txt not found.
    exit /b 1
)

echo Installing packages from requirements.txt...
pip install -r requirements.txt

IF %ERRORLEVEL% EQU 0 (
    echo Packages installed successfully.
) ELSE (
    echo Failed to install packages.
)

ENDLOCAL

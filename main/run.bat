@echo off
title Forkspoofer Loader
setlocal

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Forkspoofer requires administrative privileges.
    pause
    exit /b
)

echo Installing Forkspoofer dependencies...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed, downloading and installing Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe' -OutFile 'python_installer.exe'"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
) else (
    echo Python is already installed.
)

echo Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install netifaces

cd /d "%~dp0"
echo Running Forkspoofer...
python main.py

@echo off
echo Starting Dockerized Database Sync...

:: 1. Navigate to the folder containing your Docker files
:: (The %~dp0 guarantees it finds the right folder no matter where you double-click it from)
cd /d "%~dp0for_docker"

:: 2. Tell Docker to build and run the container
:: (This replaces the old "python update_DB.py" command)
docker-compose up --build

echo.
echo Sync Complete! 
pause
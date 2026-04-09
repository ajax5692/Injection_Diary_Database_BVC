@echo off
echo Starting Database Sync...

:: 1. Navigate to your project folder
cd /d "C:\Users\abhrajyoti.chakrabarti\Documents\GitHub\Injection_Diary_Database_BVC\Python_SQL"

:: 2. Activate the virtual environment
call my_venv\Scripts\activate.bat

:: 3. Run the database update script
echo Updating SQLite database...
python update_DB.py

:: 4. Deactivate and close
deactivate
echo Sync Complete!

pause
@echo off
cd /d "c:\Users\acer\OneDrive\Desktop\Market-buddy\backend"
call ..\\.venv\Scripts\activate.bat
echo Running Alembic migrations...
alembic upgrade head
echo Done!
pause

@REM Setup script for Windows
@REM Run from the project root directory
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo Virtual environment activated.
call scripts\dbCreate.bat
echo Database created.
call scripts\dbSeed.bat
echo Database seeded.
echo Setup complete.
@REM Setup script for Windows
@REM Run from the project root directory
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo "Virtual environment activated."
.\scripts\dbCreate.bat
echo "Database created."
python -m app.seeds.seed.py
echo "Database seeded."
echo "Setup complete."
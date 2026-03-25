@REM Starting script for Windows
@REM Run from the project root directory
call venv\Scripts\activate.bat
echo Virtual environment activated.
echo Launching API...
python app.py
echo API stopped.
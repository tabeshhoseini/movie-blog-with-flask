@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Movie Blog...
python app.py
pause
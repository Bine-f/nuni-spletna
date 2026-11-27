@echo off
cd /d "%~dp0"
python build.py
if errorlevel 1 (
  echo.
  echo Python ni namescen ali gradnja ni uspela. Glej README.md.
  pause
  exit /b 1
)
start "" "dist\index.html"

@echo off
REM Hospital Management System - Windows Setup Script

echo =====================================
echo 🏥 Hospital Management System Setup
echo =====================================
echo.

REM Check Python version
echo Checking Python installation...
python --version
echo.

REM Install dependencies
echo 📦 Installing dependencies...
echo Using: uv sync
echo.

uv sync

echo.
echo ✅ Installation complete!
echo.
echo 🚀 To start the application, run:
echo    python main.py
echo.
echo 🌐 Then open your browser to:
echo    http://localhost:5000
echo.
echo 📝 Default login credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo 📚 Documentation:
echo    - README.md - Full documentation
echo    - QUICKSTART.md - Quick start guide
echo    - IMPLEMENTATION_SUMMARY.md - What's included
echo.
echo Happy managing! 🏥✨
echo.
pause

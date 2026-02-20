@echo off
REM LostLinked Backend Startup Script for Windows

echo 🚀 Starting LostLinked Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your database credentials!
    pause
    exit
)

REM Start the server
echo ✅ Starting FastAPI server on http://localhost:8000
python main.py

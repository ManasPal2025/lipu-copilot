@echo off
REM Development setup script for LIPU Platform (Windows)

echo.
echo 🚀 LIPU Platform - Development Setup (Windows)
echo.

REM Check prerequisites
echo 📋 Checking prerequisites...

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git not found. Please install Git.
    exit /b 1
)

where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker not found. Please install Docker Desktop.
    exit /b 1
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 20+.
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.11+.
    exit /b 1
)

echo ✅ All prerequisites installed
echo.

REM Setup environment
echo 📦 Setting up repository...

if not exist ".env.local" (
    echo Creating .env.local...
    copy .env.example .env.local
    echo ⚠️  Please edit .env.local with your credentials
)

REM Start Docker services
echo 🐳 Starting Docker services...
docker-compose up -d

echo ⏳ Waiting for services to be healthy...
timeout /t 10

REM Setup backend
echo 🔧 Setting up backend...
cd apps\api

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt > nul 2>&1
pip install -r requirements-dev.txt > nul 2>&1

cd ..\..

REM Setup frontend
echo ⚙️  Setting up frontend...
cd apps\web
npm install > nul 2>&1
cd ..\..

echo.
echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo   1. Edit .env.local with your credentials
echo   2. Terminal 1: npm run api:dev
echo   3. Terminal 2: npm run web:dev
echo   4. Frontend: http://localhost:3000
echo   5. API Docs: http://localhost:8000/docs
echo.
echo 📚 For more info, see docs\guides\development-setup.md

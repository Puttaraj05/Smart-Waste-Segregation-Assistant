@echo off
chcp 65001 >nul

echo 🚀 Starting Waste Classification AI Application...
echo.

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Backend directory not found!
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo ❌ Frontend directory not found!
    pause
    exit /b 1
)

REM Start backend server
echo 🔧 Starting backend server...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and start server
call venv\Scripts\activate.bat
echo 📦 Installing backend dependencies...
pip install -r requirements.txt >nul 2>&1

echo 🚀 Starting FastAPI server on http://localhost:8000
start "Backend Server" cmd /k "uvicorn app:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend server
echo 🎨 Starting frontend server...
cd ..\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo 📦 Installing frontend dependencies...
    npm install >nul 2>&1
)

echo 🚀 Starting React development server on http://localhost:3000
start "Frontend Server" cmd /k "npm run dev"

echo.
echo ✅ Both servers are starting up!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo.
echo Press any key to close this window...
pause >nul 
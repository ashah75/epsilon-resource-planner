@echo off
REM Resource Planner - Fixed Windows Setup Script
REM Simplified version that avoids batch parsing issues

echo ===============================================================
echo      Epsilon Resource Planner - Windows Setup
echo ===============================================================
echo.

echo Checking prerequisites...
echo.

REM Check Python with simpler test
echo Checking Python...
python -c "print('OK')" 2>nul
if errorlevel 1 (
    echo.
    echo [ERROR] Python is NOT installed or NOT in PATH
    echo.
    echo Please install Python 3.7+ from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python -V 2^>^&1') do set PYTHON_VER=%%i
echo [OK] %PYTHON_VER%

REM Check Node.js with simpler test
echo Checking Node.js...
node -e "console.log('OK')" 2>nul
if errorlevel 1 (
    echo.
    echo [ERROR] Node.js is NOT installed or NOT in PATH
    echo.
    echo Please install Node.js 16+ from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node -v') do set NODE_VER=%%i
echo [OK] Node.js %NODE_VER%

REM Check npm
echo Checking npm...
npm -v >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] npm is NOT installed
    echo npm should come with Node.js. Please reinstall Node.js
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm -v') do set NPM_VER=%%i
echo [OK] npm %NPM_VER%

echo.
echo ===============================================================
echo All prerequisites found! Starting setup...
echo ===============================================================
echo.

REM Setup backend
echo Setting up backend...
if not exist "backend" (
    echo [ERROR] backend folder not found!
    echo Please run this script from the outputs folder
    pause
    exit /b 1
)

cd backend
echo Installing Python packages (Flask, Flask-CORS)...
pip install flask flask-cors
if errorlevel 1 (
    echo Warning: Trying alternative pip method...
    python -m pip install flask flask-cors
)
cd ..
echo [OK] Backend setup complete!
echo.

REM Setup frontend
echo Setting up frontend...
if not exist "frontend" (
    echo [ERROR] frontend folder not found!
    pause
    exit /b 1
)

cd frontend
if not exist "node_modules" (
    echo Installing Node packages (this takes 2-3 minutes)...
    call npm install
    if errorlevel 1 (
        echo [ERROR] npm install failed
        pause
        exit /b 1
    )
) else (
    echo Node packages already installed.
)
cd ..
echo [OK] Frontend setup complete!
echo.

REM Start services
echo ===============================================================
echo Starting servers...
echo ===============================================================
echo.

echo Starting backend on http://localhost:5000
start "Backend Server" cmd /k "cd backend && python backend.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting frontend on http://localhost:3000
echo.
echo ===============================================================
echo                      READY!
echo ===============================================================
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:3000 (opens in browser)
echo.
echo   Backend is running in the other window
echo   Press Ctrl+C here to stop frontend
echo ===============================================================
echo.

cd frontend
start http://localhost:3000
npm run dev

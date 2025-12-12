@echo off
REM Resource Planner - Windows Setup Script (Batch)
REM This works in Windows Command Prompt

echo ===============================================================
echo      Epsilon Resource Planner - Windows Setup
echo ===============================================================
echo.

REM Check Python
echo Checking prerequisites...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    echo Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed
    echo npm should come with Node.js. Please reinstall Node.js
    pause
    exit /b 1
)

echo [OK] Python: 
python --version
echo [OK] Node.js: 
node --version
echo [OK] npm: 
npm --version
echo.

REM Setup backend
echo ===============================================================
echo Setting up backend...
echo ===============================================================
cd backend

echo Installing Python dependencies...
pip install flask flask-cors
if errorlevel 1 (
    echo Warning: pip install had issues. Trying alternative...
    python -m pip install flask flask-cors
)

echo.
echo [OK] Backend setup complete!
echo.

REM Setup frontend
echo ===============================================================
echo Setting up frontend...
echo ===============================================================
cd ..\frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] npm install failed
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)

echo.
echo [OK] Frontend setup complete!
echo.

REM Start services
echo ===============================================================
echo Starting services...
echo ===============================================================
echo.

REM Start backend in new window
echo Starting backend server on http://localhost:5000
cd ..\backend
start "Backend Server" cmd /k "python backend.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
cd ..\frontend
echo Starting frontend server on http://localhost:3000
echo.
echo ===============================================================
echo                      Ready to Go!
echo ===============================================================
echo.
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:3000
echo.
echo   Press Ctrl+C in this window to stop frontend
echo   Close the Backend Server window to stop backend
echo.
echo ===============================================================
echo.

npm run dev

@echo off
REM Resource Planner - Enhanced Windows Setup Script with Debugging
REM This version shows exactly what's wrong

echo ===============================================================
echo      Epsilon Resource Planner - Windows Setup (Debug Mode)
echo ===============================================================
echo.

REM Check Python
echo [Step 1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is NOT installed or NOT in PATH
    echo.
    echo Please install Python 3.7+ from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    echo After installing Python, restart this Command Prompt and try again.
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Python found: 
    python --version
)
echo.

REM Check Node.js
echo [Step 2/3] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Node.js is NOT installed or NOT in PATH
    echo.
    echo Please install Node.js 16+ from: https://nodejs.org/
    echo Download the LTS (Long Term Support) version
    echo.
    echo After installing Node.js, restart this Command Prompt and try again.
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Node.js found: 
    node --version
)
echo.

REM Check npm
echo [Step 3/3] Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] npm is NOT installed
    echo.
    echo npm should come with Node.js. Please reinstall Node.js from:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
) else (
    echo [OK] npm found: 
    npm --version
)
echo.

echo ===============================================================
echo All prerequisites are installed! Continuing setup...
echo ===============================================================
echo.
pause

REM Setup backend
echo ===============================================================
echo Setting up backend...
echo ===============================================================
if not exist "backend" (
    echo [ERROR] backend folder not found!
    echo Are you running this from the correct folder?
    echo Current folder: %CD%
    pause
    exit /b 1
)

cd backend

echo Installing Python dependencies...
echo This may take a minute...
pip install flask flask-cors
if errorlevel 1 (
    echo.
    echo Warning: pip install had issues. Trying alternative method...
    python -m pip install flask flask-cors
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install Python packages
        echo Try running: python -m pip install --upgrade pip
        pause
        exit /b 1
    )
)

echo.
echo [OK] Backend setup complete!
echo.
pause

REM Setup frontend
echo ===============================================================
echo Setting up frontend...
echo ===============================================================
cd ..
if not exist "frontend" (
    echo [ERROR] frontend folder not found!
    echo Are you running this from the correct folder?
    echo Current folder: %CD%
    pause
    exit /b 1
)

cd frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    echo This will take 2-3 minutes...
    echo.
    call npm install
    if errorlevel 1 (
        echo.
        echo [ERROR] npm install failed
        echo Try: npm cache clean --force
        echo Then run this script again
        pause
        exit /b 1
    )
) else (
    echo Node modules already installed.
)

echo.
echo [OK] Frontend setup complete!
echo.
pause

REM Start services
echo ===============================================================
echo Starting services...
echo ===============================================================
echo.

REM Start backend in new window
echo Starting backend server...
cd ..\backend
start "Backend Server - DO NOT CLOSE" cmd /k "echo Backend Server Running && echo. && python backend.py"

REM Wait for backend to start
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend
cd ..\frontend
echo Starting frontend server...
echo.
echo ===============================================================
echo                      Ready!
echo ===============================================================
echo.
echo   Backend:  http://localhost:5000
echo   Frontend: http://localhost:3000
echo.
echo   A new window opened with the backend server.
echo   This window will show the frontend server.
echo.
echo   Press Ctrl+C to stop the frontend server.
echo   Close the backend window to stop the backend.
echo.
echo ===============================================================
echo.

npm run dev

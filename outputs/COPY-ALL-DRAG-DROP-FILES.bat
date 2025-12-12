@echo off
echo ========================================
echo COPYING ALL DRAG-DROP FILES
echo ========================================
echo.

REM Copy all required files for drag-drop to work
echo [1/8] Copying App.jsx...
copy /Y "outputs\frontend\src\App.jsx" "frontend\src\App.jsx"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy App.jsx
    pause
    exit /b 1
)

echo [2/8] Copying Sidebar.jsx...
copy /Y "outputs\frontend\src\components\layout\Sidebar.jsx" "frontend\src\components\layout\Sidebar.jsx"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy Sidebar.jsx
    pause
    exit /b 1
)

echo [3/8] Copying Timeline.jsx...
copy /Y "outputs\frontend\src\components\timeline\Timeline.jsx" "frontend\src\components\timeline\Timeline.jsx"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy Timeline.jsx
    pause
    exit /b 1
)

echo [4/8] Copying TimelineGrid.jsx...
copy /Y "outputs\frontend\src\components\timeline\TimelineGrid.jsx" "frontend\src\components\timeline\TimelineGrid.jsx"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy TimelineGrid.jsx
    pause
    exit /b 1
)

echo [5/8] Copying TimelineCell.jsx...
copy /Y "outputs\frontend\src\components\timeline\TimelineCell.jsx" "frontend\src\components\timeline\TimelineCell.jsx"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy TimelineCell.jsx
    pause
    exit /b 1
)

echo [6/8] Copying AssignmentModal.jsx...
copy /Y "outputs\frontend\src\components\modals\AssignmentModal.jsx" "frontend\src\components\modals\AssignmentModal.jsx"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy AssignmentModal.jsx
    pause
    exit /b 1
)

echo [7/8] Copying assignmentUtils.js...
copy /Y "outputs\frontend\src\utils\assignmentUtils.js" "frontend\src\utils\assignmentUtils.js"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy assignmentUtils.js
    pause
    exit /b 1
)

echo [8/8] Copying globals.css...
copy /Y "outputs\frontend\src\styles\globals.css" "frontend\src\styles\globals.css"
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy globals.css
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ ALL 8 FILES COPIED SUCCESSFULLY!
echo ========================================
echo.
echo Files copied:
echo   1. App.jsx (handles drag-drop)
echo   2. Sidebar.jsx (draggable projects)
echo   3. Timeline.jsx (passes handlers)
echo   4. TimelineGrid.jsx (passes to cells)
echo   5. TimelineCell.jsx (drop handler)
echo   6. AssignmentModal.jsx (edit mode)
echo   7. assignmentUtils.js (field names)
echo   8. globals.css (drop-target styles)
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. STOP frontend if running (Ctrl+C)
echo.
echo 2. RESTART frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 3. HARD REFRESH browser:
echo    Press: Ctrl + Shift + R
echo.
echo 4. TEST drag-drop:
echo    - Open DevTools (F12) -^> Console tab
echo    - Drag project from sidebar
echo    - Drop on timeline cell
echo    - Watch console for messages
echo.
echo ========================================
echo.
pause

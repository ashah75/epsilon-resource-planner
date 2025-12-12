# 🪟 Windows Setup Guide - Epsilon Resource Planner

## 📋 Prerequisites

Before starting, you need to install:

### 1. Python 3.7+ ✓
**Download:** https://www.python.org/downloads/

**Installation Steps:**
1. Download the latest Python 3.x installer
2. Run the installer
3. ⚠️ **IMPORTANT:** Check the box "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation to complete

**Verify Installation:**
```cmd
python --version
```
Should show: `Python 3.x.x`

### 2. Node.js 16+ ✓
**Download:** https://nodejs.org/

**Installation Steps:**
1. Download the LTS version (recommended)
2. Run the installer
3. Click "Next" through the installer
4. Node.js will automatically be added to PATH
5. Wait for installation to complete

**Verify Installation:**
```cmd
node --version
npm --version
```
Should show versions for both

---

## 🚀 Quick Start (Option 1: PowerShell - Recommended)

### Step 1: Open PowerShell
1. Press `Win + X`
2. Select "Windows PowerShell" or "Terminal"

### Step 2: Navigate to Project
```powershell
cd Downloads\outputs
# Or wherever you extracted the files
```

### Step 3: Run Setup Script
```powershell
.\start.ps1
```

**If you get an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\start.ps1
```

### Step 4: Access Application
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

The script will:
- ✓ Check prerequisites
- ✓ Install dependencies
- ✓ Start backend in new window
- ✓ Start frontend in current window

---

## 🚀 Quick Start (Option 2: Command Prompt)

### Step 1: Open Command Prompt
1. Press `Win + R`
2. Type `cmd`
3. Press Enter

### Step 2: Navigate to Project
```cmd
cd Downloads\outputs
```

### Step 3: Run Setup Script
```cmd
start.bat
```

### Step 4: Access Application
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

---

## 🛠️ Manual Setup (If Scripts Don't Work)

### Step 1: Setup Backend

**Open Command Prompt/PowerShell:**
```cmd
cd path\to\outputs\backend
pip install flask flask-cors
```

**If pip doesn't work:**
```cmd
python -m pip install flask flask-cors
```

### Step 2: Setup Frontend

**In the same or new Command Prompt/PowerShell:**
```cmd
cd path\to\outputs\frontend
npm install
```

This will take 2-3 minutes to download all packages.

### Step 3: Start Backend

**In Command Prompt/PowerShell #1:**
```cmd
cd path\to\outputs\backend
python backend.py
```

Keep this window open! You should see:
```
🚀 Backend server starting...
📊 Database: SQLite (resource_planner.db)
🌐 API running on: http://localhost:5000
```

### Step 4: Start Frontend

**In NEW Command Prompt/PowerShell #2:**
```cmd
cd path\to\outputs\frontend
npm run dev
```

You should see:
```
VITE v4.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

### Step 5: Open Browser
Go to: http://localhost:3000

---

## 📁 Project Location

**After downloading, you should have:**
```
Downloads\outputs\
├── start.ps1                (PowerShell script)
├── start.bat                (Batch script)
├── WINDOWS-SETUP.md         (This file)
├── README-REACT.md
├── QUICK-START.md
│
├── backend\
│   └── backend.py
│
└── frontend\
    ├── package.json
    ├── index.html
    └── src\
        └── (React files)
```

---

## 🐛 Troubleshooting

### Issue: "Python is not recognized"

**Solution:**
1. Reinstall Python
2. Make sure "Add Python to PATH" is checked
3. Restart your terminal/computer
4. Try again

**Manual PATH setup:**
1. Open System Properties → Environment Variables
2. Under "System Variables", find "Path"
3. Add Python path (e.g., `C:\Python311\` and `C:\Python311\Scripts\`)

### Issue: "Node is not recognized"

**Solution:**
1. Reinstall Node.js from https://nodejs.org/
2. Restart your terminal/computer
3. Try again

### Issue: "npm install" fails

**Solution 1: Clear npm cache**
```cmd
npm cache clean --force
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

**Solution 2: Use different registry**
```cmd
npm config set registry https://registry.npmjs.org/
npm install
```

### Issue: Port 5000 is already in use

**Solution 1: Find and kill the process**
```cmd
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F
```

**Solution 2: Change the port**

Edit `frontend\vite.config.js`:
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5001',  // Changed to 5001
        changeOrigin: true,
      }
    }
  }
})
```

Then start backend with different port:
```python
# In backend.py, last line:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Execution policy error in PowerShell

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or run with bypass:
```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

### Issue: "Access is denied" when installing Python packages

**Solution 1: Run as Administrator**
1. Right-click Command Prompt/PowerShell
2. Select "Run as Administrator"
3. Try again

**Solution 2: Install in user directory**
```cmd
pip install --user flask flask-cors
```

### Issue: Frontend shows blank page

**Solutions:**
1. Check browser console (F12) for errors
2. Verify backend is running on port 5000
3. Check http://localhost:5000/api/health
4. Clear browser cache (Ctrl + Shift + Delete)
5. Try incognito/private window

### Issue: Backend crashes immediately

**Check:**
1. Is `resource_planner.db` writable?
2. Any antivirus blocking Python?
3. Any firewall blocking port 5000?

**Solution:**
```cmd
cd backend
python -c "import flask; print(flask.__version__)"
```

If this fails, reinstall Flask:
```cmd
pip uninstall flask flask-cors
pip install flask flask-cors
```

---

## 🔄 Stopping the Servers

### Stop Frontend:
- In the frontend terminal/window: Press `Ctrl + C`
- Confirm with `Y` if asked

### Stop Backend:
- In the backend terminal/window: Press `Ctrl + C`
- Or close the window

---

## 📂 File Paths in Windows

Windows uses backslashes `\` instead of forward slashes `/`:

**Correct:**
```cmd
cd C:\Users\YourName\Downloads\outputs\backend
```

**Wrong:**
```cmd
cd C:/Users/YourName/Downloads/outputs/backend
```

**In PowerShell, both work, but backslash is preferred.**

---

## 🎯 Development Workflow

### Daily Startup:
1. Open 2 terminals (Command Prompt or PowerShell)
2. Terminal 1: 
   ```cmd
   cd path\to\outputs\backend
   python backend.py
   ```
3. Terminal 2:
   ```cmd
   cd path\to\outputs\frontend
   npm run dev
   ```
4. Open http://localhost:3000

### Or use the scripts:
- **PowerShell:** `.\start.ps1`
- **Command Prompt:** `start.bat`

---

## 🔧 IDE Recommendations for Windows

### VS Code (Recommended)
**Download:** https://code.visualstudio.com/

**Extensions to install:**
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- Python

**Open project:**
```cmd
cd path\to\outputs
code .
```

### PyCharm
**Download:** https://www.jetbrains.com/pycharm/

Good for Python development, also supports JavaScript/React.

---

## 🌐 Browser Recommendations

**Best to worst:**
1. Chrome (best React DevTools)
2. Edge (Chromium-based, good)
3. Firefox (good)
4. Safari (not available on Windows)

**Install React DevTools:**
- Chrome: https://chrome.google.com/webstore → Search "React Developer Tools"

---

## 💾 Database Location

**Windows path:**
```
outputs\backend\resource_planner.db
```

**To reset database:**
```cmd
cd outputs\backend
del resource_planner.db
python backend.py
```
The database will be recreated automatically.

---

## 📊 Checking if Services are Running

### Check Backend:
Open browser and go to: http://localhost:5000/api/health

Should see:
```json
{"status": "healthy", "timestamp": "..."}
```

### Check Frontend:
Open browser and go to: http://localhost:3000

Should see the Resource Planner interface.

### From Command Line:
```cmd
netstat -ano | findstr :5000
netstat -ano | findstr :3000
```

If you see output, the ports are in use (servers are running).

---

## 🎓 Windows Terminal Tips

### Open multiple tabs:
- Press `Ctrl + Shift + T` in Windows Terminal
- Tab 1: Run backend
- Tab 2: Run frontend

### Split panes:
- Press `Alt + Shift + D` to split pane
- Run backend in left pane
- Run frontend in right pane

---

## 📱 Accessing from Phone (Same Network)

1. Find your computer's IP address:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. Start frontend with host option:
   ```cmd
   npm run dev -- --host
   ```

3. On your phone's browser, go to:
   ```
   http://192.168.1.100:3000
   ```

---

## 🎉 Success Checklist

After setup, you should have:

- ✅ Python installed and in PATH
- ✅ Node.js installed and in PATH
- ✅ Backend running on port 5000
- ✅ Frontend running on port 3000
- ✅ Can access http://localhost:3000
- ✅ See Epsilon logo and interface
- ✅ No errors in browser console (F12)

---

## 📞 Additional Help

If you're still stuck:

1. **Check the logs:**
   - Backend terminal shows Python errors
   - Frontend terminal shows npm/Vite errors
   - Browser console (F12) shows JavaScript errors

2. **Read the docs:**
   - README-REACT.md
   - COMPONENT-IMPLEMENTATION-GUIDE.md
   - PROJECT-SUMMARY.md

3. **Common issues are in this file** - scroll up to Troubleshooting section

---

## 🎯 Next Steps

After successful setup:

1. **Read:** `QUICK-START.md` for basic usage
2. **Explore:** The working React app at http://localhost:3000
3. **Implement:** Follow `COMPONENT-IMPLEMENTATION-GUIDE.md` to complete the timeline display
4. **Learn:** React documentation at https://react.dev

---

**You're all set for Windows! 🪟🚀**

The React app is now ready to run on your Windows machine!

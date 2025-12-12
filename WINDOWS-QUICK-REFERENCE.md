# 🪟 Windows Quick Reference Card

## ⚡ Super Quick Start

### Option 1: PowerShell (Recommended)
```powershell
cd Downloads\outputs
.\start.ps1
```

### Option 2: Command Prompt
```cmd
cd Downloads\outputs
start.bat
```

---

## 📋 Prerequisites

✅ **Python 3.7+** → https://www.python.org/downloads/  
✅ **Node.js 16+** → https://nodejs.org/

**⚠️ IMPORTANT:** Check "Add Python to PATH" during installation!

---

## 🚀 Manual Start (2 Windows)

### Window 1 - Backend:
```cmd
cd path\to\outputs\backend
python backend.py
```

### Window 2 - Frontend:
```cmd
cd path\to\outputs\frontend
npm run dev
```

### Open Browser:
http://localhost:3000

---

## 🛑 Stop Servers

Press `Ctrl + C` in each terminal window

---

## 🐛 Quick Fixes

### "Python not recognized"
```cmd
# Reinstall Python with "Add to PATH" checked
# OR manually add to Windows PATH
```

### "Port 5000 in use"
```cmd
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F
```

### "npm install fails"
```cmd
npm cache clean --force
cd frontend
rmdir /s /q node_modules
npm install
```

### "Permission denied"
```cmd
# Run Command Prompt as Administrator
# Right-click → "Run as Administrator"
```

---

## 📂 Key Files

```
outputs\
├── start.ps1          ← PowerShell script
├── start.bat          ← Batch script
├── WINDOWS-SETUP.md   ← Full guide
│
├── backend\
│   └── backend.py     ← Flask API
│
└── frontend\
    ├── package.json
    └── src\           ← React code
```

---

## 🔍 Check If Running

### Backend Check:
```cmd
# In browser:
http://localhost:5000/api/health

# In terminal:
netstat -ano | findstr :5000
```

### Frontend Check:
```cmd
# In browser:
http://localhost:3000

# In terminal:
netstat -ano | findstr :3000
```

---

## 💡 Pro Tips

### Use Windows Terminal:
- Install from Microsoft Store
- Open multiple tabs: `Ctrl + Shift + T`
- Split panes: `Alt + Shift + D`

### VS Code Integration:
```cmd
cd outputs
code .
```

### Reset Database:
```cmd
cd backend
del resource_planner.db
python backend.py
```

---

## 📱 Access from Phone

1. Get your PC's IP:
   ```cmd
   ipconfig
   ```

2. Start with host flag:
   ```cmd
   npm run dev -- --host
   ```

3. On phone: `http://YOUR_IP:3000`

---

## ✅ Verify Installation

```cmd
python --version
node --version
npm --version
```

All should show version numbers.

---

## 📚 Full Documentation

- **WINDOWS-SETUP.md** → Complete Windows guide
- **README-REACT.md** → Full documentation
- **QUICK-START.md** → General quick start
- **PROJECT-SUMMARY.md** → What's included

---

## 🆘 Common Errors

| Error | Solution |
|-------|----------|
| Python not found | Add to PATH or reinstall |
| Node not found | Reinstall Node.js |
| Port in use | Kill process or change port |
| npm fails | Clear cache, delete node_modules |
| Permission denied | Run as Administrator |
| Blank page | Check backend is running |
| CORS error | Backend/frontend ports mismatch |

---

## 🎯 Development Workflow

**Daily routine:**
1. Open 2 terminals
2. Terminal 1: `cd backend && python backend.py`
3. Terminal 2: `cd frontend && npm run dev`
4. Open http://localhost:3000
5. Code and save (hot reload enabled!)

**Or just run:** `start.ps1` or `start.bat`

---

## 🔗 URLs to Remember

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health

---

## 📞 Need Help?

1. Read **WINDOWS-SETUP.md** (comprehensive troubleshooting)
2. Check browser console (F12)
3. Check terminal error messages
4. Google the specific error message

---

**Keep this card handy!** 📌

Print or save for quick reference when developing on Windows.

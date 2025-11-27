# Epsilon Resource Planner - Troubleshooting Guide

## 🐛 Common Issues and Solutions

### Issue: KeyError: 'startDate' when testing API

**Error Message:**
```
KeyError: 'startDate'
File "backend.py", line 167, in add_assignment
```

**Solution:**
This was fixed in the latest version! The backend now supports both formats:

1. **Update your backend.py** to the latest version
2. **Restart the backend:**
   ```bash
   python3 backend.py
   ```

The backend now accepts:
- **New format:** `{personId, projectId, startDate, endDate, percentage}`
- **Old format:** `{personId, projectId, period}` (auto-converts to dates)

### Issue: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install flask flask-cors --break-system-packages
```

### Issue: "Error connecting to server" in frontend

**Symptoms:**
- Red error message in app
- Assignments not saving
- Data not loading

**Solution:**
1. Check if backend is running:
   ```bash
   # Look for this process
   ps aux | grep python3 | grep backend
   ```

2. If not running, start it:
   ```bash
   cd /mnt/user-data/outputs
   python3 backend.py
   ```

3. Look for: `🌐 API running on: http://localhost:5000`

4. Refresh the frontend page

### Issue: Port 5000 already in use

**Error:** `Address already in use` or `Port 5000 is already in use`

**Solution 1 - Kill existing process:**
```bash
# Find the process
lsof -ti:5000

# Kill it
kill -9 $(lsof -ti:5000)

# Restart backend
python3 backend.py
```

**Solution 2 - Use different port:**
1. Edit `backend.py`, change last line to:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. Edit `resource-planner.html`, find this line:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```
   Change to:
   ```javascript
   const API_BASE_URL = 'http://localhost:5001/api';
   ```

### Issue: Database file not found

**Error:** `Database file disappeared` or `No such file: resource_planner.db`

**Solution:**
The backend creates the database in its current directory:

```bash
# Navigate to where backend.py is
cd /mnt/user-data/outputs

# Start backend here
python3 backend.py
```

**Important:** Always run backend.py from the same directory!

### Issue: Dates not working / Invalid date format

**Error:** Assignment not appearing, or "Invalid date" message

**Solution:**
Dates MUST be in YYYY-MM-DD format:
- ✅ Correct: `2026-01-15`
- ❌ Wrong: `01/15/2026`
- ❌ Wrong: `15-01-2026`
- ❌ Wrong: `Jan 15, 2026`

### Issue: Assignment not appearing in timeline

**Check these:**

1. **Date format correct?**
   - Use YYYY-MM-DD

2. **End date after start date?**
   - End date must be >= start date

3. **Assignment outside visible range?**
   - Use navigation buttons to move timeline
   - Default view starts Jan 1, 2026

4. **Backend connection?**
   - Check for connection errors
   - Verify backend is running

### Issue: Over-allocation not showing

**Symptoms:**
- Multiple assignments but no red warning
- Heat map not updating

**Solution:**
1. Refresh the page (Ctrl+R or Cmd+R)
2. Check if percentages add up correctly
3. Verify assignments are in the same period

**Example:**
```
Person: Sarah (Jan 15-28)
- Project A: 60% (Jan 10 - Feb 5) ✅ Overlaps
- Project B: 50% (Jan 20 - Feb 10) ✅ Overlaps
Total: 110% ⚠️ Should show red
```

### Issue: Drag & drop not working

**Solutions:**

1. **Browser compatibility:**
   - Use Chrome, Firefox, Safari, or Edge
   - Update to latest version

2. **Assignment card not draggable:**
   - Make sure you click directly on the card
   - Don't click on the × delete button

3. **Drop not working:**
   - Drag over the target cell completely
   - Wait for orange dashed border
   - Release mouse button

### Issue: CSV upload failing

**Common problems:**

1. **Wrong format:**
   ```csv
   # Correct format for assignments:
   personName,projectName,startDate,endDate,percentage
   John Doe,Project A,2026-01-01,2026-01-31,100
   ```

2. **Missing header row:**
   - First row must have column names

3. **Names don't match:**
   - Person and project names must match exactly
   - Check for extra spaces
   - Case-sensitive

4. **Date format wrong:**
   - Must be YYYY-MM-DD
   - No spaces

### Issue: Data disappeared after restart

**Explanation:**
Data is stored in `resource_planner.db` file.

**Solutions:**

1. **Check database file exists:**
   ```bash
   ls -la resource_planner.db
   ```

2. **Run backend in correct directory:**
   ```bash
   cd /mnt/user-data/outputs
   python3 backend.py
   ```

3. **Restore from backup:**
   - Use Export Data feature regularly
   - Import from JSON backup if needed

### Issue: Heat map colors wrong

**Check:**

1. **Allocation calculation:**
   - Each assignment's percentage counts
   - Multiple assignments in same period add up
   
2. **Expected colors:**
   - 0-50% = Green
   - 51-99% = Orange
   - 100%+ = Red

3. **Refresh page:**
   - Ctrl+R or Cmd+R

### Issue: Can't delete assignments

**Solutions:**

1. **× button not appearing:**
   - Hover directly over assignment card
   - Move mouse slowly

2. **Delete not working:**
   - Check backend is running
   - Check browser console for errors

3. **Assignment comes back:**
   - Backend might have crashed
   - Restart backend and try again

### Issue: Epsilon logo not showing

**Solutions:**

1. **File missing:**
   ```bash
   # Check if logo file exists
   ls -la epsilon-logo.png
   ```

2. **Wrong path:**
   - Logo must be in same folder as resource-planner.html

3. **Browser cache:**
   - Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)

## 🔍 Diagnostic Commands

### Check if backend is running:
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "healthy"}
```

### Check database:
```bash
sqlite3 resource_planner.db "SELECT COUNT(*) FROM assignments;"
```

### Check Flask installation:
```bash
python3 -c "import flask; print(flask.__version__)"
```

### View backend logs:
```bash
# Backend shows logs in the terminal where it's running
# Look for errors in that terminal
```

## 📞 Still Having Issues?

1. **Check the documentation:**
   - README.md - Technical reference
   - SETUP-GUIDE.md - Complete setup
   - HOW-TO-USE.md - Quick start

2. **Verify your setup:**
   - Backend running? ✅
   - Port 5000 available? ✅
   - In correct directory? ✅
   - Database file present? ✅

3. **Try a fresh start:**
   ```bash
   # Stop backend (Ctrl+C)
   # Delete database
   rm resource_planner.db
   # Restart
   python3 backend.py
   # Refresh frontend
   ```

## 🎯 Quick Diagnostics Checklist

- [ ] Backend running on port 5000?
- [ ] `resource_planner.db` file exists?
- [ ] Flask and Flask-CORS installed?
- [ ] Using latest version of files?
- [ ] Browser console shows no errors?
- [ ] Dates in YYYY-MM-DD format?
- [ ] Logo file in correct location?

---

**Epsilon Resource Planner v3.0**
Most issues are solved by restarting the backend! 🔄

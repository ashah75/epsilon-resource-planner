# Epsilon Resource Planner - Complete Setup Guide

## 🎯 What You Have

The complete Epsilon Resource Planner system with:
- **Frontend**: Interactive HTML interface with Epsilon branding
- **Backend**: Python Flask REST API
- **Database**: SQLite (free, no setup required)
- **Version**: 3.0 - Date-Based Assignment System

## 📁 Files Included

1. **resource-planner.html** - Main application interface (59K)
2. **backend.py** - Flask API server (9.2K)
3. **epsilon-logo.png** - Epsilon company logo (2.7K)
4. **start-backend.sh** - Startup script (277B)
5. **test-api.html** - API testing page (7.8K)
6. **index.html** - Welcome page (11K)
7. **Documentation files** - Guides and references

## 🚀 Quick Start (3 Steps)

### Step 1: Start the Backend

Open a terminal and run:

```bash
cd /mnt/user-data/outputs
python3 backend.py
```

You should see:
```
🚀 Backend server starting...
📊 Database: SQLite (resource_planner.db)
🌐 API running on: http://localhost:5000
```

**Keep this terminal window open!** The backend needs to keep running.

### Step 2: Test the Backend (Optional but Recommended)

Open `test-api.html` in your browser and click "Run All Tests". 

If all tests pass ✅, your backend is working correctly!

### Step 3: Open the Application

Open `resource-planner.html` in your browser. The application will automatically connect to the backend.

## 💡 How to Use

### Adding Data

1. **Add People** - Click "+ Add Person" to add team members
   - Enter name (e.g., "Sarah Chen")
   - Enter role (e.g., "Senior Consultant")

2. **Add Clients** - Click "+ Add Client" to add client companies
   - Enter client name (e.g., "Acme Corporation")

3. **Add Projects** - Click "+ Add Project" and link it to a client
   - Enter project name (e.g., "Digital Transformation")
   - Select the client

4. **Assign to Projects** - Click "+ Assign to Project"
   - Select team member
   - Select project
   - **📅 Choose start date** (calendar picker)
   - **📅 Choose end date** (calendar picker)
   - Enter percentage (1-100%)

### Date-Based Assignments

**NEW in v3.0:** Use flexible date ranges instead of fixed periods!

**Example 1: Short consultation**
```
Person: John Doe
Project: Quick Review
Start: 2026-01-15
End: 2026-01-17
Percentage: 50%
```

**Example 2: Long project**
```
Person: Jane Smith
Project: Major Implementation
Start: 2026-01-01
End: 2026-03-31
Percentage: 100%
```

**Example 3: Part-time engagement**
```
Person: Bob Johnson
Project: Advisory Services
Start: 2026-01-01
End: 2026-12-31
Percentage: 20%
```

### Understanding the Timeline

- Timeline shows 6 two-week periods (3 months)
- Use "← Prev 3 Months" / "Next 3 Months →" to navigate
- Assignments automatically appear in all periods they overlap
- Color-coded heat map shows allocation levels

### Heat Map Colors

- 🟢 **Green (0-50%)** - Available capacity, can take more work
- 🟠 **Orange (51-99%)** - High utilization, nearly full
- 🔴 **Red (100%+)** - Over-allocated! Needs attention

### Allocation Badges

Each cell shows total allocation:
- `45%` - Green badge, under 50%
- `85%` - Orange badge, high utilization
- `⚠️ 125%` - Red pulsing badge, over-allocated!

### Drag and Drop

Move assignments easily:
1. Click and hold any assignment card
2. Drag to a different person or time period
3. Release to drop
4. Assignment updates instantly!

**Note:** Drag & drop preserves the assignment duration

### Quick Delete

Remove assignments from timeline:
1. Hover over any assignment card
2. Click the `×` button that appears
3. Assignment deleted instantly!

### Uploading Data (CSV)

Click "📤 Upload Data" to bulk import:

**People CSV:**
```csv
name,role
John Doe,Senior Consultant
Jane Smith,Project Manager
Bob Johnson,Analyst
```

**Clients CSV:**
```csv
name
Acme Corporation
Global Tech Inc
Finance Plus
```

**Projects CSV:**
```csv
name,clientName
Digital Transformation,Acme Corporation
Cloud Migration,Global Tech Inc
Risk Assessment,Finance Plus
```

**Assignments CSV:**
```csv
personName,projectName,startDate,endDate,percentage
John Doe,Digital Transformation,2026-01-01,2026-01-31,100
Jane Smith,Cloud Migration,2026-01-15,2026-02-28,50
Bob Johnson,Risk Assessment,2026-02-01,2026-03-15,75
```

**Important:** Dates must be in YYYY-MM-DD format!

### Exporting Data

Click "📥 Export Data" to download a JSON file with all your data. 
Great for backups or reporting!

### Viewing the Timeline

- Each row shows one person
- Each column is a 2-week period
- Assignment cards show project, client, and percentage
- Hover over cards to see full date range
- Heat map colors show utilization at a glance

### Deleting Data

**Delete People, Clients, or Projects:**
- Hover over any item in the sidebar
- Click the red trash icon that appears
- Confirm the deletion

**Important:** 
- Deleting a person removes all their assignments
- Deleting a client removes all its projects and assignments
- Deleting a project removes all assignments to it

## 🔧 Technical Details

### Database

- **Type**: SQLite
- **File**: `resource_planner.db` (created automatically)
- **Location**: Same folder as backend.py
- **Persistence**: All data saved automatically

### API Architecture

```
User Action → Frontend → API Request → Backend → Database
                                                     ↓
User Sees Update ← Frontend ← API Response ← Backend
```

### Data Tables

1. **people** - Team members (name, role)
2. **clients** - Client companies (name)
3. **projects** - Projects (name, client_id)
4. **assignments** - Assignments (person_id, project_id, start_date, end_date, percentage)

## 🐛 Troubleshooting

### "Error connecting to server" message

**Solution**: Make sure the backend is running
1. Open a terminal
2. Run: `python3 backend.py`
3. Look for "API running on: http://localhost:5000"
4. Refresh the frontend

### Backend won't start

**Check**: Do you have Flask installed?
```bash
pip install flask flask-cors --break-system-packages
```

### Data disappeared

**Check**: Is the backend running in the same folder as `resource_planner.db`?
- The database file must be in the same directory as backend.py
- If you moved backend.py, move the .db file with it

### Dates not working

**Check**: Are you using YYYY-MM-DD format?
- Correct: 2026-01-15
- Wrong: 01/15/2026 or 15-01-2026

### Port 5000 already in use

**Solution**: Change the port
1. Edit backend.py, last line: `app.run(debug=True, host='0.0.0.0', port=5001)`
2. Edit resource-planner.html: `const API_BASE_URL = 'http://localhost:5001/api';`

## 📊 Best Practices

### Resource Planning Tips

1. ✅ **Keep allocation at or below 100%** - Over-allocation leads to burnout
2. ✅ **Use the heat map** - Quickly spot problems with red cells
3. ✅ **Plan buffer time** - Aim for 80-90% utilization, not 100%
4. ✅ **Regular exports** - Backup your data weekly
5. ✅ **Consistent dates** - Always use YYYY-MM-DD format

### Allocation Examples

**Perfect balance:**
```
Person: Sarah Chen (Jan 15-28)
- Project A: 50%
- Project B: 50%
Total: 100% ✅
```

**Under-allocated (good!):**
```
Person: Marcus Johnson (Feb 1-14)
- Project C: 60%
Total: 60% 🟢 (40% buffer available)
```

**Over-allocated (fix!):**
```
Person: Emma Rodriguez (Jan 1-14)
- Project X: 70%
- Project Y: 40%
- Project Z: 20%
Total: 130% ⚠️ NEEDS REBALANCING
```

## 🎓 Common Scenarios

### Scenario 1: New Team Member Onboarding
1. Add person with role
2. Assign to orientation/training at 100%
3. Gradually add project assignments
4. Monitor allocation with heat map

### Scenario 2: Multi-Project Consultant
1. Create multiple project assignments
2. Split percentage across projects
3. Use date ranges for project phases
4. Drag & drop to adjust as priorities change

### Scenario 3: Long-Term Advisory
1. Set assignment for full year
2. Use low percentage (10-20%)
3. Appears in all periods automatically
4. Easy to see ongoing commitments

### Scenario 4: Sprint-Based Work
1. Align dates with sprint calendar
2. Set to 100% for sprint duration
3. Use precise start/end dates
4. Timeline shows sprint overlap

## 📚 Additional Resources

- **V3-MIGRATION-GUIDE.md** - Changes in version 3.0
- **architecture.html** - System architecture diagram
- **drag-drop-guide.html** - Interactive feature guide
- **README.md** - Technical API reference
- **CHANGELOG.md** - Version history

## 🎉 You're All Set!

Start planning your resources with:
1. Real-time updates
2. Flexible date ranges
3. Visual heat maps
4. Drag & drop scheduling
5. Over-allocation warnings

**Epsilon Resource Planner v3.0** - Professional team management made easy! 🚀

---

Need help? Check the troubleshooting section or refer to the other documentation files.

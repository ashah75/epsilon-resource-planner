# Epsilon Resource Planner - Quick How-To Guide

## 🚀 Getting Started in 60 Seconds

### 1. Start the Backend (5 seconds)
```bash
python3 backend.py
```
Wait for: "API running on: http://localhost:5000"

### 2. Open the App (5 seconds)
Double-click `resource-planner.html`

### 3. Start Planning! (50 seconds)
You're ready to manage your team resources!

---

## 📋 Common Tasks

### ➕ Add a Team Member

1. Click **"+ Add Person"**
2. Enter **Name**: Sarah Chen
3. Enter **Role**: Senior Consultant
4. Click **"Add Person"**

✅ Done! Sarah appears in the sidebar.

---

### 🏢 Add a Client

1. Click **"+ Add Client"**
2. Enter **Client Name**: Acme Corporation
3. Click **"Add Client"**

✅ Done! Client appears in the sidebar.

---

### 📊 Add a Project

1. Click **"+ Add Project"**
2. Enter **Project Name**: Digital Transformation
3. Select **Client**: Acme Corporation
4. Click **"Add Project"**

✅ Done! Project appears under the client.

---

### 📅 Assign Someone to a Project

1. Click **"+ Assign to Project"**
2. Select **Team Member**: Sarah Chen
3. Select **Project**: Digital Transformation
4. Pick **📅 Start Date**: 2026-01-15
5. Pick **📅 End Date**: 2026-02-28
6. Enter **Percentage**: 75
7. Click **"Assign"**

✅ Done! Assignment appears in the timeline with 75% badge.

---

### 🖱️ Move an Assignment (Drag & Drop)

1. **Click and hold** on any assignment card
2. **Drag** to a different person or time period
3. **Release** to drop

✅ Done! Assignment moved instantly.

---

### 🗑️ Delete an Assignment

1. **Hover** over the assignment card
2. Click the **×** button that appears

✅ Done! Assignment removed.

---

### 📤 Upload Multiple Assignments (CSV)

1. Create a CSV file:
```csv
personName,projectName,startDate,endDate,percentage
Sarah Chen,Digital Transformation,2026-01-01,2026-01-31,100
John Doe,Cloud Migration,2026-02-01,2026-03-15,50
```

2. Click **"📤 Upload Data"**
3. Select **"Assignments"** from dropdown
4. Choose your CSV file
5. Click **"Upload"**

✅ Done! All assignments added at once.

---

### 📥 Export Your Data

1. Click **"📥 Export Data"**
2. Save the JSON file

✅ Done! You have a backup of all your data.

---

## 🎨 Understanding the Timeline

### Heat Map Colors

| Color | Allocation | Meaning |
|-------|-----------|---------|
| 🟢 Green | 0-50% | Available capacity - can take more work |
| 🟠 Orange | 51-99% | High utilization - nearly full |
| 🔴 Red | 100%+ | ⚠️ Over-allocated - needs attention! |

### Allocation Badges

Each timeline cell shows total allocation:
- `45%` - Green badge
- `85%` - Orange badge  
- `⚠️ 125%` - Red pulsing badge (OVER-ALLOCATED!)

### Reading the Timeline

```
Person Name | Jan 1-14 | Jan 15-28 | Jan 29-Feb 11 | ...
───────────────────────────────────────────────────────
Sarah Chen  | [Project A] | [Project A] | [Project B] |
            | 100%        | 50%         | 75%         |
```

---

## 💡 Pro Tips

### ✅ DO
- Keep allocation at or below 100%
- Use 80-90% as target (leave buffer)
- Check heat map regularly for red cells
- Export data weekly for backups
- Use YYYY-MM-DD date format

### ❌ DON'T
- Over-allocate (causes burnout)
- Ignore red warning badges
- Forget to save/export data
- Use wrong date formats

---

## 🎯 Common Scenarios

### Multi-Project Assignment
```
Person: Sarah Chen
Period: Jan 15-28

Assign:
- Project A: 50% (Jan 15 - Feb 28)
- Project B: 30% (Jan 15 - Jan 31)

Result: 80% allocated in Jan 15-28 period
```

### Long-Term Advisory
```
Person: John Doe
Project: Strategic Advisory
Start: 2026-01-01
End: 2026-12-31
Percentage: 15%

Result: 15% shows in ALL periods throughout the year
```

### Sprint Work
```
Person: Jane Smith
Project: Sprint 5
Start: 2026-02-03 (Sprint start)
End: 2026-02-16 (Sprint end)  
Percentage: 100%

Result: Exactly 2 weeks at 100%
```

---

## 🐛 Quick Fixes

### "Error connecting to server"
**Fix**: Start the backend
```bash
python3 backend.py
```

### Assignment not appearing
**Check**: 
- Are dates in YYYY-MM-DD format?
- Is end date after start date?
- Did you click "Assign"?

### Heat map not updating
**Fix**: Refresh the page (Ctrl+R or Cmd+R)

### Lost my data
**Check**: Is `resource_planner.db` in the same folder as backend.py?

---

## 📞 Need More Help?

Check these documents:
- **SETUP-GUIDE.md** - Complete setup instructions
- **README.md** - Technical reference
- **V3-MIGRATION-GUIDE.md** - What's new in v3.0
- **drag-drop-guide.html** - Interactive feature guide

---

## 🎉 You're a Pro Now!

5-Minute Workflow:
1. ✅ Add team members
2. ✅ Add clients & projects
3. ✅ Assign with dates & percentages
4. ✅ Check heat map for over-allocation
5. ✅ Drag & drop to rebalance

**Epsilon Resource Planner v3.0** - Team management made simple! 🚀

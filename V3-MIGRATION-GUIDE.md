# Version 3.0 - Date-Based Assignment System

## 🎉 Major Update: Date Ranges Instead of Periods

The resource planner now uses **flexible date ranges** instead of fixed 2-week periods!

## ✨ What Changed

### Before (v2.0)
- Assignments tied to fixed 2-week periods
- Period 0, Period 1, Period 2, etc.
- Limited flexibility

### Now (v3.0)
- Assignments use **start and end dates**
- Any date range supported (1 day to multiple months)
- Assignments automatically span multiple 2-week periods in the view
- Much more flexible scheduling

## 📅 New Assignment Interface

When you click "+ Assign to Project", you'll now see:

```
Team Member:     [Select person]
Project:         [Select project]
📅 Start Date:   [Date picker with calendar icon]
📅 End Date:     [Date picker with calendar icon]
Percentage:      [1-100%]
```

### Features
- **Calendar icons** for easy date selection
- **Date validation** - End date must be >= Start date
- **Default dates** - Pre-filled with current view's first period
- **Flexible ranges** - Can span days, weeks, or months

## 🗓️ How It Works

### Timeline View
The timeline still shows 2-week periods, but assignments can:
- Start and end on any date
- Span multiple periods
- Overlap periods partially

**Example:**
```
Assignment: Jan 5 - Feb 20, 2026
Appears in:
  ✓ Period 1: Jan 1-14 (partial overlap)
  ✓ Period 2: Jan 15-28 (full overlap)
  ✓ Period 3: Jan 29-Feb 11 (full overlap)
  ✓ Period 4: Feb 12-25 (partial overlap)
```

### Heat Map & Allocation
- Heat map still calculated per 2-week period
- If an assignment overlaps a period, its percentage counts
- Example: 50% assignment spanning 3 periods = 50% in each period

## 📤 CSV Import Format (Updated)

**Old Format:**
```csv
personName,projectName,period,percentage
John Doe,Project A,0,100
```

**New Format:**
```csv
personName,projectName,startDate,endDate,percentage
John Doe,Project A,2026-01-01,2026-01-31,100
Jane Smith,Project B,2026-02-01,2026-03-15,50
```

**Date Format:** YYYY-MM-DD (e.g., 2026-01-15)

## 🖱️ Drag & Drop Update

When you drag an assignment to a new cell:
- The assignment keeps its original duration
- Start date moves to the beginning of the target period
- End date adjusts to maintain duration

**Example:**
```
Original: Jan 10-24 (15 days)
Drag to Period 3 (Jan 29-Feb 11)
Result: Jan 29-Feb 12 (15 days)
```

## 🗄️ Database Changes

### New Schema
```sql
CREATE TABLE assignments (
  id INTEGER PRIMARY KEY,
  person_id INTEGER,
  project_id INTEGER,
  start_date TEXT,      -- New! (YYYY-MM-DD)
  end_date TEXT,        -- New! (YYYY-MM-DD)
  percentage INTEGER
)
```

### Migration Steps

**If you have existing data:**

1. **Export your current data:**
   ```
   Click "📥 Export Data" button
   Save the JSON file
   ```

2. **Stop the backend** (Ctrl+C)

3. **Delete old database:**
   ```bash
   rm resource_planner.db
   ```

4. **Restart backend:**
   ```bash
   python3 backend.py
   ```
   New database with date schema created automatically!

5. **Re-import your data:**
   - Convert periods to dates manually
   - Period 0 → 2026-01-01 to 2026-01-14
   - Period 1 → 2026-01-15 to 2026-01-28
   - Period 2 → 2026-01-29 to 2026-02-11
   - etc.

## ✨ Benefits

### More Flexibility
- ✅ Project can start mid-week
- ✅ Assignment can be 1 day or 6 months
- ✅ Partial period overlap supported
- ✅ Exact date tracking

### Better Accuracy
- ✅ Real start/end dates in database
- ✅ Tooltip shows actual date range
- ✅ More precise reporting
- ✅ Export includes exact dates

### Easier Planning
- ✅ Visual date picker
- ✅ See exactly when assignments run
- ✅ Natural date selection
- ✅ No period number confusion

## 🎯 Examples

### Example 1: Short Assignment
```
Person: Sarah Chen
Project: Quick Consultation
Start: 2026-01-15
End: 2026-01-17
Percentage: 50%

Result: 3-day assignment at 50%
Appears in Period 2 (Jan 15-28)
```

### Example 2: Long Assignment
```
Person: Marcus Johnson
Project: Major Implementation
Start: 2026-01-05
End: 2026-03-20
Percentage: 100%

Result: 2.5-month assignment
Spans multiple periods in timeline view
Heat map shows 100% in all overlapping periods
```

### Example 3: Overlapping Assignments
```
Person: Emma Rodriguez
Period: Jan 15-28 (Period 2)

Assignment A: Jan 10-20 @ 40%
Assignment B: Jan 18-Feb 5 @ 30%
Assignment C: Jan 22-25 @ 20%

Total in Period 2: 90% (all overlap this period)
Heat map: Orange (high utilization)
```

## 🔄 API Changes

### Create Assignment
**Endpoint:** `POST /api/assignments`

**Old Body:**
```json
{
  "personId": 1,
  "projectId": 2,
  "period": 0,
  "percentage": 100
}
```

**New Body:**
```json
{
  "personId": 1,
  "projectId": 2,
  "startDate": "2026-01-01",
  "endDate": "2026-01-31",
  "percentage": 100
}
```

## 📝 Quick Reference

| Feature | Old (v2.0) | New (v3.0) |
|---------|-----------|-----------|
| Assignment Unit | Fixed 2-week period | Flexible date range |
| Date Selection | Period dropdown | Calendar date pickers |
| Duration | Always 2 weeks | Any length (days to months) |
| CSV Format | period number | startDate, endDate |
| Database Field | period (INTEGER) | start_date, end_date (TEXT) |
| Drag & Drop | Change period | Maintains duration, shifts dates |

## 🚀 Getting Started

1. **Delete old database**: `rm resource_planner.db`
2. **Start backend**: `python3 backend.py`
3. **Open app**: resource-planner.html
4. **Click "+ Assign to Project"**
5. **Use the 📅 date pickers!**

## 💡 Tips

- Click calendar icon or date field for date picker
- Assignments can span any timeframe
- Heat map updates automatically
- Tooltip on assignments shows full date range
- Export includes exact dates for reporting

## 🎓 Common Scenarios

### Scenario 1: Part-Time Consultant for Q1
```
Start: 2026-01-01
End: 2026-03-31
Percentage: 50%
Result: 3-month engagement at half-time
```

### Scenario 2: Sprint Team Member
```
Start: 2026-02-03 (Sprint start)
End: 2026-02-16 (Sprint end)
Percentage: 100%
Result: 2-week sprint, exact dates
```

### Scenario 3: Advisory Role
```
Start: 2026-01-01
End: 2026-12-31
Percentage: 10%
Result: Year-long advisory at 10%
```

---

## ⚠️ Breaking Changes

If upgrading from v2.0:
1. Database schema changed (must recreate)
2. CSV import format changed (add date columns)
3. API changed (use dates not periods)
4. Assignment modal changed (date pickers not dropdown)

## 🎉 Version 3.0 is Live!

Experience more flexible, accurate resource planning with date-based assignments!

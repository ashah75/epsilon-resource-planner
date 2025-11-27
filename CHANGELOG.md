# Resource Planner - Changelog

## Version 2.0 - Advanced Allocation Features

### 🎉 New Features

#### 1. Drag and Drop Assignment Scheduling
- **What**: Move assignments between people and time periods by dragging
- **How**: Click and hold any assignment card, drag to target cell, release
- **Benefits**: 
  - Quick reallocation of resources
  - Visual, intuitive interface
  - Instant updates to database
  - No need to delete and recreate assignments

#### 2. Percentage-Based Allocation
- **What**: Assign people to projects with specific allocation percentages (1-100%)
- **Examples**: 
  - 100% = full-time on one project
  - 50% = half-time, can work on two projects
  - 25% = quarter-time for advisory roles
- **Benefits**:
  - Accurate capacity planning
  - Support for multiple concurrent projects
  - Flexible resource allocation
  - Better visibility into workload

#### 3. Heat Map Visualization
- **What**: Color-coded timeline cells showing allocation levels
- **Colors**:
  - 🟢 Green (0-50%): Available capacity
  - 🟠 Orange (51-99%): High utilization  
  - 🔴 Red (100%+): Over-allocated
- **Benefits**:
  - At-a-glance resource overview
  - Quick identification of bottlenecks
  - Visual capacity planning
  - Easy spot over-allocation issues

#### 4. Over-Allocation Detection
- **What**: Automatic alerts when total allocation exceeds 100%
- **Visual Indicators**:
  - Red heat map color
  - Warning badge with ⚠️ icon
  - Pulsing animation for attention
- **Benefits**:
  - Prevent burnout
  - Identify scheduling conflicts
  - Maintain realistic workloads
  - Proactive resource management

#### 5. Allocation Badges
- **What**: Small badges showing total allocation percentage per cell
- **Types**:
  - Green badge: Under 50%
  - Orange badge: 51-99%
  - Red pulsing badge: 100%+
- **Benefits**:
  - Precise allocation numbers
  - Quick capacity checks
  - Easy workload balancing

#### 6. Quick Delete from Timeline
- **What**: Delete assignments directly from timeline cards
- **How**: Hover over assignment, click × button
- **Benefits**:
  - Faster workflow
  - No need to navigate menus
  - One-click removal
  - Immediate visual feedback

### 🔧 Technical Updates

#### Database Schema
- Added `percentage` column to `assignments` table
- Default value: 100
- Type: INTEGER
- Range: 1-100

#### API Endpoints
- Updated `POST /api/assignments` to accept `percentage` parameter
- Updated `POST /api/bulk-upload/assignments` to handle percentage
- All assignment responses now include percentage field

#### Frontend
- New drag-and-drop event handlers
- Heat map calculation engine
- Allocation tracking per person per period
- Real-time visual updates
- Enhanced assignment cards with percentage display

#### CSV Import
- Now supports optional `percentage` column
- Format: `personName,projectName,period,percentage`
- Backwards compatible (defaults to 100% if omitted)

### 📊 Usage Examples

#### Example 1: Split Allocation
```
Sarah Chen:
- Project A: 50% (Period 0)
- Project B: 50% (Period 0)
Total: 100% ✅ Fully allocated
```

#### Example 2: Under-Allocation
```
Marcus Johnson:
- Project C: 30% (Period 1)
Total: 30% 🟢 70% capacity available
```

#### Example 3: Over-Allocation (Warning!)
```
Emma Rodriguez:
- Project A: 60% (Period 2)
- Project B: 50% (Period 2)
- Project C: 20% (Period 2)
Total: 130% ⚠️ OVER-ALLOCATED
```

### 🎯 Use Cases

**Consulting Firm**: Allocate consultants across multiple client projects with accurate time splits

**Agency**: Balance creative team across campaigns with varying time requirements

**Professional Services**: Track utilization rates and identify over/under-allocation

**PMO**: Visualize resource constraints and optimize project timelines

**Resource Manager**: Quick drag-and-drop scheduling with real-time conflict detection

### 📈 Benefits Over Previous Version

| Feature | Before | After |
|---------|--------|-------|
| **Assignment Flexibility** | One project per period | Multiple projects with percentages |
| **Capacity Visibility** | Manual calculation | Automatic with heat map |
| **Over-allocation Detection** | None | Automatic with warnings |
| **Assignment Movement** | Delete + Recreate | Drag and drop |
| **Visual Feedback** | Basic | Color-coded heat map |
| **Workload Balancing** | Time consuming | Quick visual scan |
| **Assignment Deletion** | Menu navigation | One-click from timeline |

### 🔄 Migration Notes

**Existing Database**: If you have an existing `resource_planner.db`:
- Delete the file and restart backend to create new schema
- OR manually add percentage column: `ALTER TABLE assignments ADD COLUMN percentage INTEGER DEFAULT 100`

**Existing Assignments**: All existing assignments will default to 100%

**CSV Files**: Update your CSV templates to include optional percentage column

### 📚 Documentation Updates

New documentation files:
- `drag-drop-guide.html` - Complete guide to new features
- Updated `SETUP-GUIDE.md` with new feature descriptions
- Updated `index.html` with feature links

### 🐛 Bug Fixes

- Improved drag-and-drop visual feedback
- Better handling of empty cells
- Fixed assignment card hover states
- Enhanced mobile responsiveness

### ⚙️ Performance

- Efficient allocation calculations
- Minimal re-rendering on drag
- Optimized heat map color computation
- Fast CSV processing with percentage parsing

### 🔮 Future Enhancements

Potential additions for future versions:
- Multi-week assignment spans
- Resource skill matching
- Availability calendars (holidays, PTO)
- Utilization reports and charts
- Email notifications for over-allocation
- Team capacity planning
- Project demand forecasting
- Historical allocation analytics

---

## Version 1.0 - Initial Release

### Core Features
- Timeline view with 2-week periods
- People, clients, and projects management
- Basic assignment scheduling
- CSV bulk upload
- SQLite database
- REST API
- Real-time updates
- Data persistence

---

**Total Lines of Code**: ~2,500 lines (frontend + backend)
**Database Tables**: 4 (people, clients, projects, assignments)
**API Endpoints**: 15+
**Documentation Pages**: 8

Built with ❤️ using Python, Flask, SQLite, and Vanilla JavaScript

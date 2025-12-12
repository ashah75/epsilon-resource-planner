# React Component Implementation Guide

## 🎯 Overview

This document guides you through implementing the remaining React components. The core structure is in place - you now need to add the detailed implementation for timeline grids and modals.

## 📝 Components to Implement

### 1. Timeline Components

**Location**: `frontend/src/components/timeline/`

#### TimelineGrid.jsx
**Purpose**: Renders the timeline grid with people rows and month columns

**Key Features:**
- Display 6 months as columns
- Show paginated people as rows
- Calculate assignment overlaps with periods
- Handle drag & drop for assignments
- Show allocation badges and colors

**Props:**
```javascript
{
  startIndex: number,  // Pagination start
  endIndex: number     // Pagination end
}
```

**Implementation Tips:**
```javascript
import { useApp } from '../../context/AppContext';
import { getPeriodDates, dateRangeOverlapsPeriod } from '../../utils/dates';
import { getClientColor, getAllocationOpacity } from '../../utils/colors';

export default function TimelineGrid({ startIndex, endIndex }) {
  const { people, projects, clients, assignments, currentPeriodOffset } = useApp();
  
  // Get paginated people
  const paginatedPeople = people.slice(startIndex, endIndex);
  
  // Generate 6 month columns
  const months = [];
  for (let i = 0; i < 6; i++) {
    const monthOffset = Math.floor(currentPeriodOffset / 2) + i;
    const date = new Date(2026, monthOffset, 1);
    months.push({
      offset: monthOffset,
      label: date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }),
      startDate: new Date(2026, monthOffset, 1),
      endDate: new Date(2026, monthOffset + 1, 0)
    });
  }
  
  return (
    <div style={{ /* grid layout */ }}>
      {/* Render headers */}
      {/* Render rows for each person */}
      {/* Render cells with assignments */}
    </div>
  );
}
```

#### TimelineCell.jsx
**Purpose**: Individual cell in timeline showing assignments for one person in one month

**Props:**
```javascript
{
  person: object,
  month: object,
  assignments: array
}
```

#### AssignmentCard.jsx
**Purpose**: Visual card showing single assignment with project name, client, percentage

**Props:**
```javascript
{
  assignment: object,
  project: object,
  client: object,
  onDelete: function,
  onEdit: function
}
```

**Features:**
- Draggable
- Color-coded by client
- Shows percentage badge
- Delete button on hover
- Click to edit

---

### 2. Modal Components

**Location**: `frontend/src/components/modals/`

All modals share similar structure:

```javascript
import { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';

export default function XModal({ isOpen, onClose, editingItem }) {
  const { addX, updateX } = useApp();
  const [formData, setFormData] = useState({ /* fields */ });
  
  useEffect(() => {
    if (editingItem) {
      setFormData(editingItem); // Prefill for editing
    } else {
      setFormData({ /* empty */ }); // Clear for adding
    }
  }, [editingItem, isOpen]);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await updateX(editingItem.id, formData);
      } else {
        await addX(formData);
      }
      onClose();
    } catch (error) {
      alert('Error saving');
    }
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h2 className="modal-title">
          {editingItem ? 'Edit' : 'Add'} X
        </h2>
        <form onSubmit={handleSubmit}>
          {/* Form fields */}
          <div className="form-actions">
            <button type="button" className="btn" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {editingItem ? 'Update' : 'Add'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

#### PersonModal.jsx
**Fields:**
- name (text input)
- role (text input)

#### ClientModal.jsx
**Fields:**
- name (text input)

#### ProjectModal.jsx
**Fields:**
- name (text input)
- clientId (select dropdown)

#### AssignmentModal.jsx
**Fields:**
- personId (select dropdown)
- projectId (select dropdown)
- startDate (date input)
- endDate (date input)
- percentage (number input, 1-100)

**Special Features:**
- Validate end date >= start date
- Default to current timeline view dates
- Show client name with project in dropdown

#### UploadModal.jsx
**Purpose**: Upload CSV files for bulk import

**Features:**
- Upload type selector (People, Clients, Projects, Assignments)
- File input
- CSV parsing using `utils/export.js`
- Progress/error messages
- Format examples for each type

**Implementation:**
```javascript
import { parseCSV } from '../../utils/export';
import { useApp } from '../../context/AppContext';

// Parse CSV and call appropriate bulk upload function
// Show success/error messages
// Handle duplicate detection
```

---

## 🎨 Styling Tips

All components use inline styles with CSS variables:
- `var(--bg-primary)` - Main background
- `var(--bg-secondary)` - Card backgrounds
- `var(--accent-primary)` - Amber accent
- `var(--text-primary)` - Light text
- `var(--border)` - Border color

For reusable styles, add to `styles/globals.css`

---

## 🔗 Connecting Components

### Timeline Flow:
1. **Timeline.jsx** manages state and pagination
2. **TimelineGrid.jsx** renders grid structure
3. **TimelineCell.jsx** renders individual cells
4. **AssignmentCard.jsx** renders assignment cards

### Modal Flow:
1. **App.jsx** manages modal state
2. Pass `openModal(type, item)` to Header/Sidebar
3. Modals read/write via Context
4. Close on successful save

---

## 📦 Context Usage

```javascript
import { useApp } from '../../context/AppContext';

function MyComponent() {
  const {
    // Data
    people, clients, projects, assignments,
    
    // Actions
    addPerson, updatePerson, deletePerson,
    // ... etc
    
    // UI State
    currentPeriodOffset,
    currentPage,
    pageSize
  } = useApp();
  
  // Your component logic
}
```

---

## 🎯 Testing Checklist

Once implemented, test:
- ✅ Add/Edit/Delete people, clients, projects
- ✅ Create assignments with dates
- ✅ Drag assignments to different cells
- ✅ Drag projects from sidebar to timeline
- ✅ Pagination works correctly
- ✅ Over-allocation warnings show
- ✅ CSV upload works
- ✅ Excel export works
- ✅ Timeline navigation works

---

## 💡 Pro Tips

1. **Use React DevTools** - Inspect component props and state
2. **Console.log Context** - Debug data flow issues
3. **Start Simple** - Get basic rendering working first
4. **Copy Patterns** - Similar components (modals) should share structure
5. **Test Incrementally** - Test each component as you build it

---

## 📚 Reference Implementation

The original vanilla JS version (`resource-planner.html`) has all the logic. You're translating it to React components. Key differences:

**Before (Vanilla JS):**
```javascript
function renderTimeline() {
  let html = '<div>';
  // ... build HTML string
  container.innerHTML = html;
}
```

**After (React):**
```javascript
function Timeline() {
  return (
    <div>
      {/* ... JSX markup */}
    </div>
  );
}
```

---

**Ready to implement?** Start with `TimelineGrid.jsx` - it's the most complex but once done, the rest follows naturally!

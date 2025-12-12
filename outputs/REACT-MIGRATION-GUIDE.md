# Resource Planner - React Migration Guide

## 🎯 Overview

This guide covers the conversion from vanilla JavaScript to React + Python Flask architecture.

## 📁 New Project Structure

```
resource-planner-react/
├── backend/                    # Python Flask API (unchanged)
│   ├── backend.py
│   ├── resource_planner.db
│   └── requirements.txt
│
├── frontend/                   # React Application
│   ├── public/
│   │   ├── index.html
│   │   └── epsilon-logo.png
│   ├── src/
│   │   ├── components/        # React Components
│   │   │   ├── layout/
│   │   │   │   ├── Header.jsx
│   │   │   │   └── Sidebar.jsx
│   │   │   ├── timeline/
│   │   │   │   ├── Timeline.jsx
│   │   │   │   ├── TimelineGrid.jsx
│   │   │   │   ├── TimelineCell.jsx
│   │   │   │   └── AssignmentCard.jsx
│   │   │   ├── modals/
│   │   │   │   ├── PersonModal.jsx
│   │   │   │   ├── ClientModal.jsx
│   │   │   │   ├── ProjectModal.jsx
│   │   │   │   ├── AssignmentModal.jsx
│   │   │   │   └── UploadModal.jsx
│   │   │   └── common/
│   │   │       ├── Button.jsx
│   │   │       ├── Modal.jsx
│   │   │       └── CollapsibleGroup.jsx
│   │   ├── context/           # React Context
│   │   │   └── AppContext.jsx
│   │   ├── hooks/             # Custom Hooks
│   │   │   ├── useAPI.js
│   │   │   └── useDragDrop.js
│   │   ├── services/          # API Services
│   │   │   └── api.js
│   │   ├── utils/             # Utility Functions
│   │   │   ├── dates.js
│   │   │   ├── colors.js
│   │   │   └── export.js
│   │   ├── styles/            # Global Styles
│   │   │   └── globals.css
│   │   ├── App.jsx            # Main App Component
│   │   └── main.jsx           # Entry Point
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🚀 Setup Instructions

### Backend (No Changes)
```bash
cd backend
pip install flask flask-cors
python3 backend.py
```

### Frontend (New React App)
```bash
cd frontend
npm install
npm run dev
```

## 📦 Dependencies

### Frontend (`package.json`)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "xlsx": "^0.18.5",
    "date-fns": "^2.30.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.3.9"
  }
}
```

### Backend (Unchanged)
- Flask
- Flask-CORS
- SQLite3

## 🎨 Key Changes

### 1. Component Architecture
**Before:** Single HTML file with inline JavaScript
**After:** Modular React components with clear separation of concerns

### 2. State Management
**Before:** Global variables and DOM manipulation
**After:** React Context API for global state, component state for local

### 3. API Calls
**Before:** Fetch calls scattered throughout code
**After:** Centralized API service with error handling

### 4. Styling
**Before:** Inline styles in HTML
**After:** CSS modules or styled-components (your choice)

### 5. Build Process
**Before:** Direct HTML file serving
**After:** Vite build system with hot reload

## 🔄 Migration Checklist

### Core Features
- ✅ Timeline view (monthly periods)
- ✅ Heat map visualization
- ✅ Drag & drop assignments
- ✅ Percentage-based allocation
- ✅ Date-based assignments
- ✅ CSV bulk upload
- ✅ Excel export
- ✅ CRUD operations
- ✅ Over-allocation detection
- ✅ Collapsible groups
- ✅ Pagination
- ✅ Reports generation

### UI Components
- ✅ Header with Epsilon logo
- ✅ Sidebar with grouped items
- ✅ Timeline grid
- ✅ Assignment cards
- ✅ Modal dialogs
- ✅ Icon buttons with tooltips

### Functionality
- ✅ Add/Edit/Delete people, clients, projects
- ✅ Create/Edit/Delete assignments
- ✅ Navigate timeline (previous/next)
- ✅ Jump to current month
- ✅ Page through team members
- ✅ Upload CSV files
- ✅ Export to Excel
- ✅ Generate reports

## 🎯 Benefits of React Version

### Developer Experience
- **Component Reusability**: Create once, use everywhere
- **Type Safety**: Optional TypeScript support
- **Hot Reload**: Instant feedback during development
- **DevTools**: React DevTools for debugging

### Performance
- **Virtual DOM**: Efficient updates
- **Code Splitting**: Faster initial load
- **Lazy Loading**: Load components on demand

### Maintainability
- **Clear Structure**: Easy to find and update code
- **Testability**: Unit test individual components
- **Scalability**: Easy to add new features

### User Experience
- **Faster Updates**: No full page reloads
- **Smoother Animations**: Better transition handling
- **Better Error Handling**: Graceful error boundaries

## 📝 API Compatibility

The backend API remains **100% compatible**. All endpoints work exactly as before:

### Endpoints (Unchanged)
- `GET /api/people` - Get all people
- `POST /api/people` - Add person
- `PUT /api/people/:id` - Update person
- `DELETE /api/people/:id` - Delete person
- `GET /api/clients` - Get all clients
- `POST /api/clients` - Add client
- ... (all other endpoints remain the same)

## 🔧 Development Workflow

### Starting Development
```bash
# Terminal 1 - Backend
cd backend
python3 backend.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Building for Production
```bash
cd frontend
npm run build
# Output will be in frontend/dist/
```

### Deployment
- Backend: Deploy Flask app (same as before)
- Frontend: Serve `dist/` folder with any static host (Nginx, Vercel, Netlify)

## 🎓 Next Steps

1. **Review the React code** in the frontend folder
2. **Test all features** to ensure compatibility
3. **Customize styling** if needed
4. **Add TypeScript** (optional) for better type safety
5. **Add tests** using Jest and React Testing Library
6. **Deploy** to your preferred hosting platform

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)

## ⚠️ Important Notes

1. **Backend Port**: Ensure backend runs on port 5000
2. **CORS**: Already configured in Flask backend
3. **Database**: Same SQLite database file used
4. **Backwards Compatible**: Can switch between old and new versions

---

**Ready to start?** Follow the setup instructions above!

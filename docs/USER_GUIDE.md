# Continuum - User Guide

**Version**: 0.2.0 (Phase 1 Complete)  
**Last Updated**: November 4, 2025

---

## Getting Started

### Starting the Application

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   source venv/Scripts/activate
   python app.py
   ```
   Backend runs at: http://localhost:5000

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs at: http://localhost:5173

3. **Open in Browser**:
   Navigate to http://localhost:5173

---

## Features

### 1. Category Switching

The top of the page shows 4 category tabs:
- **Business & Finance** 💼 - Bill payments and financial tasks
- **Coding Projects** 💻 - Development work and GitHub issues
- **Health & Life** ❤️ - Personal wellness and habits
- **Communications** ✉️ - Email management and follow-ups

Click any tab to switch categories. Each category has its own set of cards.

### 2. Kanban Board

Each category displays a kanban board with 3 columns:
- **To Do** - Tasks not yet started
- **In Progress** - Tasks currently being worked on
- **Done** - Completed tasks

The number badge on each column shows how many cards it contains.

### 3. Creating Cards

1. Click the **"+ New Card"** button in the top right
2. Fill out the card form:
   - **Title** (required) - Brief description of the task
   - **Description** (optional) - Detailed information
   - **Column** - Which column to place the card in (To Do, In Progress, Done)
   - **Priority** - Low, Medium, or High
   - **Tags** - Comma-separated keywords (e.g., "frontend, urgent, bug")
3. Click **"Create"**

### 4. Editing Cards

1. Click the ✏️ (pencil) icon on any card
2. Modify any field in the modal
3. Click **"Update"** to save changes

### 5. Deleting Cards

1. Click the 🗑️ (trash) icon on any card
2. Confirm the deletion in the popup
3. The card will be permanently removed

### 6. Drag and Drop

You can move cards between columns by dragging:
1. Click and hold on a card
2. Drag it to another column
3. Release to drop

The card will automatically update its status and save to local storage.

### 7. Card Details

Each card displays:
- **Title** - Main task description (bold)
- **Description** - Additional details (gray text)
- **Tags** - Blue badge labels
- **Priority Indicator** - Colored left border:
  - 🔴 Red = High priority
  - 🟠 Orange = Medium priority
  - 🟢 Green = Low priority
- **Updated Date** - Last modification timestamp
- **Action Buttons** - Edit and delete icons

---

## Data Persistence

Your cards are automatically saved to **browser local storage**:
- ✅ Data persists across browser sessions
- ✅ Data is stored locally on your computer
- ✅ Each category's cards are saved separately
- ✅ No internet connection required

**Note**: Local storage data is browser-specific. If you:
- Clear browser data/cache → Cards will be lost
- Use a different browser → Cards won't appear
- Use incognito mode → Cards won't persist

In Phase 2, we'll add a backend database for cloud storage.

---

## Keyboard Shortcuts

Currently no keyboard shortcuts implemented. This may be added in future updates.

---

## Mobile Usage

The app is fully responsive and works on mobile devices:
- Category tabs show icons only on small screens
- Cards stack vertically for easier scrolling
- Touch and drag works for moving cards
- Modal forms adapt to smaller screens

---

## Tips & Best Practices

### Organizing Tasks

1. **Use Priority Wisely**:
   - High: Urgent and important
   - Medium: Important but not urgent
   - Low: Nice to have

2. **Tag Effectively**:
   - Use consistent tag names (e.g., always "frontend" not "front-end")
   - Keep tags short (1-2 words)
   - Common tag examples: "bug", "feature", "urgent", "backend", "frontend", "research"

3. **Write Clear Titles**:
   - Start with action verbs: "Fix...", "Add...", "Update...", "Research..."
   - Keep under 50 characters
   - Be specific: "Fix login button styling" vs "Fix button"

4. **Use Descriptions**:
   - Add links to related resources
   - List acceptance criteria
   - Include blockers or dependencies

### Workflow

**Coding Projects Category**:
```
To Do → In Progress → Done
  ↓         ↓           ↓
Plan → Code/Test → Deployed
```

**Business & Finance Category**:
```
To Do → In Progress → Done
  ↓         ↓           ↓
Due → Processing → Paid
```

**Health & Life Category**:
```
To Do → In Progress → Done
  ↓         ↓           ↓
Planned → Doing → Completed
```

**Communications Category**:
```
To Do → In Progress → Done
  ↓         ↓           ↓
Needs Reply → Drafting → Sent
```

---

## Troubleshooting

### Cards Not Saving

**Problem**: Cards disappear after browser refresh  
**Solution**: 
- Check browser console (F12) for localStorage errors
- Ensure you're not in incognito/private mode
- Check if localStorage is enabled in browser settings

### Drag and Drop Not Working

**Problem**: Can't move cards between columns  
**Solution**:
- Refresh the page
- Check browser console for JavaScript errors
- Ensure you're using a modern browser (Chrome, Firefox, Edge, Safari)

### Backend API Not Responding

**Problem**: Backend health check fails  
**Solution**:
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Restart backend
cd backend
source venv/Scripts/activate
python app.py
```

### Frontend Not Loading

**Problem**: Vite dev server won't start  
**Solution**:
```bash
# Check if port 5173 is in use
netstat -ano | findstr :5173

# Restart frontend
cd frontend
npm run dev
```

---

## Data Export (Coming in Phase 2)

Currently, there's no export feature. In Phase 2, we'll add:
- JSON export/import
- CSV export
- Public portfolio sharing
- Backend database sync

---

## What's Next?

### Phase 2 (Weeks 3-4) - Coming Soon
- Backend REST API for card storage
- PostgreSQL database
- Docker containerization
- Kubernetes deployment

### Phase 3 (Weeks 5-6) - Future
- GitHub integration (auto-import issues)
- Plaid integration (bill payment tracking)
- Gmail integration (email task creation)

### Phase 4 (Weeks 7-8) - Future
- Public portfolio export
- CI/CD pipeline
- Automated testing

### Phase 5 (Weeks 9-10) - Future
- Multi-cloud deployment (GCP + Azure)
- Monitoring and logging
- Cost optimization

---

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/aandrx/continuum
- Documentation: See `docs/` folder
- Implementation Plan: `docs/IMPLEMENTATION_PLAN.md`

---

**Built with**: Vue.js 3, TypeScript, Pinia, Vite, Python Flask  
**License**: MIT  
**Author**: aandrx

# Continuum - Testing Guide

## Quick Testing Steps

### 1. Test Frontend (Vue.js)

**Start the frontend:**
```bash
cd frontend
npm run dev
```

**Expected output:**
```
VITE v7.x.x  ready in XXXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Test in browser:**
- Open http://localhost:5173/
- You should see the default Vue.js welcome page
- Check browser console for any errors (F12 -> Console)

**Tests to verify:**
- [ ] Page loads without errors
- [ ] No console errors
- [ ] Hot reload works (edit a file and see changes)

---

### 2. Test Backend (Python/Flask)

**Setup backend (first time only):**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

**Start the backend:**
```bash
cd backend
source venv/bin/activate  # On macOS/Linux
python app.py
```

**Expected output:**
```
Continuum API starting on 0.0.0.0:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

**Test API endpoints:**

Open a new terminal and run:

```bash
# Test health check
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","service":"continuum-api","version":"0.1.0"}

# Test categories endpoint
curl http://localhost:5000/api/categories

# Expected response: JSON array with 4 categories
```

**Or test in browser:**
- http://localhost:5000/api/health
- http://localhost:5000/api/categories

**Tests to verify:**
- [ ] Server starts without errors
- [ ] Health endpoint returns JSON
- [ ] Categories endpoint returns 4 categories
- [ ] CORS is enabled (check response headers)

---

### 3. Test Frontend + Backend Integration

**With both servers running:**

1. **Frontend** (http://localhost:5173/)
2. **Backend** (http://localhost:5000/)

**Add this test to frontend:**

Create `frontend/src/services/api.ts`:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export async function testConnection() {
  const response = await fetch(`${API_URL}/api/health`)
  return response.json()
}

export async function getCategories() {
  const response = await fetch(`${API_URL}/api/categories`)
  return response.json()
}
```

**Test in browser console:**
```javascript
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(console.log)
// Should log: {status: "healthy", service: "continuum-api", version: "0.1.0"}
```

---

### 4. Test with Docker Compose (Optional)

**Build and start:**
```bash
docker-compose up --build
```

**Note:** Docker files need to be created first (Phase 2)

---

## Automated Testing

### Frontend Tests
```bash
cd frontend
npm run test:unit     # Run unit tests
npm run lint          # Check code quality
npm run type-check    # Check TypeScript types
```

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest                # Run tests (when test files are added)
flake8 .             # Check code style
black --check .      # Check formatting
```

---

## Common Issues & Solutions

### Frontend won't start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend won't start
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Port already in use
```bash
# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9

# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9
```

### CORS errors
- Check that CORS_ORIGINS in backend/.env includes your frontend URL
- Default: `CORS_ORIGINS=http://localhost:5173,http://localhost:3000`

---

## Manual Test Checklist

### Initial Setup
- [ ] Node.js installed and working
- [ ] Python 3.9+ installed and working
- [ ] Git repository initialized
- [ ] Dependencies installed (frontend and backend)

### Frontend
- [ ] Dev server starts successfully
- [ ] Page loads at http://localhost:5173/
- [ ] No console errors
- [ ] Hot reload works
- [ ] TypeScript compiles without errors

### Backend
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Server starts on port 5000
- [ ] Health endpoint responds
- [ ] Categories endpoint returns data
- [ ] CORS headers present

### Integration
- [ ] Frontend can call backend API
- [ ] No CORS errors in browser console
- [ ] API responses are valid JSON
- [ ] Error handling works

---

## Next Steps After Testing

Once everything is working:

1. **Commit your working setup:**
```bash
git add .
git commit -m "feat: working frontend and backend setup"
git push origin main
```

2. **Update IMPLEMENTATION_PLAN.md:**
   - Mark setup tasks as complete
   - Add any notes about issues encountered

3. **Start Phase 1 development:**
   - Build category switcher component
   - Create kanban board layout
   - Implement card components

---

## Quick Reference

**Frontend URL**: http://localhost:5173/  
**Backend URL**: http://localhost:5000/  
**Health Check**: http://localhost:5000/api/health  
**Categories API**: http://localhost:5000/api/categories  

**Stop Servers**: Press `Ctrl+C` in each terminal

**Status**: Setup Complete - Ready for Development!

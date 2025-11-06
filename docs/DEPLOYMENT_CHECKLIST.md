# ✅ Deployment Checklist - Render + Vercel

Follow this checklist as you deploy. Check off each step!

---

## 📋 Pre-Deployment (1 minute)

- [ ] All changes committed and pushed to GitHub
- [ ] Terminal ready
- [ ] Browser open to https://render.com

---

## 🔧 Backend on Render (5 minutes)

### Account Setup
- [ ] Go to https://render.com
- [ ] Click "Get Started"
- [ ] Sign up with GitHub
- [ ] Authorize Render access

### Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect "continuum" repository
- [ ] Click "Connect"

### Configuration
Fill out these fields:

- [ ] **Name**: `continuum-api`
- [ ] **Region**: Select closest to you
- [ ] **Branch**: `main`
- [ ] **Root Directory**: `backend`
- [ ] **Runtime**: Python 3
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `gunicorn app:app`
- [ ] **Instance Type**: Free

### Environment Variables
- [ ] Click "Add Environment Variable"
- [ ] Add `FLASK_ENV` = `production`
- [ ] Add `DATABASE_URL` = `sqlite:///continuum.db`
- [ ] Add `PYTHON_VERSION` = `3.11.0` (optional)

### Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (~2-3 min)
- [ ] ✅ See "Live" status

### Test
- [ ] Copy your URL: `https://continuum-api-XXXX.onrender.com`
- [ ] Open URL + `/api/health` in browser
- [ ] ✅ See JSON response with "healthy" status

**Save this URL:** ________________________________

---

## 🎨 Frontend on Vercel (3 minutes)

### Install Vercel CLI
- [ ] Open terminal
- [ ] Run: `npm install -g vercel`
- [ ] Wait for installation

### Configure
- [ ] Run: `cd /c/Users/andrx/Documents/VSCode/continuum/frontend`
- [ ] Create .env.production:
  ```bash
  echo "VITE_API_URL=https://YOUR-RENDER-URL/api" > .env.production
  ```
  **⚠️ Replace YOUR-RENDER-URL with actual URL from backend**

### Deploy
- [ ] Run: `vercel --prod`
- [ ] Answer questions:
  - [ ] Set up and deploy? → `Y`
  - [ ] Which scope? → Select your username
  - [ ] Link to existing project? → `N`
  - [ ] Project name? → `continuum`
  - [ ] Directory? → `./` (press Enter)
  - [ ] Modify settings? → `N`

### Verify
- [ ] Copy Production URL: `https://continuum-XXXX.vercel.app`
- [ ] Open in browser
- [ ] ✅ See Continuum kanban board

**Save this URL:** ________________________________

---

## 🔗 Configure CORS (1 minute)

- [ ] Go to Render dashboard
- [ ] Click "continuum-api" service
- [ ] Click "Environment" (left sidebar)
- [ ] Click "Add Environment Variable"
- [ ] Add `CORS_ORIGINS` = `https://YOUR-VERCEL-URL,http://localhost:5173`
  **⚠️ Replace YOUR-VERCEL-URL with actual Vercel URL**
- [ ] Click "Save Changes"
- [ ] Wait for auto-redeploy (~1 min)

---

## ✅ Final Testing

### Test Backend
- [ ] Open: `https://YOUR-RENDER-URL/api/health`
- [ ] ✅ Returns JSON with status "healthy"
- [ ] Open: `https://YOUR-RENDER-URL/api/categories`
- [ ] ✅ Returns array of 4 categories

### Test Frontend
- [ ] Open your Vercel URL in browser
- [ ] Open browser console (F12)
- [ ] Click "Business" tab
- [ ] Click "+" button
- [ ] Create a test card
- [ ] ✅ Card appears (no errors in console)
- [ ] Refresh page
- [ ] ✅ Card still there

### Test Integration
- [ ] Create another card
- [ ] Move it to "In Progress"
- [ ] ✅ Drag and drop works
- [ ] Refresh page
- [ ] ✅ Card is still in "In Progress"

---

## 🎉 Success!

If all checkboxes are checked, your app is live!

### Your URLs:
**Backend:** ________________________________  
**Frontend:** ________________________________

### Share Your App:
- Send the frontend URL to friends
- Add to your resume/portfolio
- Post on LinkedIn/Twitter

---

## 📝 Next Steps

- [ ] Bookmark your URLs
- [ ] Set up monitoring (optional)
- [ ] Continue with Week 4: Authentication
- [ ] Consider custom domain (optional)

---

## ⚠️ Troubleshooting

If you encounter issues, check the matching step in `RENDER_WALKTHROUGH.md` for detailed solutions.

**Common issues:**
- Connection failed → Check .env.production has correct URL
- CORS error → Update CORS_ORIGINS on Render
- Backend slow → Render free tier wakes up on first request
- Build failed → Check Render logs for errors

---

**Time to completion:** ~10 minutes  
**Cost:** $0  
**Auto-updates:** Every git push

Ready? Let's go! 🚀

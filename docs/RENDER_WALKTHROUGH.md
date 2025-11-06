# 🚀 Complete Render Deployment Walkthrough

## What You'll Deploy
- **Backend API** → Render Web Service (Free tier)
- **Frontend** → Vercel (Free tier)
- **Total time**: ~10 minutes
- **Cost**: $0

---

## Part 1: Deploy Backend to Render (5 minutes)

### Step 1: Create Render Account

1. **Go to** https://render.com
2. **Click "Get Started"** (top right)
3. **Sign up with GitHub**
   - Click "Sign up with GitHub"
   - Authorize Render to access your repos
   - ✅ This connects your GitHub account

### Step 2: Create New Web Service

1. **Click "New +"** (top right, blue button)
2. **Select "Web Service"** from dropdown
3. **Connect a repository**:
   - You should see a list of your GitHub repos
   - Find and click **"continuum"** repo
   - If you don't see it, click "Configure account" → Select repos → Add "continuum"
   - Click "Connect"

### Step 3: Configure Web Service

You'll see a configuration form. Fill it out exactly like this:

#### **Basic Settings:**
```
Name: continuum-api
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: backend
```

#### **Build & Deploy:**
```
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

⚠️ **Important**: The start command must be exactly `gunicorn app:app` (no extra flags)

#### **Plan:**
```
Instance Type: Free
```
(This gives you 750 hours/month free)

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section:

1. **Click "Add Environment Variable"**
2. Add these two variables:

**Variable 1:**
```
Key: FLASK_ENV
Value: production
```

**Variable 2:**
```
Key: DATABASE_URL
Value: sqlite:///continuum.db
```

**Variable 3 (Optional but recommended):**
```
Key: PYTHON_VERSION
Value: 3.11.0
```

### Step 5: Create Web Service

1. **Scroll to bottom**
2. **Click "Create Web Service"** (big blue button)
3. **Wait for deployment** (~2-3 minutes)

You'll see a deployment log streaming:
```
=== Installing dependencies ===
Collecting flask...
✓ Successfully installed flask-3.0.0
=== Starting service ===
[INFO] Booting worker with pid: 1
[INFO] Listening at: http://0.0.0.0:10000
```

### Step 6: Get Your Backend URL

Once deployment succeeds:

1. **Look at the top** of the page
2. **Copy your URL**: It will be like `https://continuum-api.onrender.com`
3. **Save this URL** - you'll need it for frontend setup

### Step 7: Test Your Backend

**In your browser, visit:**
```
https://continuum-api.onrender.com/api/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "continuum-api",
  "version": "0.1.0"
}
```

✅ **Backend is live!**

---

## Part 2: Deploy Frontend to Vercel (3 minutes)

### Step 8: Install Vercel CLI

**Open your terminal** and run:
```bash
npm install -g vercel
```

Wait for installation to complete (~30 seconds).

### Step 9: Configure Frontend

**Navigate to frontend directory:**
```bash
cd /c/Users/andrx/Documents/VSCode/continuum/frontend
```

**Create production environment file:**
```bash
echo "VITE_API_URL=https://continuum-api.onrender.com/api" > .env.production
```

⚠️ **Replace `continuum-api.onrender.com` with YOUR actual Render URL from Step 6**

### Step 10: Deploy to Vercel

**Run deployment command:**
```bash
vercel --prod
```

You'll be asked several questions. **Answer like this:**

**Question 1:**
```
? Set up and deploy "~/continuum/frontend"? [Y/n]
```
**Answer:** `Y` (press Enter)

**Question 2:**
```
? Which scope do you want to deploy to?
```
**Answer:** Select your username (use arrow keys, press Enter)

**Question 3:**
```
? Link to existing project? [y/N]
```
**Answer:** `N` (press Enter)

**Question 4:**
```
? What's your project's name?
```
**Answer:** `continuum` (press Enter)

**Question 5:**
```
? In which directory is your code located?
```
**Answer:** `./` (press Enter - it's already in frontend directory)

**Question 6:**
```
? Want to modify these settings? [y/N]
```
**Answer:** `N` (press Enter)

### Step 11: Wait for Deployment

You'll see output like:
```
🔗  Linked to username/continuum
🔍  Inspect: https://vercel.com/...
✅  Production: https://continuum-xyz123.vercel.app
```

**Copy the Production URL** - this is your live frontend!

### Step 12: Test Your Frontend

1. **Open your Vercel URL** in browser
2. You should see the Continuum kanban board
3. **Try creating a card:**
   - Click "Business" tab
   - Click "+" button
   - Fill in card details
   - Click "Create"
4. **Refresh the page**
5. Card should still be there ✅

---

## Part 3: Configure CORS (1 minute)

Your frontend can now talk to backend, but we need to whitelist your domain.

### Step 13: Update CORS Settings

1. **Go back to Render dashboard**: https://dashboard.render.com
2. **Click on "continuum-api"** service
3. **Click "Environment"** (left sidebar)
4. **Click "Add Environment Variable"**
5. Add this variable:

```
Key: CORS_ORIGINS
Value: https://continuum-xyz123.vercel.app,http://localhost:5173
```

⚠️ **Replace `continuum-xyz123.vercel.app` with YOUR actual Vercel URL**

6. **Click "Save Changes"**

The service will automatically redeploy (~1 minute).

### Step 14: Test Everything

1. **Open your Vercel URL** again
2. **Open browser console** (F12)
3. **Try creating a card**
4. You should see **no CORS errors**
5. Card appears and persists on refresh ✅

---

## 🎉 You're Done!

### Your Live URLs:

**Backend API:**
```
https://continuum-api.onrender.com
```

**Frontend App:**
```
https://continuum-xyz123.vercel.app
```

**Test Endpoints:**
- Health: https://continuum-api.onrender.com/api/health
- Categories: https://continuum-api.onrender.com/api/categories
- Cards: https://continuum-api.onrender.com/api/cards

---

## Post-Deployment

### Automatic Updates

Every time you `git push` to main:
- **Render**: Auto-deploys backend (~2-3 min)
- **Vercel**: Auto-deploys frontend (~1 min)

**No manual steps needed!** Just code and push.

### Manual Updates

**Update frontend only:**
```bash
cd frontend
vercel --prod
```

**Update backend:**
- Just `git push` - Render watches your repo

---

## Common Issues & Solutions

### Issue 1: "Connection failed" in frontend

**Cause:** Wrong API URL in .env.production

**Fix:**
```bash
cd frontend
echo "VITE_API_URL=https://YOUR-RENDER-URL/api" > .env.production
vercel --prod
```

### Issue 2: "CORS error" in browser console

**Cause:** Vercel URL not in CORS_ORIGINS

**Fix:**
1. Render dashboard → continuum-api → Environment
2. Update CORS_ORIGINS to include your Vercel URL
3. Save (auto-redeploys)

### Issue 3: Backend is very slow

**Cause:** Render free tier spins down after 15 min inactivity

**Solution:** 
- First request wakes it up (~30 seconds)
- This is normal for free tier
- Upgrade to paid tier ($7/month) for always-on

### Issue 4: "Build failed" on Render

**Cause:** Missing dependencies or wrong Python version

**Fix:**
1. Check Render logs for error
2. Verify `requirements.txt` has all dependencies
3. Set PYTHON_VERSION env var to `3.11.0`

### Issue 5: Data disappears on backend restart

**Cause:** SQLite database not persisting on Render free tier

**Solution:**
- This is expected with file-based SQLite on ephemeral storage
- Upgrade to PostgreSQL in Week 4 (authentication)
- Or upgrade to paid Render tier with persistent disk

---

## Monitoring Your Deployment

### Render Dashboard

**View logs:**
1. Render dashboard → continuum-api
2. Click "Logs" tab
3. See real-time server logs

**View metrics:**
1. Click "Metrics" tab
2. See CPU, memory, request rates

### Vercel Dashboard

**View deployments:**
1. https://vercel.com/dashboard
2. Click "continuum" project
3. See all deployments and logs

**View analytics:**
1. Click "Analytics" tab
2. See visitor stats, performance

---

## Next Steps

### Week 4: Add Authentication

Your app is deployed and works great! Now continue with:

1. **Read** `docs/AUTHENTICATION.md`
2. **Implement** user login/register
3. **Upgrade** to PostgreSQL for data persistence
4. **Deploy** updated code (auto-deploys on push!)

### Optional Improvements

1. **Custom domain:**
   - Buy domain on Namecheap/Google Domains
   - Configure in Vercel settings
   - `continuum.yourdomain.com`

2. **Better database:**
   - Add PostgreSQL on Render (free tier available)
   - Update DATABASE_URL environment variable
   - Data persists forever

3. **Monitoring:**
   - Add Sentry for error tracking
   - Set up uptime monitoring (UptimeRobot)
   - Configure email alerts

---

## Costs

### Current Setup (Free):
- Render: 750 hours/month
- Vercel: Unlimited deployments
- **Total: $0/month** ✅

### If You Outgrow Free Tier:
- Render Starter: $7/month (always-on, more resources)
- Vercel Pro: $20/month (more bandwidth, team features)
- PostgreSQL: Free on Render, or $7/month for larger DB

---

## Quick Reference

### Render Service Settings:
```
Name: continuum-api
Runtime: Python 3
Root Directory: backend
Build: pip install -r requirements.txt
Start: gunicorn app:app
Environment:
  FLASK_ENV=production
  DATABASE_URL=sqlite:///continuum.db
  CORS_ORIGINS=https://your-vercel-url.vercel.app
```

### Vercel Deployment:
```bash
cd frontend
echo "VITE_API_URL=https://your-render-url.onrender.com/api" > .env.production
vercel --prod
```

---

## Getting Help

**Render Issues:**
- Docs: https://render.com/docs
- Community: https://community.render.com

**Vercel Issues:**
- Docs: https://vercel.com/docs
- Support: support@vercel.com

**This Project:**
- Check `docs/QUICK_DEPLOY.md`
- Check GitHub issues
- Review Render/Vercel logs

---

**Ready to deploy?** Start with Step 1! 🚀

Each step takes about 1 minute, and you'll have a live app in 10 minutes total.

# 🚀 DEPLOY NOW - Copy/Paste Commands

## Fastest Path (10 minutes total)

### Option A: Render (Backend) + Vercel (Frontend) - RECOMMENDED

#### 1. Backend on Render (Web UI - 5 min)
```
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select "aandrx/continuum" repo
5. Configure:
   - Name: continuum-api
   - Root Directory: backend
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
6. Add Environment Variables:
   - FLASK_ENV = production
   - DATABASE_URL = sqlite:///continuum.db
7. Click "Create Web Service"
8. Copy your URL: https://continuum-api-XXXX.onrender.com
```

#### 2. Frontend on Vercel (CLI - 3 min)
```bash
# Install Vercel CLI
npm install -g vercel

# Go to frontend
cd frontend

# Set backend URL (use YOUR Render URL from step 1)
echo "VITE_API_URL=https://continuum-api-XXXX.onrender.com/api" > .env.production

# Deploy
vercel --prod
# Answer: Y, N, continuum, Enter, N

# Copy your URL: https://continuum-XXXX.vercel.app
```

#### 3. Update CORS (1 min)
```
Go back to Render dashboard → continuum-api → Environment
Add: CORS_ORIGINS = https://continuum-XXXX.vercel.app
(Use YOUR Vercel URL from step 2)
Save → Auto redeploys
```

**✅ DONE! Open your Vercel URL in browser**

---

### Option B: All Azure (Requires Azure CLI)

```bash
# Login to Azure
az login

# Deploy backend (5 min)
az group create --name continuum-rg --location eastus
az appservice plan create --name continuum-plan --resource-group continuum-rg --sku F1 --is-linux
az webapp create --resource-group continuum-rg --plan continuum-plan --name continuum-api-$(whoami) --runtime "PYTHON:3.11"
az webapp config set --resource-group continuum-rg --name continuum-api-$(whoami) --startup-file "gunicorn app:app"

# Deploy code
cd backend
zip -r deploy.zip . -x "venv/*" -x "__pycache__/*" -x "*.pyc" -x "*.db"
az webapp deployment source config-zip --resource-group continuum-rg --name continuum-api-$(whoami) --src deploy.zip

# Get URL
echo "Backend: https://continuum-api-$(whoami).azurewebsites.net"

# Deploy frontend to Vercel (same as Option A step 2)
```

---

## Post-Deployment

**Test Backend:**
```bash
curl https://YOUR-BACKEND-URL/api/health
```

**Test Frontend:**
Open browser → https://YOUR-FRONTEND-URL

**Create a card:**
1. Click "Business" tab
2. Click "+"
3. Add card
4. Refresh page
5. Card should still be there ✅

---

## Auto-Deploy on Push

Once deployed, every `git push` to main automatically deploys:
- Vercel: ~1 minute
- Render: ~2-3 minutes

Just code and push! 🚀

---

## Costs

**FREE TIER:**
- Render: 750 hours/month
- Vercel: Unlimited
- Azure: F1 tier free

**Total: $0** ✅

---

## Troubleshooting

**"Connection failed"**
→ Check .env.production has correct URL
→ Rebuild: `vercel --prod`

**"CORS error"**
→ Update CORS_ORIGINS on Render
→ Include your Vercel URL

**Backend slow?**
→ Render free tier sleeps after 15 min
→ First request wakes it (~30s)

---

**Need help?** Check `docs/QUICK_DEPLOY.md` for detailed guide

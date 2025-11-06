# 🚀 Quick Deployment - 10 Minutes to Live

## Fastest Method: Vercel (Frontend) + Render (Backend)

This is the **absolute fastest** way to get your app online. Both services have free tiers and automatic deployments.

---

## Step 1: Deploy Backend to Render (5 minutes)

1. **Go to** https://render.com and sign up (free)

2. **Click "New +"** → **"Web Service"**

3. **Connect your GitHub repo** `aandrx/continuum`

4. **Configure the service:**
   ```
   Name: continuum-api
   Region: (Choose closest to you)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

5. **Click "Advanced"** and add environment variables:
   ```
   FLASK_ENV = production
   DATABASE_URL = sqlite:///continuum.db
   ```

6. **Click "Create Web Service"**

7. **Wait 2-3 minutes** for deployment. You'll get a URL like:
   ```
   https://continuum-api.onrender.com
   ```

8. **Test it:**
   ```bash
   curl https://continuum-api.onrender.com/api/health
   ```

✅ **Backend is live!**

---

## Step 2: Deploy Frontend to Vercel (3 minutes)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

3. **Update API URL:**
   ```bash
   echo "VITE_API_URL=https://continuum-api.onrender.com/api" > .env.production
   ```

4. **Deploy:**
   ```bash
   vercel --prod
   ```

5. **Follow prompts:**
   - Setup and deploy? **Y**
   - Which scope? (Your account)
   - Link to existing project? **N**
   - Project name? **continuum**
   - Directory? **./frontend** (press Enter)
   - Override settings? **N**

6. **Wait 1-2 minutes**. You'll get a URL like:
   ```
   https://continuum-xyz123.vercel.app
   ```

✅ **Frontend is live!**

---

## Step 3: Update CORS (1 minute)

Go back to Render dashboard:

1. Click your `continuum-api` service
2. Go to **Environment**
3. Add new variable:
   ```
   CORS_ORIGINS = https://continuum-xyz123.vercel.app,http://localhost:5173
   ```
   (Replace with your actual Vercel URL)
4. Click **Save Changes**
5. Service will automatically redeploy

✅ **All done!**

---

## Test Your Deployed App

1. **Open your Vercel URL** in browser
2. **Try creating a card**
3. **Refresh the page** - card should persist!

---

## Deployment URLs

You now have:
- **Frontend:** https://continuum-xyz123.vercel.app
- **Backend:** https://continuum-api.onrender.com
- **API Docs:** https://continuum-api.onrender.com/api/health

---

## Future Updates

Every time you push to `main` branch:
- **Vercel:** Auto-deploys frontend (takes 1-2 min)
- **Render:** Auto-deploys backend (takes 2-3 min)

Or manually:
```bash
cd frontend && vercel --prod    # Update frontend
# Backend updates automatically from GitHub
```

---

## Costs

- **Render Free Tier:** ✅ 750 hours/month (plenty for personal use)
- **Vercel Free Tier:** ✅ Unlimited deployments
- **Total:** **$0/month** 🎉

⚠️ **Note:** Render free tier spins down after 15 min inactivity. First request after sleep takes ~30s.

---

## Troubleshooting

**Backend not responding?**
- Check Render logs in dashboard
- Verify `gunicorn` is installed in requirements.txt ✅

**Frontend can't connect to backend?**
- Check `.env.production` has correct API URL
- Verify CORS_ORIGINS includes your Vercel URL
- Rebuild frontend: `vercel --prod`

**Database resets?**
- This is expected with SQLite on Render free tier
- Upgrade to PostgreSQL in Week 4 (authentication) for persistence

---

## Next Steps

After deployment works:
1. ✅ Share the URL with friends!
2. ✅ Continue with Week 4 - Authentication
3. ✅ Upgrade to PostgreSQL for permanent storage
4. ✅ Add custom domain (optional)

---

**Ready?** Run these commands:

```bash
# 1. Deploy backend on Render.com (web interface)
# 2. Then run:
cd frontend
echo "VITE_API_URL=https://YOUR-RENDER-URL/api" > .env.production
npm install -g vercel
vercel --prod
```

That's it! 🚀

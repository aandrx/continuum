# Deployment Guide - Quick Start

## Deploy to Azure (Recommended - Free Tier Available)

### Option 1: Azure Portal (Easiest - 10 minutes)

#### Backend (Azure App Service)

1. **Create Azure App Service**
   ```bash
   # Install Azure CLI if not installed
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   
   # Login
   az login
   
   # Create resource group
   az group create --name continuum-rg --location eastus
   
   # Create App Service plan (Free tier)
   az appservice plan create --name continuum-plan --resource-group continuum-rg --sku F1 --is-linux
   
   # Create web app
   az webapp create --resource-group continuum-rg --plan continuum-plan --name continuum-api --runtime "PYTHON:3.11"
   
   # Configure startup command
   az webapp config set --resource-group continuum-rg --name continuum-api --startup-file "gunicorn app:app"
   
   # Deploy
   cd backend
   zip -r deploy.zip . -x "venv/*" -x "__pycache__/*" -x "*.pyc" -x "continuum.db"
   az webapp deployment source config-zip --resource-group continuum-rg --name continuum-api --src deploy.zip
   ```

2. **Configure Environment Variables**
   ```bash
   az webapp config appsettings set --resource-group continuum-rg --name continuum-api --settings \
     FLASK_ENV=production \
     DATABASE_URL="sqlite:///continuum.db"
   ```

3. **Enable CORS**
   ```bash
   az webapp cors add --resource-group continuum-rg --name continuum-api --allowed-origins "*"
   ```

#### Frontend (Azure Static Web Apps)

1. **Build frontend**
   ```bash
   cd frontend
   npm ci
   npm run build
   ```

2. **Deploy to Azure Static Web Apps**
   ```bash
   # Install Static Web Apps CLI
   npm install -g @azure/static-web-apps-cli
   
   # Deploy (will prompt for Azure login)
   swa deploy ./dist --env production
   ```

3. **Update API URL**
   - Edit `frontend/.env.production`:
   ```
   VITE_API_URL=https://continuum-api.azurewebsites.net/api
   ```
   - Rebuild and redeploy

---

### Option 2: GitHub Actions (Automated - Recommended for CI/CD)

1. **Create Azure Resources** (one-time setup)
   ```bash
   # Backend App Service
   az group create --name continuum-rg --location eastus
   az appservice plan create --name continuum-plan --resource-group continuum-rg --sku F1 --is-linux
   az webapp create --resource-group continuum-rg --plan continuum-plan --name continuum-api --runtime "PYTHON:3.11"
   
   # Get publish profile
   az webapp deployment list-publishing-profiles --resource-group continuum-rg --name continuum-api --xml > publish-profile.xml
   
   # Frontend Static Web App
   az staticwebapp create --name continuum-app --resource-group continuum-rg --location eastus2
   az staticwebapp secrets list --name continuum-app --resource-group continuum-rg
   ```

2. **Add GitHub Secrets**
   - Go to GitHub repo → Settings → Secrets and variables → Actions
   - Add:
     - `AZURE_WEBAPP_PUBLISH_PROFILE` - Content of publish-profile.xml
     - `AZURE_STATIC_WEB_APPS_API_TOKEN` - From static web app secrets

3. **Push to main branch** - GitHub Actions will auto-deploy!

---

## Deploy to Vercel (Fastest - 2 minutes)

### Frontend Only (Backend on Azure)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Set environment variables** in Vercel dashboard:
   - `VITE_API_URL` = Your Azure backend URL

---

## Deploy to Render (Free Tier - Good Alternative)

### Backend

1. Create account at https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3.11
5. Add environment variables:
   - `DATABASE_URL` = `sqlite:///continuum.db`

### Frontend

1. New → Static Site
2. Settings:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Publish Directory**: `dist`
3. Add environment variable:
   - `VITE_API_URL` = Your Render backend URL

---

## Production Readiness Checklist

Before deploying:

- [ ] Update `frontend/.env.production` with production API URL
- [ ] Set `FLASK_ENV=production` in backend environment
- [ ] Configure CORS to only allow your frontend domain (not `*`)
- [ ] Add proper error logging (Sentry, Azure Monitor)
- [ ] Set up database backups (if using PostgreSQL)
- [ ] Add health check monitoring
- [ ] Configure custom domain (optional)
- [ ] Set up SSL/HTTPS (auto with Azure/Vercel/Render)

---

## Database Consideration

**Current**: SQLite (file-based)
- ✅ Works for single-instance deployments
- ❌ Won't work with multiple instances or Azure App Service restarts

**Recommended for Production**:
```bash
# Option 1: Azure Database for PostgreSQL (Free tier available)
az postgres flexible-server create --resource-group continuum-rg --name continuum-db --location eastus --admin-user admin --admin-password <password> --sku-name Standard_B1ms --tier Burstable --storage-size 32

# Option 2: Use Render PostgreSQL (Free tier)
# Create database on Render dashboard

# Update backend/app.py:
# DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///continuum.db')
```

---

## Cost Estimate

### Free Tier Options:
- **Azure**: App Service F1 (Free) + Static Web Apps (Free) = $0/month
- **Vercel**: Frontend only (Free) = $0/month
- **Render**: Web Service (Free) + Static Site (Free) = $0/month

### Paid Tier (for scaling):
- **Azure**: B1 App Service ($13/month) + Static Web Apps (Free)
- **Render**: Starter ($7/month) + Free static

---

## Quick Commands Reference

```bash
# Check backend deployment
curl https://continuum-api.azurewebsites.net/api/health

# Check frontend
curl https://continuum-app.azurestaticapps.net

# View logs
az webapp log tail --resource-group continuum-rg --name continuum-api

# Restart app
az webapp restart --resource-group continuum-rg --name continuum-api
```

---

## Next Steps After Deployment

1. ✅ Test the deployed app thoroughly
2. ✅ Set up monitoring and alerts
3. ✅ Implement authentication (Week 4 plan)
4. ✅ Configure custom domain
5. ✅ Add database backups
6. ✅ Set up CI/CD for automatic deployments

---

**Fastest Path**: 
1. Deploy backend to Azure App Service (5 minutes)
2. Deploy frontend to Vercel (2 minutes)
3. Update frontend env with backend URL
4. Done! 🎉

**Best for Learning**: 
- Use Azure for everything (matches your project goals)
- Set up GitHub Actions for CI/CD
- Prepare for authentication and future features

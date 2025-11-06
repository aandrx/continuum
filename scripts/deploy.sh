#!/bin/bash

# Continuum Quick Deploy Script
# Deploys backend to Azure App Service and frontend to Vercel

set -e  # Exit on error

echo "🚀 Continuum Deployment Script"
echo "================================"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Installing..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
fi

# Check if logged into Azure
if ! az account show &> /dev/null; then
    echo "🔐 Please login to Azure..."
    az login
fi

# Variables
RESOURCE_GROUP="continuum-rg"
LOCATION="eastus"
APP_SERVICE_PLAN="continuum-plan"
BACKEND_APP_NAME="continuum-api-$(whoami)"
FRONTEND_DIR="$(pwd)/frontend"
BACKEND_DIR="$(pwd)/backend"

echo "📦 Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Backend App: $BACKEND_APP_NAME"
echo ""

# Create resource group
echo "1️⃣  Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION --output none

# Create App Service plan (Free tier)
echo "2️⃣  Creating App Service plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku F1 \
  --is-linux \
  --output none

# Create web app
echo "3️⃣  Creating web app..."
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $BACKEND_APP_NAME \
  --runtime "PYTHON:3.11" \
  --output none

# Configure startup command
echo "4️⃣  Configuring startup command..."
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --startup-file "gunicorn app:app" \
  --output none

# Set environment variables
echo "5️⃣  Setting environment variables..."
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --settings FLASK_ENV=production DATABASE_URL="sqlite:///continuum.db" \
  --output none

# Enable CORS
echo "6️⃣  Enabling CORS..."
az webapp cors add \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --allowed-origins "*" \
  --output none

# Deploy backend
echo "7️⃣  Deploying backend..."
cd $BACKEND_DIR
zip -r deploy.zip . -x "venv/*" -x "__pycache__/*" -x "*.pyc" -x "continuum.db" -x "*.db" > /dev/null
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP_NAME \
  --src deploy.zip \
  --output none
rm deploy.zip
cd ..

BACKEND_URL="https://${BACKEND_APP_NAME}.azurewebsites.net"

echo ""
echo "✅ Backend deployed!"
echo "   URL: $BACKEND_URL"
echo ""

# Update frontend environment variable
echo "8️⃣  Updating frontend environment..."
echo "VITE_API_URL=${BACKEND_URL}/api" > $FRONTEND_DIR/.env.production

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Deploy frontend to Vercel
echo "9️⃣  Deploying frontend to Vercel..."
cd $FRONTEND_DIR
vercel --prod --yes

echo ""
echo "🎉 Deployment Complete!"
echo "================================"
echo ""
echo "🔗 Your app is now live:"
echo "   Backend:  $BACKEND_URL"
echo "   Frontend: (Check Vercel output above)"
echo ""
echo "📝 Next steps:"
echo "   1. Test the health endpoint: curl $BACKEND_URL/api/health"
echo "   2. Open the frontend URL in your browser"
echo "   3. Create a card to test the integration"
echo ""
echo "💡 To update CORS after frontend deployment:"
echo "   az webapp cors add --resource-group $RESOURCE_GROUP --name $BACKEND_APP_NAME --allowed-origins <your-vercel-url>"
echo ""

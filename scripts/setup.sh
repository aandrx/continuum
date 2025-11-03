#!/bin/bash

# Continuum - Setup Script
# This script sets up the development environment

set -e

echo "Setting up Continuum development environment..."

# Check prerequisites
echo "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi
echo "Node.js $(node --version)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi
echo "Python $(python3 --version)"

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo "Docker $(docker --version)"
else
    echo "Docker not found (optional for local development)"
fi

# Setup Frontend
echo ""
echo "Setting up frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "Frontend dependencies already installed"
fi
cd ..

# Setup Backend
echo ""
echo "Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
fi

source venv/bin/activate
pip install -r requirements.txt
echo "Backend dependencies installed"

# Copy environment files
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Backend .env file created"
fi
cd ..

# Create frontend .env if needed
cd frontend
if [ ! -f ".env.local" ]; then
    echo "VITE_API_URL=http://localhost:5000" > .env.local
    echo "Frontend .env.local file created"
fi
cd ..

echo ""
echo "Setup complete!"
echo ""
echo "To start development:"
echo "  Frontend: cd frontend && npm run dev"
echo "  Backend:  cd backend && source venv/bin/activate && python app.py"
echo ""
echo "Or use Docker Compose: docker-compose up"

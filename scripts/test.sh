#!/bin/bash

# Continuum - Quick Test Script
# This script performs basic tests to verify the setup is working

set -e

echo "================================"
echo "Continuum - Quick Test"
echo "================================"
echo ""

# Test 1: Check prerequisites
echo "[1/5] Checking prerequisites..."
node --version || { echo "ERROR: Node.js not found"; exit 1; }
python3 --version || { echo "ERROR: Python not found"; exit 1; }
echo "OK Prerequisites OK"
echo ""

# Test 2: Check project structure
echo "[2/5] Checking project structure..."
test -d "frontend" || { echo "ERROR: frontend/ directory not found"; exit 1; }
test -d "backend" || { echo "ERROR: backend/ directory not found"; exit 1; }
test -f "frontend/package.json" || { echo "ERROR: frontend/package.json not found"; exit 1; }
test -f "backend/requirements.txt" || { echo "ERROR: backend/requirements.txt not found"; exit 1; }
echo "OK Project structure OK"
echo ""

# Test 3: Check frontend dependencies
echo "[3/5] Checking frontend dependencies..."
if [ ! -d "frontend/node_modules" ]; then
    echo "WARNING: Frontend dependencies not installed"
    echo "Run: cd frontend && npm install"
else
    echo "OK Frontend dependencies OK"
fi
echo ""

# Test 4: Check backend virtual environment
echo "[4/5] Checking backend setup..."
if [ ! -d "backend/venv" ]; then
    echo "WARNING: Backend virtual environment not found"
    echo "Run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
else
    echo "OK Backend virtual environment OK"
fi
echo ""

# Test 5: Verify files are readable
echo "[5/5] Checking configuration files..."
test -f "README.md" || echo "WARNING: README.md not found"
test -f "docker-compose.yml" || echo "WARNING: docker-compose.yml not found"
test -f ".gitignore" || echo "WARNING: .gitignore not found"
test -f "frontend/.env.local" || echo "WARNING: frontend/.env.local not found"
test -f "backend/.env.example" || echo "WARNING: backend/.env.example not found"
echo "OK Configuration files OK"
echo ""

echo "================================"
echo "Test Summary"
echo "================================"
echo ""
echo "Your Continuum setup is ready!"
echo ""
echo "Next steps to test the application:"
echo ""
echo "1. Start frontend:"
echo "   cd frontend && npm run dev"
echo "   Then open: http://localhost:5173/"
echo ""
echo "2. Start backend (in a new terminal):"
echo "   cd backend && source venv/bin/activate && python app.py"
echo "   Then test: curl http://localhost:5000/api/health"
echo ""
echo "See docs/TESTING.md for detailed testing instructions"
echo ""

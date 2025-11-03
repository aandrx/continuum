# Continuum - Quick Start Guide

## Getting Started

### Prerequisites
- Node.js 16+ (you have v20+)
- Python 3.9+
- Git

### One-Command Setup
```bash
./scripts/setup.sh
```

## Development Commands

### Frontend (Vue.js)
```bash
cd frontend
npm run dev          # Start dev server (http://localhost:5173)
npm run build        # Build for production
npm run test:unit    # Run unit tests
npm run lint         # Lint and fix code
npm run format       # Format code with Prettier
npm run type-check   # Check TypeScript types
```

### Backend (Python/Flask)
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python app.py             # Start API server (http://localhost:5000)
pytest                    # Run tests (when added)
black .                   # Format code
flake8 .                  # Lint code
```

### Docker Compose
```bash
docker-compose up        # Start all services
docker-compose down      # Stop all services
docker-compose build     # Rebuild containers
```

## Project Structure

```
continuum/
├── frontend/        # Vue.js 3 + TypeScript
├── backend/         # Python Flask API
├── infrastructure/  # Terraform & Kubernetes
├── docs/           # Documentation
├── scripts/        # Utility scripts
└── tests/          # Integration tests
```

## Useful URLs

- **Frontend Dev**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health
- **Categories**: http://localhost:5000/api/categories

## Key Files

- `IMPLEMENTATION_PLAN.md` - Progress tracker with checkboxes
- `outline.md` - Original project vision and requirements
- `docs/ARCHITECTURE.md` - Technical architecture details
- `.env.example` - Environment variable templates

## Current Phase

**Phase 1: Core Kanban Board** (Weeks 1-2)
- Setup & Foundation complete
- Next: Build UI components

## Documentation

- Architecture: `docs/ARCHITECTURE.md`
- Progress: `IMPLEMENTATION_PLAN.md`
- Vision: `outline.md`

## Git Workflow

```bash
# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: description of feature"

# Push to GitHub
git push origin main
```

## Tips

1. Always activate Python venv before backend work
2. Frontend runs on port 5173, backend on 5000
3. Use `npm run format` before committing frontend code
4. Use `black .` before committing backend code
5. Check IMPLEMENTATION_PLAN.md and mark off completed tasks
6. Add notes about issues/solutions to IMPLEMENTATION_PLAN.md

## Troubleshooting

### Frontend won't start
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Backend issues
```bash
cd backend
deactivate  # if venv is active
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

## Support

Check documentation or review IMPLEMENTATION_PLAN.md for detailed steps and notes.

---

**Project**: Continuum - Personal Productivity Dashboard  
**Started**: November 3, 2025  
**Status**: Active Development

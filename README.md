# Continuum - Personal Productivity Dashboard

A unified kanban board with specialized categories that integrates with your life and showcases your work publicly. Built with Vue.js, Python, Docker, and Kubernetes.

## Vision

Category-switching productivity platform managing:
- **Business & Finance** - Bill payments and financial tasks (Plaid integration)
- **Coding Projects** - Development work and GitHub issues (GitHub integration)
- **Health & Life** - Personal wellness and habits (Manual tracking)
- **Communications** - Email management and follow-ups (Gmail integration)

## Tech Stack

- **Frontend**: Vue.js 3, TypeScript, Pinia, Vue Router, Vite
- **Backend**: Python 3.9+, Flask, CORS
- **Infrastructure**: Docker, Kubernetes, GCP + Azure
- **CI/CD**: GitHub Actions
- **IaC**: Terraform

## Project Structure

```
continuum/
├── frontend/          # Vue.js 3 + TypeScript
├── backend/           # Python Flask API
├── infrastructure/    # Terraform & Kubernetes
├── docs/              # Documentation & guides
├── scripts/           # Setup & utility scripts
└── tests/             # Integration tests
```

## Quick Start

### Prerequisites
- Node.js 16+
- Python 3.9+
- Git

### Setup & Run

```bash
# Clone and setup
git clone https://github.com/aandrx/continuum.git
cd continuum
./scripts/setup.sh

# Start frontend (Terminal 1)
cd frontend
npm run dev
# Opens at http://localhost:5173

# Start backend (Terminal 2)
cd backend
source venv/bin/activate
python app.py
# Runs at http://localhost:5000
```

### Test

```bash
./scripts/test.sh
```

## Documentation

- [Implementation Plan](./docs/IMPLEMENTATION_PLAN.md) - Detailed roadmap and progress
- [Architecture](./docs/ARCHITECTURE.md) - System design and data flow
- [Testing Guide](./docs/TESTING.md) - How to test the application
- [Quick Start](./docs/QUICK_START.md) - Development commands
- [Original Outline](./docs/outline.md) - Project vision and requirements

## Development

```bash
# Frontend commands
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run test:unit    # Run tests
npm run lint         # Lint code

# Backend commands
cd backend
source venv/bin/activate
python app.py        # Start API server
pytest               # Run tests (when available)
black .              # Format code
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/categories` - Get all categories

## Status

**Current Phase**: Setup & Foundation Complete  
**Next**: Core Kanban UI Components  
**Started**: November 3, 2025

## License

MIT License

## Contributing

Personal portfolio project. Feedback welcome!

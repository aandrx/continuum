# Continuum - Project Roadmap

**Version**: 0.2.0  
**Last Updated**: November 6, 2025  
**Current Phase**: Phase 2 (Backend & Containers)

---

## Overview

Continuum is evolving from a local-storage kanban board into a full-stack, cloud-native productivity platform. This roadmap outlines the remaining 4 phases of development.

**Timeline**: 8 weeks (November 7 - January 3, 2026)  
**Progress**: Phase 1 Complete ✅ | Phase 2 In Progress 🔄

---

## Phase 2: Backend API & Authentication (Weeks 3-4)

**Status**: 🔄 In Progress  
**Duration**: 2 weeks (Nov 7 - Nov 20, 2025)  
**Goal**: Replace local storage with real database, add user authentication

### Week 3: Database & Core API ✅ (Partially Complete)
- [x] Set up SQLAlchemy with SQLite database
- [x] Create Card and Category models
- [x] Build 8 REST API endpoints (CRUD for cards)
- [x] Add Pydantic validation schemas
- [x] Connect frontend to backend API
- [x] Add loading states and error handling
- [ ] Write API tests (backend)
- [ ] Write integration tests (frontend + backend)

### Week 4: User Authentication & Data Isolation
**Priority**: HIGH - Required for multi-user functionality

#### Backend Authentication
- [ ] Install Flask-Login and bcrypt
- [ ] Create User model (email, password_hash, created_at)
- [ ] Add JWT token generation
- [ ] Create auth endpoints:
  - `POST /api/auth/register` - User registration
  - `POST /api/auth/login` - Login and receive JWT
  - `POST /api/auth/logout` - Invalidate session
  - `GET /api/auth/me` - Get current user info
- [ ] Add authentication middleware to protect endpoints
- [ ] Update Card model with `user_id` foreign key
- [ ] Filter all card queries by authenticated user

#### Frontend Authentication
- [ ] Create Login.vue and Register.vue components
- [ ] Add auth store (Pinia) for user state
- [ ] Implement login/register workflows
- [ ] Add route guards (redirect unauthenticated users)
- [ ] Store JWT in localStorage
- [ ] Add Authorization header to all API calls
- [ ] Add logout button to app header
- [ ] Handle token expiration gracefully

#### Security
- [ ] Implement password hashing (bcrypt)
- [ ] Add password requirements (8+ chars, complexity)
- [ ] Configure JWT expiration (24 hours)
- [ ] Add rate limiting to login endpoint
- [ ] Update CORS configuration for production

#### Containerization
- [ ] Write production Dockerfile for backend
- [ ] Write production Dockerfile for frontend
- [ ] Update docker-compose.yml with environment variables
- [ ] Test full stack in Docker containers
- [ ] Document Docker deployment process

**Deliverables**:
- ✅ Working REST API with database persistence
- 🔄 User authentication and authorization system
- 🔄 Dockerized application
- 🔄 API documentation (Swagger/OpenAPI)

---

## Phase 3: External Integrations (Weeks 5-6)

**Status**: ⏳ Not Started  
**Duration**: 2 weeks (Nov 21 - Dec 4, 2025)  
**Goal**: Connect to external services for automated task creation

### Week 5: GitHub Integration
- [ ] Set up GitHub OAuth app
- [ ] Create GitHub API service wrapper
- [ ] Add GitHub account linking UI
- [ ] Implement issue syncing:
  - Pull assigned issues as "Coding" category cards
  - Auto-update when issues change
  - Mark cards as done when issues close
- [ ] Add webhook endpoint for real-time updates
- [ ] Show GitHub avatar and link on cards

### Week 6: Financial & Email Integration
- [ ] Set up Plaid developer account
- [ ] Create Plaid Link UI for bank connection
- [ ] Pull transactions for "Business" category
- [ ] Categorize transactions as potential tasks
- [ ] Set up Gmail API OAuth
- [ ] Create email parser for action items
- [ ] Auto-create "Communications" cards from flagged emails
- [ ] Add email reply button on cards

**Deliverables**:
- Automated task creation from GitHub issues
- Financial transaction monitoring with Plaid
- Email-to-task conversion from Gmail
- OAuth integration for all 3rd party services

---

## Phase 4: Public Portfolio & CI/CD (Weeks 7-8)

**Status**: ⏳ Not Started  
**Duration**: 2 weeks (Dec 5 - Dec 18, 2025)  
**Goal**: Deploy to production and create public showcase

### Week 7: CI/CD Pipeline
- [ ] Set up GitHub Actions workflows:
  - Automated testing on PR
  - Linting and type checking
  - Build Docker images
  - Push to container registry
- [ ] Configure environments (dev, staging, prod)
- [ ] Add automated deployment to staging
- [ ] Set up secrets management
- [ ] Create rollback procedures

### Week 8: Public Export & Deployment
- [ ] Create public portfolio page:
  - Show completed projects (opt-in)
  - Display coding activity stats
  - Showcase skills and technologies
- [ ] Add privacy controls (select what's public)
- [ ] Deploy to GCP Cloud Run
- [ ] Set up custom domain
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring and logging

**Deliverables**:
- Automated CI/CD pipeline
- Production deployment on GCP
- Public portfolio page
- Domain and SSL configured

---

## Phase 5: Multi-Cloud & Observability (Weeks 9-10)

**Status**: ⏳ Not Started  
**Duration**: 2 weeks (Dec 19, 2025 - Jan 3, 2026)  
**Goal**: Add redundancy and production-grade monitoring

### Week 9: Multi-Cloud Deployment
- [ ] Set up Azure App Service as backup
- [ ] Configure Terraform for infrastructure-as-code:
  - GCP resources (primary)
  - Azure resources (DR)
- [ ] Implement database replication
- [ ] Set up traffic routing/failover
- [ ] Test disaster recovery procedures
- [ ] Document multi-cloud architecture

### Week 10: Monitoring & Optimization
- [ ] Set up Prometheus for metrics collection
- [ ] Configure Grafana dashboards:
  - API response times
  - Database query performance
  - User activity metrics
  - Error rates and logs
- [ ] Add application performance monitoring (APM)
- [ ] Set up alerting (email/SMS for critical issues)
- [ ] Implement log aggregation
- [ ] Performance optimization based on metrics
- [ ] Load testing and capacity planning

**Deliverables**:
- Multi-cloud deployment (GCP + Azure)
- Infrastructure-as-code with Terraform
- Complete observability stack
- Performance optimization report
- Production operations runbook

---

## Key Milestones

| Phase | Start Date | End Date | Key Deliverable |
|-------|-----------|----------|-----------------|
| Phase 1 ✅ | Nov 3 | Nov 6 | Kanban UI with local storage |
| Phase 2 🔄 | Nov 7 | Nov 20 | Backend API + Authentication |
| Phase 3 ⏳ | Nov 21 | Dec 4 | External integrations (GitHub, Plaid, Gmail) |
| Phase 4 ⏳ | Dec 5 | Dec 18 | Production deployment + CI/CD |
| Phase 5 ⏳ | Dec 19 | Jan 3 | Multi-cloud + monitoring |

---

## Success Criteria

### Phase 2 Success
- ✅ Users can register and login
- ✅ Each user sees only their own cards
- ✅ Data persists in database (not localStorage)
- ✅ API has >90% test coverage
- ✅ App runs in Docker containers

### Phase 3 Success
- ✅ GitHub issues automatically create cards
- ✅ Plaid shows recent transactions as tasks
- ✅ Flagged emails become communication cards
- ✅ All OAuth flows work smoothly

### Phase 4 Success
- ✅ App deployed to production (GCP)
- ✅ Accessible via custom domain with HTTPS
- ✅ CI/CD deploys on every merge to main
- ✅ Public portfolio shows completed work

### Phase 5 Success
- ✅ App runs on both GCP and Azure
- ✅ Monitoring dashboards show key metrics
- ✅ Alerts trigger on critical issues
- ✅ Infrastructure defined in Terraform
- ✅ Can handle 1000+ concurrent users

---

## Technical Debt & Future Enhancements

### Known Issues (To Address)
- [ ] Add password reset flow (forgot password)
- [ ] Implement refresh tokens (currently only access tokens)
- [ ] Add email verification on signup
- [ ] Rate limiting on all endpoints (not just login)
- [ ] Add WebSocket support for real-time updates
- [ ] Migrate from SQLite to PostgreSQL (for production)

### Future Features (Post-v1.0)
- [ ] Mobile app (React Native)
- [ ] Desktop app (Electron)
- [ ] Shared boards (collaboration)
- [ ] Card comments and attachments
- [ ] Recurring tasks
- [ ] Calendar view
- [ ] Analytics dashboard
- [ ] AI-powered task suggestions
- [ ] Dark mode theme
- [ ] Customizable categories

---

## Resources & References

### Documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
- [PHASE2_PROGRESS.md](./PHASE2_PROGRESS.md) - Current work tracking
- [AUTHENTICATION.md](./AUTHENTICATION.md) - Auth implementation guide
- [USER_GUIDE.md](./USER_GUIDE.md) - Feature documentation

### External APIs
- [GitHub REST API](https://docs.github.com/en/rest)
- [Plaid API](https://plaid.com/docs/)
- [Gmail API](https://developers.google.com/gmail/api)

### Cloud Platforms
- [GCP Cloud Run](https://cloud.google.com/run)
- [Azure App Service](https://azure.microsoft.com/en-us/services/app-service/)

---

## Notes

- **Phase 2 is critical** - Authentication must be complete before external integrations
- **Security first** - All auth flows must be reviewed before Phase 3
- **Docker readiness** - Containerization enables Phase 4 deployment
- **Monitor early** - Start logging and metrics in Phase 2, not Phase 5
- **Test coverage** - Aim for 80%+ coverage before production deployment

**Last Review**: November 6, 2025  
**Next Review**: November 13, 2025 (End of Week 3)

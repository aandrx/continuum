# Authentication Implementation Guide

**Version**: 0.3.0  
**Phase**: 2 (Week 4)  
**Priority**: HIGH  
**Estimated Time**: 12-16 hours

---

## Overview

This document outlines the complete implementation of user authentication for Continuum, transforming it from a single-user local storage app into a multi-user, database-backed platform with secure login.

**Goal**: Enable multiple users to have private, isolated kanban boards accessible from any device.

---

## Architecture

### Authentication Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ 1. POST /api/auth/register
       │    {email, password}
       ▼
┌─────────────────────────────┐
│   Flask Backend             │
│                             │
│  2. Hash password (bcrypt)  │
│  3. Create user in DB       │
│  4. Generate JWT token      │
└──────┬──────────────────────┘
       │ 5. Return {token, user}
       ▼
┌─────────────┐
│   Browser   │
│             │
│  6. Store token in          │
│     localStorage            │
│  7. Add to all requests:    │
│     Authorization: Bearer   │
│     <token>                 │
└─────────────┘

Subsequent requests:
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ GET /api/cards
       │ Authorization: Bearer <token>
       ▼
┌─────────────────────────────┐
│   Flask Backend             │
│                             │
│  1. Verify JWT signature    │
│  2. Extract user_id         │
│  3. Query cards WHERE       │
│     user_id = <user_id>     │
└──────┬──────────────────────┘
       │ Return user's cards only
       ▼
┌─────────────┐
│   Browser   │
└─────────────┘
```

---

## Backend Implementation

### Step 1: Install Dependencies

Add to `backend/requirements.txt`:
```
Flask-JWT-Extended==4.6.0
bcrypt==4.2.0
email-validator==2.1.1
```

Install:
```bash
cd backend
source venv/Scripts/activate
pip install -r requirements.txt
```

### Step 2: Create User Model

Create `backend/models/user.py`:
```python
"""
User model for authentication
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt
from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to cards
    cards = relationship("Card", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )

    def to_dict(self):
        """Convert to dictionary (exclude password)"""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
```

### Step 3: Update Card Model

Modify `backend/models/card.py` to add `user_id`:
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category_id = Column(String(50), ForeignKey('categories.id'), nullable=False)
    column_id = Column(String(50), nullable=False)
    priority = Column(String(20), default='medium')
    tags = Column(Text)  # JSON string
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = relationship("Category")
    user = relationship("User", back_populates="cards")
```

### Step 4: Create Auth Service

Create `backend/services/auth_service.py`:
```python
"""
Authentication service
"""
from sqlalchemy.orm import Session
from models.user import User
from typing import Optional
import re


class AuthService:
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        Returns (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        return True, ""

    @staticmethod
    def register_user(db: Session, email: str, password: str) -> tuple[Optional[User], Optional[str]]:
        """
        Register a new user
        Returns (user, error_message)
        """
        # Validate email
        if not AuthService.validate_email(email):
            return None, "Invalid email format"

        # Check if user exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return None, "Email already registered"

        # Validate password
        is_valid, error = AuthService.validate_password(password)
        if not is_valid:
            return None, error

        # Create user
        user = User(email=email)
        user.set_password(password)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user, None

    @staticmethod
    def login_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user
        Returns user if successful, None otherwise
        """
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.check_password(password):
            return None
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
```

### Step 5: Configure JWT

Update `backend/app.py`:
```python
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

# CORS Configuration
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

# Register blueprints
from api.routes import api
from api.auth_routes import auth_bp
app.register_blueprint(api)
app.register_blueprint(auth_bp)
```

Update `.env`:
```bash
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
```

### Step 6: Create Auth Routes

Create `backend/api/auth_routes.py`:
```python
"""
Authentication routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import get_db
from services.auth_service import AuthService
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @validator('password')
    def password_strength(cls, v):
        is_valid, error = AuthService.validate_password(v)
        if not is_valid:
            raise ValueError(error)
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = RegisterRequest(**request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    db = next(get_db())
    try:
        user, error = AuthService.register_user(db, data.email, data.password)
        if error:
            return jsonify({'error': error}), 400

        # Generate JWT token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'user': user.to_dict(),
            'token': access_token
        }), 201

    finally:
        db.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = LoginRequest(**request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    db = next(get_db())
    try:
        user = AuthService.login_user(db, data.email, data.password)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate JWT token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'user': user.to_dict(),
            'token': access_token
        }), 200

    finally:
        db.close()


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    
    db = next(get_db())
    try:
        user = AuthService.get_user_by_id(db, user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify(user.to_dict()), 200

    finally:
        db.close()


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client-side token removal)"""
    # JWT tokens are stateless, so logout is handled client-side
    # This endpoint exists for consistency and future token blacklisting
    return jsonify({'message': 'Logged out successfully'}), 200
```

### Step 7: Protect Card Routes

Update `backend/api/routes.py` to require authentication:
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@api.route('/cards', methods=['GET'])
@jwt_required()
def get_cards():
    """Get all cards for authenticated user"""
    user_id = get_jwt_identity()
    category_id = request.args.get('category')
    
    db = next(get_db())
    try:
        cards = CardService.get_cards(db, user_id=user_id, category_id=category_id)
        return jsonify(cards), 200
    finally:
        db.close()

# Update all other card endpoints similarly...
```

Update `backend/services/db_service.py`:
```python
class CardService:
    @staticmethod
    def get_cards(db: Session, user_id: int, category_id: Optional[str] = None) -> list[dict]:
        """Get cards for a specific user"""
        query = db.query(Card).filter(Card.user_id == user_id)
        if category_id:
            query = query.filter(Card.category_id == category_id)
        cards = query.all()
        return [card.to_dict() for card in cards]

    @staticmethod
    def create_card(db: Session, user_id: int, card_data: dict) -> dict:
        """Create a new card for user"""
        card = Card(**card_data, user_id=user_id)
        db.add(card)
        db.commit()
        db.refresh(card)
        return card.to_dict()
    
    # Update all other methods to filter by user_id...
```

---

## Frontend Implementation

### Step 1: Create Auth Service

Create `frontend/src/services/auth.ts`:
```typescript
import type { User } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

interface AuthResponse {
  user: User
  token: string
}

interface ErrorResponse {
  error: string
}

class AuthService {
  private token: string | null = null

  constructor() {
    // Load token from localStorage on init
    this.token = localStorage.getItem('auth_token')
  }

  getToken(): string | null {
    return this.token
  }

  setToken(token: string) {
    this.token = token
    localStorage.setItem('auth_token', token)
  }

  clearToken() {
    this.token = null
    localStorage.removeItem('auth_token')
  }

  async register(email: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (!response.ok) {
      const error: ErrorResponse = await response.json()
      throw new Error(error.error || 'Registration failed')
    }

    const data: AuthResponse = await response.json()
    this.setToken(data.token)
    return data
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (!response.ok) {
      const error: ErrorResponse = await response.json()
      throw new Error(error.error || 'Login failed')
    }

    const data: AuthResponse = await response.json()
    this.setToken(data.token)
    return data
  }

  async logout(): Promise<void> {
    if (this.token) {
      try {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: { 
            'Authorization': `Bearer ${this.token}`
          }
        })
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    this.clearToken()
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: { 
        'Authorization': `Bearer ${this.token}`
      }
    })

    if (!response.ok) {
      throw new Error('Failed to get user')
    }

    return response.json()
  }

  isAuthenticated(): boolean {
    return this.token !== null
  }
}

export default new AuthService()
```

### Step 2: Update Types

Add to `frontend/src/types/index.ts`:
```typescript
export interface User {
  id: number
  email: string
  created_at: string
}
```

### Step 3: Create Auth Store

Create `frontend/src/stores/auth.ts`:
```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import authService from '@/services/auth'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function register(email: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await authService.register(email, password)
      user.value = response.user
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await authService.login(email, password)
      user.value = response.user
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      await authService.logout()
      user.value = null
    } finally {
      loading.value = false
    }
  }

  async function checkAuth() {
    if (authService.isAuthenticated()) {
      try {
        user.value = await authService.getCurrentUser()
      } catch (error) {
        authService.clearToken()
      }
    }
  }

  function isAuthenticated(): boolean {
    return user.value !== null
  }

  return {
    user,
    loading,
    error,
    register,
    login,
    logout,
    checkAuth,
    isAuthenticated
  }
})
```

### Step 4: Update API Client

Modify `frontend/src/services/api.ts` to include auth token:
```typescript
import authService from './auth'

class ApiClient {
  private async fetch(url: string, options: RequestInit = {}) {
    const token = authService.getToken()
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${this.baseUrl}${url}`, {
      ...options,
      headers
    })

    if (response.status === 401) {
      // Token expired or invalid
      authService.clearToken()
      window.location.href = '/login'
      throw new Error('Unauthorized')
    }

    if (!response.ok) {
      const error: ApiError = await response.json()
      throw new Error(error.message || 'API request failed')
    }

    return response
  }

  async getCards(categoryId?: CategoryId): Promise<Card[]> {
    const url = categoryId ? `/cards?category=${categoryId}` : '/cards'
    const response = await this.fetch(url)
    return response.json()
  }

  // Update all methods to use this.fetch() instead of direct fetch()
}
```

### Step 5: Create Login Component

Create `frontend/src/views/LoginView.vue`:
```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const isRegisterMode = ref(false)
const errorMessage = ref('')

async function handleSubmit() {
  errorMessage.value = ''
  
  try {
    if (isRegisterMode.value) {
      await authStore.register(email.value, password.value)
    } else {
      await authStore.login(email.value, password.value)
    }
    router.push('/')
  } catch (error: any) {
    errorMessage.value = error.message
  }
}

function toggleMode() {
  isRegisterMode.value = !isRegisterMode.value
  errorMessage.value = ''
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>{{ isRegisterMode ? 'Create Account' : 'Welcome Back' }}</h1>
      <p class="subtitle">{{ isRegisterMode ? 'Sign up for Continuum' : 'Sign in to Continuum' }}</p>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="your@email.com"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            :placeholder="isRegisterMode ? 'At least 8 characters' : 'Your password'"
          />
          <small v-if="isRegisterMode">Must contain uppercase, lowercase, and number</small>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="submit-btn" :disabled="authStore.loading">
          {{ authStore.loading ? 'Loading...' : (isRegisterMode ? 'Sign Up' : 'Sign In') }}
        </button>
      </form>

      <div class="toggle-mode">
        <span>{{ isRegisterMode ? 'Already have an account?' : "Don't have an account?" }}</span>
        <button @click="toggleMode" type="button">
          {{ isRegisterMode ? 'Sign In' : 'Sign Up' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #364fc7 0%, #2b3e9e 100%);
}

.auth-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 400px;
}

h1 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  color: #212529;
}

.subtitle {
  color: #6c757d;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #495057;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #364fc7;
}

small {
  display: block;
  margin-top: 0.25rem;
  color: #6c757d;
  font-size: 0.85rem;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.submit-btn {
  width: 100%;
  padding: 0.875rem;
  background-color: #364fc7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #2b3e9e;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toggle-mode {
  margin-top: 1.5rem;
  text-align: center;
  color: #6c757d;
}

.toggle-mode button {
  background: none;
  border: none;
  color: #364fc7;
  font-weight: 600;
  cursor: pointer;
  margin-left: 0.5rem;
}

.toggle-mode button:hover {
  text-decoration: underline;
}
</style>
```

### Step 6: Add Route Guards

Update `frontend/src/router/index.ts`:
```typescript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Check authentication status
  if (!authStore.user) {
    await authStore.checkAuth()
  }

  const requiresAuth = to.meta.requiresAuth
  const isAuthenticated = authStore.isAuthenticated()

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login if not authenticated
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    // Redirect to home if already authenticated
    next('/')
  } else {
    next()
  }
})

export default router
```

### Step 7: Add Logout Button

Update `frontend/src/App.vue`:
```vue
<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">Continuum</h1>
        <p class="app-subtitle">Personal Productivity Dashboard</p>
      </div>
      <button v-if="authStore.isAuthenticated()" @click="handleLogout" class="logout-btn">
        Logout
      </button>
    </header>

    <CategorySwitcher v-if="authStore.isAuthenticated()" />

    <main class="app-main">
      <router-view />
    </main>

    <AppFooter />
  </div>
</template>
```

---

## Testing Checklist

### Backend Tests
- [ ] Test user registration with valid data
- [ ] Test registration with duplicate email (should fail)
- [ ] Test registration with weak password (should fail)
- [ ] Test login with correct credentials
- [ ] Test login with wrong password (should fail)
- [ ] Test JWT token generation
- [ ] Test protected endpoints without token (should return 401)
- [ ] Test protected endpoints with valid token
- [ ] Test protected endpoints with expired token
- [ ] Test data isolation (users can't see each other's cards)

### Frontend Tests
- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test logout flow
- [ ] Test token persistence (refresh page, still logged in)
- [ ] Test route guards (redirect to login when not authenticated)
- [ ] Test automatic logout on token expiration
- [ ] Test error handling (wrong password, network errors)

---

## Security Considerations

### Implemented
- ✅ Password hashing with bcrypt (with salt)
- ✅ Email validation
- ✅ Password strength requirements
- ✅ JWT tokens for stateless auth
- ✅ Token expiration (24 hours)
- ✅ Protected API endpoints
- ✅ User data isolation in database queries

### TODO (Phase 3+)
- [ ] Rate limiting on login/register endpoints
- [ ] Account lockout after failed attempts
- [ ] Email verification on signup
- [ ] Password reset flow (forgot password)
- [ ] Refresh tokens (for longer sessions)
- [ ] HTTPS enforcement in production
- [ ] CSRF protection
- [ ] Token blacklisting (for logout)
- [ ] Session management (track active sessions)

---

## Migration Guide

### Database Migration

Run Alembic migration to add User table and update Card table:
```bash
cd backend
source venv/Scripts/activate
alembic revision -m "Add authentication"
alembic upgrade head
```

Or manually:
```sql
-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Add user_id to cards
ALTER TABLE cards ADD COLUMN user_id INTEGER;
ALTER TABLE cards ADD FOREIGN KEY(user_id) REFERENCES users(id);
```

### Data Migration (Existing Cards)

If you have existing cards without a user, create a default user and assign them:
```python
# One-time migration script
from models import get_db, User, Card

db = next(get_db())

# Create default user
default_user = User(email="admin@continuum.local")
default_user.set_password("ChangeMe123!")
db.add(default_user)
db.commit()

# Assign existing cards to default user
cards = db.query(Card).filter(Card.user_id == None).all()
for card in cards:
    card.user_id = default_user.id
db.commit()

print(f"Migrated {len(cards)} cards to default user")
```

---

## Troubleshooting

### Common Issues

**Issue**: JWT token not being sent with requests  
**Solution**: Check that auth service is setting token in localStorage and API client is reading it

**Issue**: CORS errors on login  
**Solution**: Ensure CORS is configured to allow credentials:
```python
CORS(app, origins=cors_origins, supports_credentials=True)
```

**Issue**: Password validation too strict  
**Solution**: Adjust requirements in `AuthService.validate_password()`

**Issue**: Token expires too quickly  
**Solution**: Increase `JWT_ACCESS_TOKEN_EXPIRES` in app config

---

## Next Steps

After authentication is complete:
1. Test thoroughly with multiple users
2. Add user settings page (change password, delete account)
3. Implement "remember me" with refresh tokens
4. Add email verification flow
5. Move to Phase 3: External integrations

---

**Last Updated**: November 6, 2025  
**Status**: Implementation Ready  
**Estimated Completion**: November 20, 2025

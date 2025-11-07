"""
Continuum Backend API
Main application entry point with database integration
"""
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import database and routes
from models import init_db, get_db
from services.db_service import CategoryService
from api.routes import api

app = Flask(__name__)

# Configure CORS - allow production domains
cors_origins_env = os.getenv('CORS_ORIGINS', 'http://localhost:5173')
if cors_origins_env:
    # Support both comma-separated list and regex patterns
    cors_origins = cors_origins_env.split(',')
else:
    cors_origins = ['http://localhost:5173']

# Use regex pattern to support Vercel/Azure wildcards
import re
def check_origin(origin, allowed_origins):
    """Check if origin matches allowed patterns including wildcards"""
    for allowed in allowed_origins:
        # Convert wildcard pattern to regex
        if '*' in allowed:
            pattern = allowed.replace('.', r'\.').replace('*', r'[a-zA-Z0-9-]+')
            if re.match(f'^{pattern}$', origin):
                return True
        elif origin == allowed:
            return True
    return False

# Configure CORS with origin checking function
CORS(app, 
     origins=lambda origin: check_origin(origin, cors_origins + ['https://*.vercel.app', 'https://*.azurestaticapps.net']),
     supports_credentials=True, 
     resources={r"/api/*": {"origins": "*"}})

# Register API blueprint
app.register_blueprint(api)

# Initialize database
with app.app_context():
    init_db()
    # Seed categories
    db = next(get_db())
    CategoryService.seed_categories(db)
    db.close()
    print("✓ Database initialized and categories seeded")

@app.route('/')
def root():
    """Root endpoint with API information."""
    return jsonify({
        'message': 'Continuum API v1.0',
        'version': '0.2.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'categories': '/api/categories',
            'cards': '/api/cards',
            'card_detail': '/api/cards/<id>',
            'move_card': '/api/cards/<id>/move'
        }
    })

if __name__ == '__main__':
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('PORT', os.getenv('API_PORT', 5000)))  # Azure uses PORT env var
    debug = os.getenv('FLASK_ENV', 'development') != 'production'
    
    print(f"Continuum API starting on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)


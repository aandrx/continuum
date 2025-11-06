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

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

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
        'message': 'Continuum API',
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
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"Continuum API starting on {host}:{port}")
    app.run(host=host, port=port, debug=debug)


"""
Continuum Backend API
Main application entry point
"""
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
CORS(app, origins=cors_origins)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'continuum-api',
        'version': '0.1.0'
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    categories = [
        {
            'id': 'business-finance',
            'name': 'Business & Finance',
            'icon': 'briefcase',
            'description': 'Bill payments and financial tasks'
        },
        {
            'id': 'coding-projects',
            'name': 'Coding Projects',
            'icon': 'code',
            'description': 'Development work and GitHub issues'
        },
        {
            'id': 'health-life',
            'name': 'Health & Life',
            'icon': 'heart',
            'description': 'Personal wellness and habits'
        },
        {
            'id': 'communications',
            'name': 'Communications',
            'icon': 'mail',
            'description': 'Email management and follow-ups'
        }
    ]
    return jsonify(categories)

if __name__ == '__main__':
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"Continuum API starting on {host}:{port}")
    app.run(host=host, port=port, debug=debug)

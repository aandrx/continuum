"""API routes for Continuum."""

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from models import get_db
from services.db_service import CardService, CategoryService
from utils.validators import CardCreate, CardUpdate, CardMove

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Continuum API is running'
    })


@api.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    db = next(get_db())
    try:
        categories = CategoryService.get_categories(db)
        return jsonify([cat.to_dict() for cat in categories])
    finally:
        db.close()


@api.route('/cards', methods=['GET'])
def get_cards():
    """Get all cards, optionally filtered by category."""
    category_id = request.args.get('categoryId')
    
    db = next(get_db())
    try:
        cards = CardService.get_cards(db, category_id)
        return jsonify([card.to_dict() for card in cards])
    finally:
        db.close()


@api.route('/cards', methods=['POST'])
def create_card():
    """Create a new card."""
    try:
        # Validate request data
        card_data = CardCreate(**request.json)
        
        db = next(get_db())
        try:
            # Create card in database
            card = CardService.create_card(db, card_data.model_dump(by_alias=False))
            return jsonify(card.to_dict()), 201
        finally:
            db.close()
            
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'details': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Failed to create card',
            'message': str(e)
        }), 500


@api.route('/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    """Get a single card by ID."""
    db = next(get_db())
    try:
        card = CardService.get_card(db, card_id)
        if not card:
            return jsonify({'error': 'Card not found'}), 404
        return jsonify(card.to_dict())
    finally:
        db.close()


@api.route('/cards/<card_id>', methods=['PUT'])
def update_card(card_id):
    """Update a card."""
    try:
        # Validate request data
        update_data = CardUpdate(**request.json)
        
        db = next(get_db())
        try:
            # Update card in database
            card = CardService.update_card(
                db, 
                card_id, 
                update_data.model_dump(by_alias=False, exclude_none=True)
            )
            
            if not card:
                return jsonify({'error': 'Card not found'}), 404
            
            return jsonify(card.to_dict())
        finally:
            db.close()
            
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'details': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Failed to update card',
            'message': str(e)
        }), 500


@api.route('/cards/<card_id>/move', methods=['PATCH'])
def move_card(card_id):
    """Move a card to a different column."""
    try:
        # Validate request data
        move_data = CardMove(**request.json)
        
        db = next(get_db())
        try:
            # Move card
            card = CardService.move_card(db, card_id, move_data.column_id)
            
            if not card:
                return jsonify({'error': 'Card not found'}), 404
            
            return jsonify(card.to_dict())
        finally:
            db.close()
            
    except ValidationError as e:
        return jsonify({
            'error': 'Validation error',
            'details': e.errors()
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Failed to move card',
            'message': str(e)
        }), 500


@api.route('/cards/<card_id>', methods=['DELETE'])
def delete_card(card_id):
    """Delete a card."""
    db = next(get_db())
    try:
        success = CardService.delete_card(db, card_id)
        
        if not success:
            return jsonify({'error': 'Card not found'}), 404
        
        return jsonify({'message': 'Card deleted successfully'}), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete card',
            'message': str(e)
        }), 500
    finally:
        db.close()


@api.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@api.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

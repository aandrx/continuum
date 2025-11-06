"""Database service for CRUD operations."""

from sqlalchemy.orm import Session
from models.card import Card
from models.category import Category
from typing import List, Optional

class CardService:
    """Service for card CRUD operations."""
    
    @staticmethod
    def create_card(db: Session, card_data: dict) -> Card:
        """Create a new card."""
        card = Card(
            id=card_data['id'],
            title=card_data['title'],
            description=card_data.get('description'),
            category_id=card_data['category_id'],
            column_id=card_data['column_id'],
            priority=card_data.get('priority'),
            tags=card_data.get('tags', [])
        )
        db.add(card)
        db.commit()
        db.refresh(card)
        return card
    
    @staticmethod
    def get_card(db: Session, card_id: str) -> Optional[Card]:
        """Get a card by ID."""
        return db.query(Card).filter(Card.id == card_id).first()
    
    @staticmethod
    def get_cards(db: Session, category_id: Optional[str] = None) -> List[Card]:
        """Get all cards, optionally filtered by category."""
        query = db.query(Card)
        if category_id:
            query = query.filter(Card.category_id == category_id)
        return query.order_by(Card.created_at.desc()).all()
    
    @staticmethod
    def update_card(db: Session, card_id: str, update_data: dict) -> Optional[Card]:
        """Update a card."""
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            return None
        
        for key, value in update_data.items():
            if value is not None:  # Only update if value is provided
                setattr(card, key, value)
        
        db.commit()
        db.refresh(card)
        return card
    
    @staticmethod
    def move_card(db: Session, card_id: str, column_id: str) -> Optional[Card]:
        """Move a card to a different column."""
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            return None
        
        card.column_id = column_id
        db.commit()
        db.refresh(card)
        return card
    
    @staticmethod
    def delete_card(db: Session, card_id: str) -> bool:
        """Delete a card."""
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            return False
        
        db.delete(card)
        db.commit()
        return True


class CategoryService:
    """Service for category operations."""
    
    @staticmethod
    def get_categories(db: Session) -> List[Category]:
        """Get all categories."""
        return db.query(Category).all()
    
    @staticmethod
    def seed_categories(db: Session):
        """Seed initial categories if they don't exist."""
        categories = [
            {
                'id': 'business',
                'name': 'Business & Finance',
                'description': 'Financial planning, investments, and business tasks',
                'icon': 'briefcase'
            },
            {
                'id': 'coding',
                'name': 'Coding Projects',
                'description': 'Development projects, issues, and technical tasks',
                'icon': 'code'
            },
            {
                'id': 'health',
                'name': 'Health & Life',
                'description': 'Fitness, wellness, and personal development',
                'icon': 'heart'
            },
            {
                'id': 'communications',
                'name': 'Communications',
                'description': 'Emails, messages, and correspondence',
                'icon': 'mail'
            }
        ]
        
        for cat_data in categories:
            existing = db.query(Category).filter(Category.id == cat_data['id']).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
        
        db.commit()

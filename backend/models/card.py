"""Card database model."""

from sqlalchemy import Column, String, Text, DateTime, JSON
from datetime import datetime
from models import Base

class Card(Base):
    """Card model representing a kanban card."""
    
    __tablename__ = "cards"
    
    id = Column(String, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(String(50), nullable=False)
    column_id = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'categoryId': self.category_id,
            'columnId': self.column_id,
            'priority': self.priority,
            'tags': self.tags or [],
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<Card(id='{self.id}', title='{self.title}', category='{self.category_id}')>"

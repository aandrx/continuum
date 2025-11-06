"""Category database model."""

from sqlalchemy import Column, String, Text
from models import Base

class Category(Base):
    """Category model representing a kanban category."""
    
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
        }
    
    def __repr__(self):
        return f"<Category(id='{self.id}', name='{self.name}')>"

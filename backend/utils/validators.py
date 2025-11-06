"""Input validation utilities using Pydantic."""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class CardCreate(BaseModel):
    """Schema for creating a card."""
    id: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category_id: str = Field(..., alias='categoryId')
    column_id: str = Field(..., alias='columnId')
    priority: Optional[str] = None
    tags: Optional[List[str]] = []
    
    @validator('priority')
    def validate_priority(cls, v):
        if v and v not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be low, medium, or high')
        return v
    
    @validator('column_id')
    def validate_column(cls, v):
        if v not in ['todo', 'inProgress', 'done']:
            raise ValueError('Column must be todo, inProgress, or done')
        return v
    
    @validator('category_id')
    def validate_category(cls, v):
        if v not in ['business', 'coding', 'health', 'communications']:
            raise ValueError('Invalid category ID')
        return v
    
    class Config:
        populate_by_name = True


class CardUpdate(BaseModel):
    """Schema for updating a card."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category_id: Optional[str] = Field(None, alias='categoryId')
    column_id: Optional[str] = Field(None, alias='columnId')
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    
    @validator('priority')
    def validate_priority(cls, v):
        if v and v not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be low, medium, or high')
        return v
    
    @validator('column_id')
    def validate_column(cls, v):
        if v and v not in ['todo', 'inProgress', 'done']:
            raise ValueError('Column must be todo, inProgress, or done')
        return v
    
    @validator('category_id')
    def validate_category(cls, v):
        if v and v not in ['business', 'coding', 'health', 'communications']:
            raise ValueError('Invalid category ID')
        return v
    
    class Config:
        populate_by_name = True


class CardMove(BaseModel):
    """Schema for moving a card."""
    column_id: str = Field(..., alias='columnId')
    
    @validator('column_id')
    def validate_column(cls, v):
        if v not in ['todo', 'inProgress', 'done']:
            raise ValueError('Column must be todo, inProgress, or done')
        return v
    
    class Config:
        populate_by_name = True


class CardResponse(BaseModel):
    """Schema for card response."""
    id: str
    title: str
    description: Optional[str]
    category_id: str = Field(..., alias='categoryId')
    column_id: str = Field(..., alias='columnId')
    priority: Optional[str]
    tags: List[str]
    created_at: str = Field(..., alias='createdAt')
    updated_at: str = Field(..., alias='updatedAt')
    
    class Config:
        populate_by_name = True

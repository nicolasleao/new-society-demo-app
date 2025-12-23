from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class MealCreate(BaseModel):
    username: str
    title: str
    carbs: float
    proteins: float
    fats: float
    total_calories: float
    
    @validator('carbs', 'proteins', 'fats', 'total_calories')
    def validate_positive_numbers(cls, v):
        if v < 0:
            raise ValueError('Values must be non-negative')
        return v
    
    @validator('username', 'title')
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

class MealResponse(BaseModel):
    id: int
    username: str
    title: str
    carbs: float
    proteins: float
    fats: float
    total_calories: float
    created_at: datetime
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_carbs: float
    total_proteins: float
    total_fats: float
    total_calories: float
    meal_count: int
    
class TodayStatsResponse(StatsResponse):
    date: str

class AIMealRequest(BaseModel):
    description: str
    username: str
    
    @validator('description', 'username')
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

class AIMealResponse(BaseModel):
    title: str
    carbs: float
    proteins: float
    fats: float
    total_calories: float
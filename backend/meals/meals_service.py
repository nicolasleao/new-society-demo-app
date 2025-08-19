from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from models import Meal
from schemas import MealCreate, MealResponse
from .meals_repository import MealsRepository

class MealsService:
    def __init__(self, db: Session):
        self.repository = MealsRepository(db)
    
    def create_meal(self, meal_data: MealCreate) -> Meal:
        return self.repository.create_meal(meal_data)
    
    def get_meals_by_username(
        self, 
        username: str, 
        date_filter: Optional[str] = None
    ) -> List[Meal]:
        if not username or not username.strip():
            raise HTTPException(status_code=400, detail="Username cannot be empty")
        
        try:
            return self.repository.get_meals_by_username(username, date_filter)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    def delete_meal(self, meal_id: int) -> dict:
        meal = self.repository.get_meal_by_id(meal_id)
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")
        
        self.repository.soft_delete_meal(meal)
        return {"message": "Meal deleted successfully"}
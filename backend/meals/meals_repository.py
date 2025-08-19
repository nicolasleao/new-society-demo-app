from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List, Optional
from models import Meal
from schemas import MealCreate

class MealsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_meal(self, meal_data: MealCreate) -> Meal:
        meal = Meal(**meal_data.dict())
        self.db.add(meal)
        self.db.commit()
        self.db.refresh(meal)
        return meal
    
    def get_meals_by_username(
        self, 
        username: str, 
        date_filter: Optional[str] = None
    ) -> List[Meal]:
        query = self.db.query(Meal).filter(
            Meal.username == username.strip(),
            Meal.deleted_at.is_(None)
        )
        
        if date_filter == "today":
            today = date.today()
            query = query.filter(func.date(Meal.created_at) == today)
        elif date_filter:
            filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(func.date(Meal.created_at) == filter_date)
        
        return query.order_by(Meal.created_at.desc()).all()
    
    def get_meal_by_id(self, meal_id: int) -> Optional[Meal]:
        return self.db.query(Meal).filter(Meal.id == meal_id).first()
    
    def soft_delete_meal(self, meal: Meal) -> None:
        meal.deleted_at = func.now()
        self.db.commit()
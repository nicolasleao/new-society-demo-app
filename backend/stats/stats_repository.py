from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List
from models import Meal

class StatsRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_meals_by_username(self, username: str) -> List[Meal]:
        return self.db.query(Meal).filter(
            Meal.username == username.strip(),
            Meal.deleted_at.is_(None)
        ).all()
    
    def get_today_meals_by_username(self, username: str) -> List[Meal]:
        today = date.today()
        return self.db.query(Meal).filter(
            Meal.username == username.strip(),
            Meal.deleted_at.is_(None),
            func.date(Meal.created_at) == today
        ).all()
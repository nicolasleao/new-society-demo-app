from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date
from schemas import StatsResponse, TodayStatsResponse
from .stats_repository import StatsRepository

class StatsService:
    def __init__(self, db: Session):
        self.repository = StatsRepository(db)
    
    def get_user_stats(self, username: str) -> StatsResponse:
        if not username or not username.strip():
            raise HTTPException(status_code=400, detail="Username cannot be empty")
        
        meals = self.repository.get_all_meals_by_username(username)
        
        if not meals:
            return StatsResponse(
                total_carbs=0,
                total_proteins=0,
                total_fats=0,
                total_calories=0,
                meal_count=0
            )
        
        total_carbs = sum(meal.carbs for meal in meals)
        total_proteins = sum(meal.proteins for meal in meals)
        total_fats = sum(meal.fats for meal in meals)
        total_calories = sum(meal.total_calories for meal in meals)
        
        return StatsResponse(
            total_carbs=total_carbs,
            total_proteins=total_proteins,
            total_fats=total_fats,
            total_calories=total_calories,
            meal_count=len(meals)
        )
    
    def get_today_stats(self, username: str) -> TodayStatsResponse:
        if not username or not username.strip():
            raise HTTPException(status_code=400, detail="Username cannot be empty")
        
        meals = self.repository.get_today_meals_by_username(username)
        today = date.today()
        
        if not meals:
            return TodayStatsResponse(
                total_carbs=0,
                total_proteins=0,
                total_fats=0,
                total_calories=0,
                meal_count=0,
                date=str(today)
            )
        
        total_carbs = sum(meal.carbs for meal in meals)
        total_proteins = sum(meal.proteins for meal in meals)
        total_fats = sum(meal.fats for meal in meals)
        total_calories = sum(meal.total_calories for meal in meals)
        
        return TodayStatsResponse(
            total_carbs=total_carbs,
            total_proteins=total_proteins,
            total_fats=total_fats,
            total_calories=total_calories,
            meal_count=len(meals),
            date=str(today)
        )
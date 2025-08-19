from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from database import get_db
from models import Meal
from schemas import StatsResponse, TodayStatsResponse

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/{username}", response_model=StatsResponse)
def get_user_stats(username: str, db: Session = Depends(get_db)):
    if not username or not username.strip():
        raise HTTPException(status_code=400, detail="Username cannot be empty")
        
    meals = db.query(Meal).filter(
        Meal.username == username.strip(),
        Meal.deleted_at.is_(None)
    ).all()
    
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

@router.get("/{username}/today", response_model=TodayStatsResponse)
def get_today_stats(username: str, db: Session = Depends(get_db)):
    if not username or not username.strip():
        raise HTTPException(status_code=400, detail="Username cannot be empty")
        
    today = date.today()
    meals = db.query(Meal).filter(
        Meal.username == username.strip(),
        Meal.deleted_at.is_(None),
        func.date(Meal.created_at) == today
    ).all()
    
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
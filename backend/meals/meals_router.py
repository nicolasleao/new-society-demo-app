from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List, Optional
from database import get_db
from models import Meal
from schemas import MealCreate, MealResponse

router = APIRouter(prefix="/meals", tags=["meals"])

@router.post("", response_model=MealResponse)
def create_meal(meal_data: MealCreate, db: Session = Depends(get_db)):
    meal = Meal(**meal_data.dict())
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

@router.get("/{username}", response_model=List[MealResponse])
def get_meals(
    username: str,
    date_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if not username or not username.strip():
        raise HTTPException(status_code=400, detail="Username cannot be empty")
        
    query = db.query(Meal).filter(
        Meal.username == username.strip(),
        Meal.deleted_at.is_(None)
    )
    
    if date_filter == "today":
        today = date.today()
        query = query.filter(func.date(Meal.created_at) == today)
    elif date_filter:
        try:
            filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(func.date(Meal.created_at) == filter_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    return query.order_by(Meal.created_at.desc()).all()

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    meal.deleted_at = func.now()
    db.commit()
    return {"message": "Meal deleted successfully"}
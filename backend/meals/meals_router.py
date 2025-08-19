from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import MealCreate, MealResponse
from .meals_service import MealsService

router = APIRouter(prefix="/meals", tags=["meals"])

@router.post("", response_model=MealResponse)
def create_meal(meal_data: MealCreate, db: Session = Depends(get_db)):
    service = MealsService(db)
    return service.create_meal(meal_data)

@router.get("/{username}", response_model=List[MealResponse])
def get_meals(
    username: str,
    date_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = MealsService(db)
    return service.get_meals_by_username(username, date_filter)

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    service = MealsService(db)
    return service.delete_meal(meal_id)
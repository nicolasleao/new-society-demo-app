from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import MealCreate, MealResponse, AIMealRequest, AIMealResponse
from .meals_service import MealsService
from .ai_service import AIService

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

@router.post("/ai-infer", response_model=AIMealResponse)
def infer_meal_from_description(request: AIMealRequest):
    """
    Uses AI to infer macronutrients from a natural language meal description.
    
    Args:
        request: Contains the meal description and username
        
    Returns:
        AIMealResponse with inferred meal data (title, carbs, proteins, fats, calories)
    """
    try:
        ai_service = AIService()
        meal_data = ai_service.infer_meal_macros(request.description)
        
        return AIMealResponse(
            title=meal_data.title,
            carbs=meal_data.carbs,
            proteins=meal_data.proteins,
            fats=meal_data.fats,
            total_calories=meal_data.total_calories
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to infer meal data: {str(e)}")
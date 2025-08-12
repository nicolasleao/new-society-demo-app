from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from typing import List, Optional
from database import engine, get_db
from models import Base, Meal
from schemas import MealCreate, MealResponse, StatsResponse, TodayStatsResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Calory Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://new-society-demo-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Calory Tracker API"}

@app.post("/meals", response_model=MealResponse)
def create_meal(meal_data: MealCreate, db: Session = Depends(get_db)):
    meal = Meal(**meal_data.dict())
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

@app.get("/meals/{username}", response_model=List[MealResponse])
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

@app.delete("/meals/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    meal.deleted_at = func.now()
    db.commit()
    return {"message": "Meal deleted successfully"}

@app.get("/stats/{username}", response_model=StatsResponse)
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

@app.get("/stats/{username}/today", response_model=TodayStatsResponse)
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
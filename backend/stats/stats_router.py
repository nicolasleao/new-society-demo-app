from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import StatsResponse, TodayStatsResponse
from .stats_service import StatsService

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/{username}", response_model=StatsResponse)
def get_user_stats(username: str, db: Session = Depends(get_db)):
    service = StatsService(db)
    return service.get_user_stats(username)

@router.get("/{username}/today", response_model=TodayStatsResponse)
def get_today_stats(username: str, db: Session = Depends(get_db)):
    service = StatsService(db)
    return service.get_today_stats(username)
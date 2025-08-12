from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    carbs = Column(Float, nullable=False)
    proteins = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    total_calories = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
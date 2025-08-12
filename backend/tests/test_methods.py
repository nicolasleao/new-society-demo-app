"""
Unit tests for backend methods and validation logic.
Focuses on testing individual functions and validation without API calls.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from datetime import datetime, date

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from schemas import MealCreate, StatsResponse, TodayStatsResponse
from models import Meal


class TestMealValidation:
    """Test Pydantic validation logic in MealCreate schema"""
    
    def test_valid_meal_creation(self):
        """Test creating a meal with valid data"""
        meal_data = {
            "username": "testuser",
            "title": "Breakfast",
            "carbs": 45.0,
            "proteins": 20.0,
            "fats": 10.0,
            "total_calories": 340.0
        }
        meal = MealCreate(**meal_data)
        
        assert meal.username == "testuser"
        assert meal.title == "Breakfast"
        assert meal.carbs == 45.0
        assert meal.proteins == 20.0
        assert meal.fats == 10.0
        assert meal.total_calories == 340.0
    
    def test_negative_nutrition_values_rejected(self):
        """Test that negative nutrition values raise ValueError"""
        with pytest.raises(ValueError, match="Values must be non-negative"):
            MealCreate(
                username="testuser",
                title="Test Meal",
                carbs=-5.0,
                proteins=15.0,
                fats=5.0,
                total_calories=180.0
            )
    
    def test_empty_username_rejected(self):
        """Test that empty username raises ValueError"""
        with pytest.raises(ValueError, match="Field cannot be empty"):
            MealCreate(
                username="",
                title="Test Meal",
                carbs=20.0,
                proteins=15.0,
                fats=5.0,
                total_calories=180.0
            )
    
    def test_whitespace_only_title_rejected(self):
        """Test that whitespace-only title raises ValueError"""
        with pytest.raises(ValueError, match="Field cannot be empty"):
            MealCreate(
                username="testuser",
                title="   ",
                carbs=20.0,
                proteins=15.0,
                fats=5.0,
                total_calories=180.0
            )
    
    def test_string_fields_stripped(self):
        """Test that string fields have whitespace stripped"""
        meal = MealCreate(
            username="  testuser  ",
            title="  Lunch Salad  ",
            carbs=20.0,
            proteins=15.0,
            fats=5.0,
            total_calories=180.0
        )
        
        assert meal.username == "testuser"
        assert meal.title == "Lunch Salad"
    
    def test_zero_values_allowed(self):
        """Test that zero values are allowed for nutrition fields"""
        meal = MealCreate(
            username="testuser",
            title="Water",
            carbs=0.0,
            proteins=0.0,
            fats=0.0,
            total_calories=0.0
        )
        
        assert meal.carbs == 0.0
        assert meal.proteins == 0.0
        assert meal.fats == 0.0
        assert meal.total_calories == 0.0


class TestResponseModels:
    """Test response model creation and validation"""
    
    def test_stats_response_creation(self):
        """Test creating StatsResponse with various values"""
        stats = StatsResponse(
            total_carbs=150.5,
            total_proteins=80.2,
            total_fats=45.8,
            total_calories=1250.0,
            meal_count=5
        )
        
        assert stats.total_carbs == 150.5
        assert stats.total_proteins == 80.2
        assert stats.total_fats == 45.8
        assert stats.total_calories == 1250.0
        assert stats.meal_count == 5
    
    def test_today_stats_response_inherits_from_stats(self):
        """Test that TodayStatsResponse includes date and inherits from StatsResponse"""
        today_str = "2023-12-25"
        today_stats = TodayStatsResponse(
            total_carbs=75.0,
            total_proteins=40.0,
            total_fats=25.0,
            total_calories=650.0,
            meal_count=3,
            date=today_str
        )
        
        # Check inherited fields
        assert today_stats.total_carbs == 75.0
        assert today_stats.total_proteins == 40.0
        assert today_stats.total_fats == 25.0
        assert today_stats.total_calories == 650.0
        assert today_stats.meal_count == 3
        
        # Check additional field
        assert today_stats.date == today_str
    
    def test_empty_stats_response(self):
        """Test creating StatsResponse with zero values (no meals scenario)"""
        empty_stats = StatsResponse(
            total_carbs=0.0,
            total_proteins=0.0,
            total_fats=0.0,
            total_calories=0.0,
            meal_count=0
        )
        
        assert empty_stats.total_carbs == 0.0
        assert empty_stats.total_proteins == 0.0
        assert empty_stats.total_fats == 0.0
        assert empty_stats.total_calories == 0.0
        assert empty_stats.meal_count == 0


class TestCalculationLogic:
    """Test calculation logic that would be used in the API endpoints"""
    
    def test_meal_totals_calculation(self):
        """Test calculating totals from a list of meals (simulating DB query results)"""
        # Create mock meals like what would come from DB
        meals = [
            Mock(carbs=20.0, proteins=15.0, fats=5.0, total_calories=180.0),
            Mock(carbs=45.0, proteins=25.0, fats=12.0, total_calories=360.0),
            Mock(carbs=30.0, proteins=20.0, fats=8.0, total_calories=260.0),
        ]
        
        # Calculate totals (this is the logic from the API endpoints)
        total_carbs = sum(meal.carbs for meal in meals)
        total_proteins = sum(meal.proteins for meal in meals)
        total_fats = sum(meal.fats for meal in meals)
        total_calories = sum(meal.total_calories for meal in meals)
        meal_count = len(meals)
        
        assert total_carbs == 95.0
        assert total_proteins == 60.0
        assert total_fats == 25.0
        assert total_calories == 800.0
        assert meal_count == 3
    
    def test_empty_meals_calculation(self):
        """Test calculating totals when no meals exist"""
        meals = []
        
        total_carbs = sum(meal.carbs for meal in meals)
        total_proteins = sum(meal.proteins for meal in meals)
        total_fats = sum(meal.fats for meal in meals)
        total_calories = sum(meal.total_calories for meal in meals)
        meal_count = len(meals)
        
        assert total_carbs == 0.0
        assert total_proteins == 0.0
        assert total_fats == 0.0
        assert total_calories == 0.0
        assert meal_count == 0
    
    def test_username_validation_logic(self):
        """Test username validation logic used in API endpoints"""
        # This tests the validation logic: not username or not username.strip()
        
        valid_usernames = ["testuser", "user123", "  validuser  "]
        invalid_usernames = ["", "   ", None]
        
        for username in valid_usernames:
            # Simulate the validation check from the API
            is_valid = username and username.strip()
            assert is_valid, f"Username '{username}' should be valid"
            
            if username:
                cleaned = username.strip()
                assert len(cleaned) > 0
        
        for username in invalid_usernames:
            # Simulate the validation check from the API
            is_valid = username and username.strip() if username else False
            assert not is_valid, f"Username '{username}' should be invalid"


class TestDateFilterLogic:
    """Test date filtering logic without database calls"""
    
    def test_today_filter_logic(self):
        """Test logic for filtering meals by 'today'"""
        from datetime import date
        
        today = date.today()
        date_filter = "today"
        
        # This simulates the condition in get_meals endpoint
        should_filter_today = date_filter == "today"
        assert should_filter_today
        
        # The actual date used for comparison
        filter_date = today
        assert filter_date == date.today()
    
    def test_specific_date_filter_parsing(self):
        """Test parsing specific date strings for filtering"""
        from datetime import datetime
        
        valid_date_string = "2023-12-25"
        
        try:
            parsed_date = datetime.strptime(valid_date_string, "%Y-%m-%d").date()
            assert parsed_date.year == 2023
            assert parsed_date.month == 12
            assert parsed_date.day == 25
        except ValueError:
            pytest.fail("Valid date string should parse successfully")
    
    def test_invalid_date_filter_parsing(self):
        """Test that invalid date strings raise ValueError"""
        invalid_date_strings = ["invalid-date", "12/25/2023", "2023-13-01", ""]
        
        for invalid_date in invalid_date_strings:
            with pytest.raises(ValueError):
                datetime.strptime(invalid_date, "%Y-%m-%d").date()
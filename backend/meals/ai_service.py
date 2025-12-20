import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional


class MealMacros(BaseModel):
    """Structured output model for OpenAI response"""
    title: str
    carbs: float
    proteins: float
    fats: float
    total_calories: float


class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=api_key)
    
    def infer_meal_macros(self, description: str) -> MealMacros:
        """
        Uses OpenAI to infer macronutrients from a meal description.
        
        Args:
            description: Natural language description of the meal
            
        Returns:
            MealMacros object with structured meal data
        """
        system_prompt = """You are a nutrition expert assistant. When given a description of a meal or food, 
analyze it and provide accurate estimates of its macronutrient content.

Guidelines:
- title: Create a concise, clear name for the meal (e.g., "Grilled Chicken Salad" not just "chicken")
- carbs: Carbohydrates in grams
- proteins: Protein content in grams
- fats: Fat content in grams
- total_calories: Total caloric content

Be as accurate as possible with standard portion sizes. If the description is vague, 
use typical serving sizes. All values should be positive numbers."""

        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this meal and provide macronutrient information: {description}"}
                ],
                response_format=MealMacros,
            )
            
            meal_data = completion.choices[0].message.parsed
            if not meal_data:
                raise ValueError("Failed to parse response from OpenAI")
            
            return meal_data
            
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")


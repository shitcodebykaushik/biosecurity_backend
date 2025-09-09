# app/nutrition/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

# This defines the input the farmer will send
class AnimalNutritionInput(BaseModel):
    animal_type: str = Field(..., description="e.g., 'cow' or 'hen'")
    weight_kg: float
    age_months: int
    # For dairy animals
    milk_yield_liters_per_day: Optional[float] = 0
    # For poultry
    is_laying: Optional[bool] = False

# This defines the output the API will return
class NutritionAdvisory(BaseModel):
    animal_status: str
    recommended_daily_feed: str
    health_notes: str

class VeterinaryContact(BaseModel):
    message: str
    phone: str
    emergency_mobile: str
    email: str
    
class HolisticAdvisory(BaseModel):
    animal_status: str
    recommended_daily_feed: str
    health_notes: str
    vaccination_schedule: str
    breeding_info: str
    housing_advice: str
    contact_vet: VeterinaryContact
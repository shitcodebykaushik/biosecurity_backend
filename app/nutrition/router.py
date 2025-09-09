# app/nutrition/router.py

from fastapi import APIRouter, Depends, Query
from . import services, schemas

router = APIRouter(
    prefix="/nutrition",
    tags=["Nutritional Advisory"]
)

# --- UPDATE THE ENDPOINT SIGNATURE HERE ---
@router.post("/calculate", response_model=schemas.HolisticAdvisory)
def get_nutrition_advisory(
    request: schemas.AnimalNutritionInput,
    lang: str = Query("en", enum=["en", "hi", "pa", "ta"], description="Language for the response")
):
    """
    Calculates nutritional needs and provides holistic advice in the chosen language.
    """
    return services.calculate_nutrition_needs(request=request, lang=lang)
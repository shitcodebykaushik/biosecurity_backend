# app/nutrition/services.py

from .schemas import AnimalNutritionInput, HolisticAdvisory
from .nutrition_data import NUTRITION_DATA, ANIMAL_TYPE_MAP
from fastapi import HTTPException

def get_translated_text(data_dict, key, lang):
    """
    A helper function to safely get translated text from a nested dictionary.
    It falls back to English ('en') if the requested language is not found.
    """
    if key in data_dict and isinstance(data_dict[key], dict):
        return data_dict[key].get(lang, data_dict[key].get("en", "Translation not available."))
    # Handle non-dictionary values like production_bonus numbers
    elif key in data_dict:
        return data_dict[key]
    return "Data not available."


def calculate_nutrition_needs(request: AnimalNutritionInput, lang: str):
    """
    Determines an animal's life stage and returns a holistic advisory plan
    in the specified language.
    """
    # 1. Standardize the animal type input (e.g., "गाय" -> "cow")
    canonical_animal_type = ANIMAL_TYPE_MAP.get(request.animal_type.lower())
    
    if not canonical_animal_type:
        raise HTTPException(status_code=400, detail=f"Animal type '{request.animal_type}' is not recognized.")
    
    if canonical_animal_type not in NUTRITION_DATA:
        raise HTTPException(status_code=404, detail=f"Nutritional data for '{canonical_animal_type}' not found.")
    
    data = NUTRITION_DATA[canonical_animal_type]
    vet_info = NUTRITION_DATA["veterinary_helpline"]

    # --- Logic for Ruminants (Cows, Buffaloes, Goats) ---
    if canonical_animal_type in ["cow", "buffalo", "goat"]:
        # Determine life stage
        if request.milk_yield_liters_per_day > 0:
            stage = "lactating"
        elif request.age_months < 6:
            stage = "kid" if canonical_animal_type == "goat" else "calf"
        elif request.age_months < 24:
            stage = "grower" if canonical_animal_type == "goat" else "heifer"
        else:
            stage = "dry"
        
        rules = data[stage]
        status_text = f"Status: {request.weight_kg}kg {stage.capitalize()} {canonical_animal_type.capitalize()}"
        
        # Calculate feed requirements
        dmi = request.weight_kg * (rules["dmi_percent_body_weight"] / 100)
        recommendation = (f"Provide ~{dmi:.2f} kg of Dry Matter per day. "
                          f"This should contain ~{rules['cp_percent']}% Crude Protein and "
                          f"~{rules['tdn_percent']}% TDN (Energy).")
        
        # Add production bonus with translated text
        if stage == "lactating" and "production_bonus" in rules:
            bonus_text = get_translated_text(rules, "production_bonus", lang)
            recommendation += f" Additionally, {bonus_text}"

        # Build and return the complete, translated advisory object
        return HolisticAdvisory(
            animal_status=status_text,
            recommended_daily_feed=recommendation,
            health_notes=get_translated_text(rules, "notes", lang),
            vaccination_schedule=get_translated_text(rules, "vaccination_schedule", lang),
            breeding_info=get_translated_text(rules, "breeding_info", lang),
            housing_advice=get_translated_text(rules, "housing_advice", lang),
            contact_vet={
                "message": get_translated_text(vet_info, "message", lang),
                "phone": get_translated_text(vet_info, "phone", lang),
                "emergency_mobile": get_translated_text(vet_info, "emergency_mobile", lang),
                "email": get_translated_text(vet_info, "email", lang)
            }
        )

    # --- Logic for Hens ---
    elif canonical_animal_type == "hen":
        if request.is_laying:
            stage = "layer"
        elif request.age_months < 2:
            stage = "chick"
        else:
            stage = "grower"
            
        rules = data[stage]
        status_text = f"Status: {stage.capitalize()} Hen"
        
        return HolisticAdvisory(
            animal_status=status_text,
            recommended_daily_feed=get_translated_text(rules, "feed_type", lang),
            health_notes=get_translated_text(rules, "notes", lang),
            # This general advice can also be added to the knowledge base for translation
            vaccination_schedule=get_translated_text({"vaccination_schedule": NUTRITION_DATA["cow"]["calf"]["vaccination_schedule"]}, "vaccination_schedule", lang),
            breeding_info="Breeding info for hens...",
            housing_advice="Housing advice for hens...",
            contact_vet={
                "message": get_translated_text(vet_info, "message", lang),
                "phone": get_translated_text(vet_info, "phone", lang),
                "emergency_mobile": get_translated_text(vet_info, "emergency_mobile", lang),
                "email": get_translated_text(vet_info, "email", lang)
            }
        )

    raise HTTPException(status_code=400, detail="Logic for this animal type is not fully implemented.")
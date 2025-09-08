# app/assessment/crud.py

from sqlalchemy.orm import Session
from .. import models
from . import schemas

# --- NEW SCORING LOGIC (PART 1: WEIGHTS) ---
# We define how many risk points each "bad" answer (False) is worth.
# Critical risks like disposal and fencing are worth more.
RISK_WEIGHTS = {
    # Category 1
    "has_fence": 10,
    "has_locked_gate": 5,
    "has_disinfectant_bath": 10,
    "uses_visitor_log": 5,
    # Category 2
    "is_all_in_all_out": 10,
    "is_quarantine_used": 15,
    "are_ages_separated": 5,
    # Category 3
    "is_feed_secure": 5,
    "is_water_source_safe": 10,
    "is_equipment_shared": 15,
    # Category 4
    "is_disposal_approved": 20, # This is a very high risk
    "is_waste_contained": 10,
}

QUESTION_TO_CATEGORY = {
    "has_fence": "Farm Perimeter & Access", "has_locked_gate": "Farm Perimeter & Access",
    "has_disinfectant_bath": "Farm Perimeter & Access", "uses_visitor_log": "Farm Perimeter & Access",
    "is_all_in_all_out": "Housing & Animal Management", "is_quarantine_used": "Housing & Animal Management",
    "are_ages_separated": "Housing & Animal Management",
    "is_feed_secure": "Feed, Water & Supplies", "is_water_source_safe": "Feed, Water & Supplies",
    "is_equipment_shared": "Feed, Water & Supplies",
    "is_disposal_approved": "Waste & Mortality Disposal", "is_waste_contained": "Waste & Mortality Disposal"
}


# ... (all your existing save_category functions are here) ...


# --- NEW SCORING LOGIC (PART 2: CALCULATION FUNCTION) ---
def calculate_risk_score(db: Session, farm_id: str):
    # Get all responses for this farm from the database
    responses = db.query(models.AssessmentResponse).filter(models.AssessmentResponse.farm_id == farm_id).all()
    
    if not responses:
        return {"total_score": 0, "risk_level": "Unknown", "top_weaknesses": ["No assessment data found."]}

    total_score = 0
    category_scores = {
        "Farm Perimeter & Access": 0,
        "Housing & Animal Management": 0,
        "Feed, Water & Supplies": 0,
        "Waste & Mortality Disposal": 0
    }

    # Calculate the score
    for response in responses:
        # If the answer is False, it's a risk. Add points.
        if response.answer is False:
            points = RISK_WEIGHTS.get(response.question_id, 0)
            total_score += points
            
            # Add points to the specific category for weakness ranking
            category = QUESTION_TO_CATEGORY.get(response.question_id)
            if category:
                category_scores[category] += points

    # Determine risk level
    if total_score <= 20:
        risk_level = "Low"
    elif total_score <= 50:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    # Find the categories with the highest scores (the biggest weaknesses)
    sorted_weaknesses = sorted(category_scores.items(), key=lambda item: item[1], reverse=True)
    top_weaknesses = [category for category, score in sorted_weaknesses if score > 0]

    return {
        "total_score": total_score,
        "risk_level": risk_level,
        "top_weaknesses": top_weaknesses[:3] # Return the top 3 weaknesses
    }
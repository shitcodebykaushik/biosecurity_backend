# app/assessment/crud.py

from sqlalchemy.orm import Session
from .. import models
from . import schemas

# --- SCORING LOGIC (WEIGHTS) ---
# We define how many risk points each "bad" answer (False) is worth.
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
    "is_disposal_approved": 20,
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

# --- CATEGORY 1 SAVE FUNCTION ---
def save_category1_responses(db: Session, responses: schemas.AssessmentCategory1):
    db_items = [
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="has_fence", answer=responses.has_fence),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="has_locked_gate", answer=responses.has_locked_gate),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="has_disinfectant_bath", answer=responses.has_disinfectant_bath),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="uses_visitor_log", answer=responses.uses_visitor_log),
    ]
    db.add_all(db_items)
    db.commit()
    return {"message": f"Successfully saved Category 1 responses for farm {responses.farm_id}"}

# --- CATEGORY 2 SAVE FUNCTION ---
def save_category2_responses(db: Session, responses: schemas.AssessmentCategory2):
    db_items = [
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="is_all_in_all_out", answer=responses.is_all_in_all_out),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="is_quarantine_used", answer=responses.is_quarantine_used),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="are_ages_separated", answer=responses.are_ages_separated),
    ]
    db.add_all(db_items)
    db.commit()
    return {"message": f"Successfully saved Category 2 responses for farm {responses.farm_id}"}

# --- CATEGORY 3 SAVE FUNCTION ---
def save_category3_responses(db: Session, responses: schemas.AssessmentCategory3):
    db_items = [
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="is_feed_secure", answer=responses.is_feed_secure),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="is_water_source_safe", answer=responses.is_water_source_safe),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="is_equipment_shared", answer=responses.is_equipment_shared),
    ]
    db.add_all(db_items)
    db.commit()
    return {"message": f"Successfully saved Category 3 responses for farm {responses.farm_id}"}

# --- CATEGORY 4 SAVE FUNCTION ---
def save_category4_responses(db: Session, responses: schemas.AssessmentCategory4):
    db_items = [
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="is_disposal_approved", answer=responses.is_disposal_approved),
        models.AssessmentResponse(farm_id=responses.farm_id, question_id="is_waste_contained", answer=responses.is_waste_contained),
    ]
    db.add_all(db_items)
    db.commit()
    return {"message": f"Successfully saved Category 4 responses for farm {responses.farm_id}"}

# --- SCORING CALCULATION FUNCTION ---
def calculate_risk_score(db: Session, farm_id: str):
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

    for response in responses:
        if response.answer is False:
            points = RISK_WEIGHTS.get(response.question_id, 0)
            total_score += points
            
            category = QUESTION_TO_CATEGORY.get(response.question_id)
            if category:
                category_scores[category] += points

    if total_score <= 20:
        risk_level = "Low"
    elif total_score <= 50:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    sorted_weaknesses = sorted(category_scores.items(), key=lambda item: item[1], reverse=True)
    top_weaknesses = [category for category, score in sorted_weaknesses if score > 0]

    return {
        "total_score": total_score,
        "risk_level": risk_level,
        "top_weaknesses": top_weaknesses[:3]
    }
# app/assessment/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from . import crud, schemas

router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ... (endpoints for category 1, 2, and 3 are here) ...

@router.post("/category3")
def submit_category3(response_data: schemas.AssessmentCategory3, db: Session = Depends(get_db)):
    return crud.save_category3_responses(db=db, responses=response_data)

# --- NEW CODE FOR CATEGORY 4 ---
@router.post("/category4")
def submit_category4(response_data: schemas.AssessmentCategory4, db: Session = Depends(get_db)):
    """
    Submit answers for Category 4: Waste & Mortality Disposal.
    """
    return crud.save_category4_responses(db=db, responses=response_data) 

@router.get("/results/{farm_id}", response_model=schemas.RiskResult)
def get_assessment_results(farm_id: str, db: Session = Depends(get_db)):
    """
    Calculates and returns the final risk score and analysis for a given farm.
    """
    return crud.calculate_risk_score(db=db, farm_id=farm_id)
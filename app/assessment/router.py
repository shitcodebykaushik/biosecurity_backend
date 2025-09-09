# app/assessment/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from . import crud, schemas

# --- SETUP ---
router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CATEGORY 1 ENDPOINT ---
@router.post("/category1")
def submit_category1(response_data: schemas.AssessmentCategory1, db: Session = Depends(get_db)):
    """
    Submit answers for Category 1: Farm Perimeter & Access.
    """
    return crud.save_category1_responses(db=db, responses=response_data)

# --- CATEGORY 2 ENDPOINT ---
@router.post("/category2")
def submit_category2(response_data: schemas.AssessmentCategory2, db: Session = Depends(get_db)):
    """
    Submit answers for Category 2: Housing & Animal Management.
    """
    return crud.save_category2_responses(db=db, responses=response_data)

# --- CATEGORY 3 ENDPOINT ---
@router.post("/category3")
def submit_category3(response_data: schemas.AssessmentCategory3, db: Session = Depends(get_db)):
    """
    Submit answers for Category 3: Feed, Water & Supplies.
    """
    return crud.save_category3_responses(db=db, responses=response_data)

# --- CATEGORY 4 ENDPOINT ---
@router.post("/category4")
def submit_category4(response_data: schemas.AssessmentCategory4, db: Session = Depends(get_db)):
    """
    Submit answers for Category 4: Waste & Mortality Disposal.
    """
    return crud.save_category4_responses(db=db, responses=response_data)

# --- FINAL RESULTS ENDPOINT ---
@router.get("/results/{farm_id}", response_model=schemas.RiskResult)
def get_assessment_results(farm_id: str, db: Session = Depends(get_db)):
    """
    Calculates and returns the final risk score and analysis for a given farm.
    """
    return crud.calculate_risk_score(db=db, farm_id=farm_id)
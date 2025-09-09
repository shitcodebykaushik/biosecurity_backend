# app/compliance/router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from . import crud, schemas

# We create a new router specifically for this module
router = APIRouter(
    prefix="/compliance",     # All URLs in this file will start with /compliance
    tags=["Compliance & Logs"] # Group these endpoints in the API docs
)

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/log/visitor")
def create_visitor_log(log_data: schemas.VisitorLogCreate, db: Session = Depends(get_db)):
    """
    Logs a new visitor entry for a farm.
    """
    return crud.log_visitor(db=db, log_data=log_data)
# Code for mortality log endpoint
@router.post("/log/mortality")
def create_mortality_log(log_data: schemas.MortalityLogCreate, db: Session = Depends(get_db)):
    """
    Logs a new animal mortality entry for a farm.
    """
    return crud.log_mortality(db=db, log_data=log_data)

@router.post("/log/task-completion")
def create_task_completion_log(log_data: schemas.TaskCompletionLogCreate, db: Session = Depends(get_db)):
    """
    Logs a completed biosecurity task.
    """
    return crud.log_task_completion(db=db, log_data=log_data)

@router.post("/farms", response_model=schemas.Farm)
def register_new_farm(farm: schemas.FarmCreate, db: Session = Depends(get_db)):
    """
    Register a new farm in the system.
    """
    return crud.create_farm(db=db, farm=farm)
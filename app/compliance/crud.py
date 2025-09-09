# app/compliance/crud.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models
from . import schemas

# --- Farm Management Functions ---

def get_farm_by_farm_id(db: Session, farm_id: str):
    """Fetches a single farm by its unique farm_id."""
    return db.query(models.Farm).filter(models.Farm.farm_id == farm_id).first()

def create_farm(db: Session, farm: schemas.FarmCreate):
    """Registers a new farm in the database, checking for duplicates first."""
    if get_farm_by_farm_id(db, farm_id=farm.farm_id):
        raise HTTPException(status_code=400, detail="Farm ID already registered")
    
    db_farm = models.Farm(**farm.dict())
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm

# --- Digital Logging Functions ---

def log_visitor(db: Session, log_data: schemas.VisitorLogCreate):
    """Logs a new visitor after validating the farm_id."""
    # 1. Validate if the farm exists
    farm = get_farm_by_farm_id(db, farm_id=log_data.farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm ID '{log_data.farm_id}' not found. Your work is incomplete because the farm is not registered.")

    # 2. If it exists, create the log entry
    db_log = models.ActivityLog(
        farm_id=log_data.farm_id,
        log_type="VISITOR_LOG",
        details=log_data.details
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def log_mortality(db: Session, log_data: schemas.MortalityLogCreate):
    """Logs animal mortality after validating the farm_id."""
    # 1. Validate if the farm exists
    farm = get_farm_by_farm_id(db, farm_id=log_data.farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm ID '{log_data.farm_id}' not found. Your work is incomplete because the farm is not registered.")

    # 2. If it exists, format details and create the log entry
    details_string = f"Count: {log_data.count}"
    if log_data.details:
        details_string += f". Notes: {log_data.details}"

    db_log = models.ActivityLog(
        farm_id=log_data.farm_id,
        log_type="MORTALITY_LOG",
        details=details_string
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def log_task_completion(db: Session, log_data: schemas.TaskCompletionLogCreate):
    """Logs a completed biosecurity task after validating the farm_id."""
    # 1. Validate if the farm exists
    farm = get_farm_by_farm_id(db, farm_id=log_data.farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Farm ID '{log_data.farm_id}' not found. Your work is incomplete because the farm is not registered.")

    # 2. If it exists, create the log entry
    db_log = models.ActivityLog(
        farm_id=log_data.farm_id,
        log_type="TASK_COMPLETED",
        details=log_data.details
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
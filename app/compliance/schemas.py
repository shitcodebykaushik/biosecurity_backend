# app/compliance/schemas.py

from pydantic import BaseModel
from typing import Optional

class VisitorLogCreate(BaseModel):
    farm_id: str
    # A simple text field for all visitor details
    details: str
    
    
    
# --- NEW CODE FOR MORTALITY LOG ---
class MortalityLogCreate(BaseModel):
    farm_id: str
    count: int  # The number of mortalities
    details: Optional[str] = None # Optional notes, e.g., "Observed coughing"

class TaskCompletionLogCreate(BaseModel):
    farm_id: str
    # The description of the task that was completed
    details: str
    
    
class FarmCreate(BaseModel):
    farm_id: str
    farm_name: str
    owner_name: str

class Farm(FarmCreate):
    id: int
    class Config:
        from_attributes = True
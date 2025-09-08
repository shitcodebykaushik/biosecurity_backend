# app/assessment/schemas.py

from pydantic import BaseModel
from typing import List

class AssessmentCategory1(BaseModel):
    farm_id: str
    has_fence: bool
    has_locked_gate: bool
    has_disinfectant_bath: bool
    uses_visitor_log: bool

    class Config:
        from_attributes = True

class AssessmentCategory2(BaseModel):
    farm_id: str
    is_all_in_all_out: bool
    is_quarantine_used: bool
    are_ages_separated: bool

    class Config:
        from_attributes = True

class AssessmentCategory3(BaseModel):
    farm_id: str
    is_feed_secure: bool
    is_water_source_safe: bool
    is_equipment_shared: bool

    class Config:
        from_attributes = True

# --- NEW CODE FOR CATEGORY 4 ---
class AssessmentCategory4(BaseModel):
    farm_id: str
    is_disposal_approved: bool # e.g., Govt pickup or proper composting
    is_waste_contained: bool   # e.g., Manure/wastewater in a secure tank

    class Config:
        from_attributes = True
    
    
# Risk calculation result schema
class RiskResult(BaseModel):
    total_score: int
    risk_level: str
    top_weaknesses: List[str]
# app/models.py

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(String, index=True) # A unique ID for each farm
    question_id = Column(String, index=True) # e.g., "has_fence"
    answer = Column(Boolean) # Storing Yes/No as True/False
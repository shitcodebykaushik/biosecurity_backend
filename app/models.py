# app/models.py

from sqlalchemy import Column, Integer, String, Boolean,DateTime,Text
from .database import Base
from sqlalchemy.sql import func


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True)
    farm_id = Column(String, unique=True, index=True, nullable=False)
    farm_name = Column(String)
    owner_name = Column(String)

class AssessmentResponse(Base):
    __tablename__ = "assessment_responses"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(String, index=True) # A unique ID for each farm
    question_id = Column(String, index=True) # e.g., "has_fence"
    answer = Column(Boolean) # Storing Yes/No as True/False
    
# --- NEW MODEL FOR THE DIGITAL LOGBOOK ---
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(String, index=True, nullable=False)
    
    # Type of log entry (e.g., "TASK_COMPLETED", "VISITOR_LOG", "MORTALITY_LOG")
    log_type = Column(String, index=True, nullable=False)
    
    # Use the database's current time as the default
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # A text field to store details, like a visitor's name or a task description
    details = Column(Text, nullable=False)
    
    
    
class IDCounter(Base):
    __tablename__ = "id_counters"
    
    # Animal type will be the primary key (e.g., 'COW', 'BUFFALO')
    animal_type = Column(String, primary_key=True, index=True)
    last_id = Column(Integer, default=0)

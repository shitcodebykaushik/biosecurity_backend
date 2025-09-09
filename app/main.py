# app/main.py

from fastapi import FastAPI
from . import models
from .database import engine
from .assessment.router import router as assessment_router # <-- Correctly imports the router object
from .compliance.router import router as compliance_router # <-- ADD THIS LINE
from .nutrition.router import router as nutrition_router # <-- ADD THIS

# This command creates the database table defined in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(assessment_router) # <-- ADD THIS LINE
app.include_router(compliance_router) # <-- ADD THIS LINE
app.include_router(nutrition_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Biosecurity Backend API"}
# From the root of the project 
 uvicorn app.main:app --reload

Digital Record-Keeping & Compliance
# Assessment folder 
# Module 1 - Risk Self-Assessment module.
- Here we are collecting the data and store it in db then analyze the rist  and provide the insight of it .
# Endpoint 1
- `http://127.0.0.1:8000/assessment/category1`
Payload  {
  "farm_id": "FARM_LUD_001",
  "has_fence": true,
  "has_locked_gate": true,
  "has_disinfectant_bath": false,
  "uses_visitor_log": true
}

# Endpoint 2 
http://127.0.0.1:8000/assessment/category2

Payload {
    {
  "farm_id": "FARM_LUD_001",
  "is_all_in_all_out": true,
  "is_quarantine_used": false,
  "are_ages_separated": true
}
}

# Endpoint 3 
http://127.0.0.1:8000/assessment/category3

{
  "farm_id": "FARM_LUD_001",
  "is_feed_secure": true,
  "is_water_source_safe": true,
  "is_equipment_shared": false
}

# Endpoint 4 
http://127.0.0.1:8000/assessment/category4
- Payload
{
  "farm_id": "FARM_LUD_001",
  "is_disposal_approved": false,
  "is_waste_contained": true
}

# Compilence folder 
# Module 2 Digital Record-Keeping and Compliance Tracking Module. 
# Endpoint 1
http://127.0.0.1:8000/compliance/log/visitor
- Payload
{
  "farm_id": "FARM_LUD_001",
  "details": "Visitor: Dr. Sharma (Vet), Vehicle: PB 10 XY 5678, Purpose: Health Checkup"
}

# Endpoint 2

http://127.0.0.1:8000/compliance/log/mortality
- Payload
{
  "farm_id": "FARM_LUD_001",
  "count": 3,
  "details": "Observed in Shed-B, no other symptoms"
}

# Endpoint 3

POST http://127.0.0.1:8000//compliance/log/task-completion
-Payload
{
  "farm_id": "FARM_XYZ_999",
  "details": "This will fail."
}

# Milk Egg calculation for animal
http://127.0.0.1:8000/nutrition/calculate?lang={language_code}

- The language code 
en for English
hi for Hindi
pa for Punjabi
ta for Tamil


- Payload  
{
  "animal_type": "गाय",
  "weight_kg": 450,
  "age_months": 36,
  "milk_yield_liters_per_day": 10
} 

As of now the payload is 50/multilingual .


# Breeding & Reproduction Cycle Management

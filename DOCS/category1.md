
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

{
  "farm_id": "FARM_LUD_001",
  "is_disposal_approved": false,
  "is_waste_contained": true
}


# Endpoint 5

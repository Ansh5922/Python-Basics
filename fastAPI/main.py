from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# 1. Initialize FastAPI application
app = FastAPI()


# 2. Pydantic Models (Schemas)
# Pydantic is used to validate the incoming data from the user/client.

# Used for creating a patient (POST) and full update (PUT)
class Patient(BaseModel):
    name: str
    age: int
    disease: str


# Used for partial update (PATCH) where all fields are optional
class PatientPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    disease: Optional[str] = None


# 3. Import Dummy Dataset
# We import our dummy dataset from the separate data.py file
from data import patients


# =========================================================
# CRUD OPERATIONS
# =========================================================

# ---------------------------------------------------------
# C - CREATE (POST)
# Adds a new patient to our dictionary.
# ---------------------------------------------------------
@app.post("/patients")
def create_patient(patient: Patient):
    # Generate a new ID by taking the max existing ID + 1
    new_id = max(patients.keys(), default=0) + 1

    # Store patient data in dictionary
    patients[new_id] = {
        "id": new_id,
        "name": patient.name,
        "age": patient.age,
        "disease": patient.disease
    }
    return {"message": "Patient created successfully", "patient": patients[new_id]}


# ---------------------------------------------------------
# R - RETRIEVE (GET)
# Read data from the database.
# ---------------------------------------------------------

# 1. Get ALL patients
@app.get("/patients")
def get_all_patients():
    # Return all values from our dictionary as a list
    return list(patients.values())


# 2. Get a SINGLE patient by ID
@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    # Check if patient exists
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients[patient_id]


# ---------------------------------------------------------
# U - UPDATE (PUT & PATCH)
# Modify existing data.
# ---------------------------------------------------------

# PUT -> Full update: Replaces ALL data of the patient.
@app.put("/patients/{patient_id}")
def update_patient_full(patient_id: int, patient: Patient):
    # Check if patient exists
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Overwrite the entire patient data
    patients[patient_id] = {
        "id": patient_id,
        "name": patient.name,
        "age": patient.age,
        "disease": patient.disease
    }
    return {"message": "Patient fully updated (PUT)", "patient": patients[patient_id]}


# PATCH -> Partial update: Updates ONLY the fields sent by the user.
@app.patch("/patients/{patient_id}")
def update_patient_partial(patient_id: int, patient: PatientPatch):
    # Check if patient exists
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Only update fields that were provided (not None)
    if patient.name is not None:
        patients[patient_id]["name"] = patient.name
    if patient.age is not None:
        patients[patient_id]["age"] = patient.age
    if patient.disease is not None:
        patients[patient_id]["disease"] = patient.disease

    return {"message": "Patient partially updated (PATCH)", "patient": patients[patient_id]}


# ---------------------------------------------------------
# D - DELETE (DELETE)
# Remove a patient from the dictionary.
# ---------------------------------------------------------
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    # Check if patient exists
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Remove the patient
    deleted_patient = patients.pop(patient_id)
    return {"message": "Patient deleted successfully", "deleted_patient": deleted_patient}

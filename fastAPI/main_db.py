"""
FastAPI with PostgreSQL (CRUD Operations)
=========================================
This file demonstrates how to connect FastAPI to a PostgreSQL database
using SQLAlchemy ORM and perform full CRUD (Create, Retrieve, Update, Delete) operations.

Prerequisites:
  pip install fastapi uvicorn sqlalchemy psycopg2-binary
"""

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# =========================================================
# 1. DATABASE CONFIGURATION & CONNECTION
# =========================================================

# Database connection URL format:
# postgresql://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL = "postgresql://postgres:password@localhost:5432/hospital_db"

# Create the SQLAlchemy Engine
# The engine manages database connections
engine = create_engine(DATABASE_URL)

# Create a sessionmaker
# Each request will get its own temporary database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQLAlchemy database models
Base = declarative_base()


# =========================================================
# 2. SQLALCHEMY DATABASE MODEL (TABLE STRUCTURE)
# =========================================================
class PatientModel(Base):
    """
    Defines the 'patients' table in PostgreSQL.
    """
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    disease = Column(String, nullable=False)


# Automatically create the table in PostgreSQL if it doesn't exist already
Base.metadata.create_all(bind=engine)


# =========================================================
# 3. PYDANTIC SCHEMAS (DATA VALIDATION)
# =========================================================

# Schema for creating a new patient (POST) and full update (PUT)
class PatientCreate(BaseModel):
    name: str
    age: int
    disease: str


# Schema for partial update (PATCH) - all fields are optional
class PatientPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    disease: Optional[str] = None


# Schema for returning patient data to the client
class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    disease: str

    # Enables reading data directly from SQLAlchemy objects
    class Config:
        from_attributes = True


# =========================================================
# 4. DATABASE SESSION DEPENDENCY
# =========================================================
def get_db():
    """
    FastAPI dependency that provides a database session for each request,
    and automatically closes it when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# 5. FASTAPI APP INITIALIZATION
# =========================================================
app = FastAPI(title="Patient Management API with PostgreSQL")


# =========================================================
# 6. CRUD API ENDPOINTS
# =========================================================

# ---------------------------------------------------------
# C - CREATE (POST /patients)
# ---------------------------------------------------------
@app.post("/patients", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """
    Create a new patient record in the PostgreSQL database.
    """
    # 1. Create a new SQLAlchemy model instance
    db_patient = PatientModel(
        name=patient.name,
        age=patient.age,
        disease=patient.disease
    )

    # 2. Add to session and save (commit) to database
    db.add(db_patient)
    db.commit()

    # 3. Refresh to get the generated ID from the database
    db.refresh(db_patient)

    return db_patient


# ---------------------------------------------------------
# R - RETRIEVE ALL (GET /patients)
# ---------------------------------------------------------
@app.get("/patients", response_model=List[PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):
    """
    Retrieve all patient records from the database.
    """
    patients = db.query(PatientModel).all()
    return patients


# ---------------------------------------------------------
# R - RETRIEVE BY ID (GET /patients/{patient_id})
# ---------------------------------------------------------
@app.get("/patients/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single patient by their primary key (ID).
    """
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ---------------------------------------------------------
# U - FULL UPDATE (PUT /patients/{patient_id})
# ---------------------------------------------------------
@app.put("/patients/{patient_id}", response_model=PatientResponse)
def update_patient_full(patient_id: int, updated_data: PatientCreate, db: Session = Depends(get_db)):
    """
    PUT operation: Completely replaces all fields of an existing patient.
    """
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Overwrite all fields
    patient.name = updated_data.name
    patient.age = updated_data.age
    patient.disease = updated_data.disease

    db.commit()
    db.refresh(patient)
    return patient


# ---------------------------------------------------------
# U - PARTIAL UPDATE (PATCH /patients/{patient_id})
# ---------------------------------------------------------
@app.patch("/patients/{patient_id}", response_model=PatientResponse)
def update_patient_partial(patient_id: int, patch_data: PatientPatch, db: Session = Depends(get_db)):
    """
    PATCH operation: Updates ONLY the fields provided in the request body.
    """
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Only update fields that were provided (not None)
    if patch_data.name is not None:
        patient.name = patch_data.name
    if patch_data.age is not None:
        patient.age = patch_data.age
    if patch_data.disease is not None:
        patient.disease = patch_data.disease

    db.commit()
    db.refresh(patient)
    return patient


# ---------------------------------------------------------
# D - DELETE (DELETE /patients/{patient_id})
# ---------------------------------------------------------
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete a patient record from PostgreSQL.
    """
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return {"message": f"Patient with ID {patient_id} deleted successfully"}

"""
================================================================================
           PYDANTIC V2 COMPLETE REVISION NOTES & CRASH COURSE
           Based on: github.com/campusx-official/pydantic-crash-course
================================================================================

Table of Contents:
  1. Why Pydantic? (Type Validation, Coercion, Field Constraints & Metadata)
  2. Field Validators (@field_validator, Modes, Transformation)
  3. Model Validators (@model_validator, Cross-Field Validation)
  4. Computed Fields (@computed_field, Derived Properties)
  5. Nested Models (Composition, Hierarchical Data, Automatic Validation)
  6. Serialization & Exporting (.model_dump, .model_dump_json, Filters)
================================================================================
"""

# ==============================================================================
# DETAILED DESCRIPTION OF IMPORTS
# ==============================================================================
# 1. From Python's standard `typing` module:
#    - List:       Specifies a homogeneous list of items, e.g., List[str].
#    - Dict:       Specifies key-value mappings with strict types, e.g., Dict[str, str].
#    - Optional:   Shorthand for Union[Type, None]. Marks a field as nullable/optional.
#    - Annotated:  Python 3.9+ syntax used to attach metadata (like Field()) to a type.
from typing import List, Dict, Optional, Annotated

# 2. From `pydantic`:
#    - BaseModel:         The core class all Pydantic models inherit from. Handles validation,
#                         type coercion, initialization, and serialization (.model_dump).
#    - EmailStr:          A specialized string type that validates standard email address formats
#                         (e.g., checks for '@' and valid domain syntax).
#    - AnyUrl:            A specialized string type that validates valid URL formats
#                         (e.g., checks for scheme 'http/https' and host).
#    - Field:             Used inside models to add extra validation constraints (gt, lt,
#                         min_length, max_length) and documentation metadata (title, description, examples).
#    - field_validator:   Decorator used to write custom validation or transformation logic
#                         for an INDIVIDUAL field (e.g., capitalizing names, checking domains).
#    - model_validator:   Decorator used for CROSS-FIELD validation (logic that depends
#                         on multiple fields at once, e.g., checking emergency contact if age > 60).
#    - computed_field:    Decorator (used with @property) to define dynamic, calculated attributes
#                         (e.g., BMI) that are automatically included in .model_dump() and JSON exports.
from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator,
    model_validator,
    computed_field
)


# ==============================================================================
# SECTION 1: WHY PYDANTIC? (Validation + Type Coercion + Field Constraints)
# ==============================================================================
"""
KEY CONCEPTS:
- Python is dynamically typed. Standard type hints (x: int) DO NOT enforce types at runtime.
- Pydantic enforces types at runtime and performs automatic 'Type Coercion'
  (e.g., string '30' is automatically converted to integer 30).
- EmailStr & AnyUrl: Specialized string types with built-in format validation.
- Field(...): Adds validation rules (gt, lt, min_length, max_length) and metadata
  (title, description, examples, default).
- Annotated[Type, Field(...)]: Recommended modern Python syntax for attaching metadata.
"""

class PatientBasic(BaseModel):
    # Field with rich documentation & length constraint
    name: Annotated[
        str,
        Field(max_length=50, title="Patient Name", description="Name under 50 chars", examples=["Nitish", "Amit"])
    ]
    
    # Specialized format validations (requires email-validator package for EmailStr)
    email: EmailStr
    linkedin_url: AnyUrl

    # Numeric constraints: gt (greater than), lt (less than)
    age: int = Field(gt=0, lt=120)

    # strict=True disables automatic type coercion (e.g., "75.2" as a string will raise an error)
    weight: Annotated[float, Field(gt=0, strict=True)]

    # Default values & Optional fields
    married: Annotated[Optional[bool], Field(default=None, description="Is the patient married or not")]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]


def run_section_1_demo():
    print("\n--- SECTION 1: Basic Validation & Type Coercion ---")
    data = {
        "name": "Nitish",
        "email": "abc@gmail.com",
        "linkedin_url": "https://linkedin.com/in/nitish",
        "age": "30",         # Notice: string '30' gets coerced to integer 30!
        "weight": 75.2,      # Float as strict float
        "contact_details": {"phone": "9876543210"}
    }
    patient = PatientBasic(**data)
    print("Patient created successfully!")
    print(f"Name: {patient.name}, Age: {patient.age} (type: {type(patient.age).__name__})")
    print(f"Email: {patient.email}, Weight: {patient.weight}kg")


# ==============================================================================
# SECTION 2: FIELD VALIDATORS (@field_validator)
# ==============================================================================
"""
KEY CONCEPTS:
- Used to validate or transform INDIVIDUAL fields.
- Must be decorated with @field_validator('<field_name>') AND @classmethod.
- Modes:
    * mode='after' (default): Runs AFTER Pydantic's internal type coercion/validation.
    * mode='before': Runs BEFORE Pydantic attempts to coerce types.
- Can raise ValueError to fail validation with a clean error message.
- Can return a modified value to perform sanitization / transformation (e.g., .upper()).
"""

class PatientWithFieldValidators(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # Example 1: Custom Business Logic Validation (Email domain check)
    @field_validator("email")
    @classmethod
    def email_domain_validator(cls, value: str):
        valid_domains = ["hdfc.com", "icici.com", "hospital.org"]
        domain = value.split("@")[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain '{domain}' is not authorized. Allowed: {valid_domains}")
        return value

    # Example 2: Data Transformation (Normalize name to uppercase)
    @field_validator("name")
    @classmethod
    def transform_name_to_upper(cls, value: str):
        return value.strip().upper()

    # Example 3: Value Range Validation with mode='after'
    @field_validator("age", mode="after")
    @classmethod
    def validate_age_range(cls, value: int):
        if not (0 < value < 120):
            raise ValueError("Age must be strictly between 0 and 120")
        return value


def run_section_2_demo():
    print("\n--- SECTION 2: Field Validators & Transformation ---")
    data = {
        "name": "  nitish sharma  ",   # Will be stripped and capitalized to NITISH SHARMA
        "email": "doctor@icici.com",   # Matches allowed domains
        "age": "32",                  # Coerced to 32, then validated by validate_age_range
        "weight": 72.5,
        "married": True,
        "allergies": ["dust", "pollen"],
        "contact_details": {"phone": "1234567890"}
    }
    p = PatientWithFieldValidators(**data)
    print(f"Transformed Name: {p.name}")
    print(f"Validated Email: {p.email}")


# ==============================================================================
# SECTION 3: MODEL VALIDATORS (@model_validator)
# ==============================================================================
"""
KEY CONCEPTS:
- Used for CROSS-FIELD VALIDATION (when validation depends on TWO OR MORE fields).
- mode='after': Validator runs on the model instance (self) after individual fields are validated.
- mode='before': Validator runs on the raw input dictionary before field validation.
- Must return the model instance (in mode='after') or input dict (in mode='before').
"""

class PatientWithModelValidator(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # Cross-field rule: If patient is older than 60, emergency contact is MANDATORY
    @model_validator(mode="after")
    def validate_emergency_contact_for_seniors(self):
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError(f"Patient is {self.age} years old (>60). An 'emergency' contact number is mandatory!")
        return self


def run_section_3_demo():
    print("\n--- SECTION 3: Model Validator (Cross-Field) ---")
    data = {
        "name": "Robert Senior",
        "email": "robert@icici.com",
        "age": 68,
        "weight": 80.0,
        "married": True,
        "allergies": [],
        "contact_details": {
            "phone": "9998887776",
            "emergency": "1122334455"  # Required because age > 60
        }
    }
    p = PatientWithModelValidator(**data)
    print(f"Senior Patient Verified: {p.name}, Emergency Contact: {p.contact_details['emergency']}")


# ==============================================================================
# SECTION 4: COMPUTED FIELDS (@computed_field)
# ==============================================================================
"""
KEY CONCEPTS:
- Used to define dynamic, calculated/derived properties.
- Combines @computed_field with @property.
- Return type annotation (e.g. -> float) is MANDATORY.
- Unlike standard Python properties, Pydantic computed fields are AUTOMATICALLY
  included in model serialization (.model_dump() and .model_dump_json()).
"""

class PatientWithBMI(BaseModel):
    name: str
    email: EmailStr
    weight: float  # in kilograms
    height: float  # in meters

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculates Body Mass Index: weight / (height^2)"""
        return round(self.weight / (self.height ** 2), 2)


def run_section_4_demo():
    print("\n--- SECTION 4: Computed Fields (@computed_field) ---")
    p = PatientWithBMI(
        name="Amit",
        email="amit@icici.com",
        weight=75.0,
        height=1.75
    )
    print(f"Weight: {p.weight} kg, Height: {p.height} m")
    print(f"Calculated BMI: {p.bmi}")
    print(f"Included in model_dump(): {p.model_dump()}")


# ==============================================================================
# SECTION 5: NESTED MODELS (Data Composition)
# ==============================================================================
"""
KEY CONCEPTS:
- Models can be composed inside other models (Address inside Patient).
- Benefits:
    1. Organization: Groups related fields cleanly.
    2. Reusability: Use Address across Patient, Doctor, Hospital models.
    3. Automatic Validation: Nested models are recursively validated automatically.
    4. Input format: Can accept either an instantiated model OR a raw nested dictionary.
"""

class Address(BaseModel):
    city: str
    state: str
    pin: str


class PatientWithAddress(BaseModel):
    name: str
    gender: str
    age: int
    address: Address  # Nested Pydantic Model


def run_section_5_demo():
    print("\n--- SECTION 5: Nested Models ---")
    # Pydantic automatically instantiates Address from the nested dictionary!
    patient_data = {
        "name": "Neha",
        "gender": "Female",
        "age": 28,
        "address": {
            "city": "Gurgaon",
            "state": "Haryana",
            "pin": "122001"
        }
    }
    p = PatientWithAddress(**patient_data)
    print(f"Patient: {p.name}")
    print(f"City: {p.address.city}, State: {p.address.state}, Pin: {p.address.pin}")


# ==============================================================================
# SECTION 6: SERIALIZATION & EXPORTING (.model_dump)
# ==============================================================================
"""
KEY CONCEPTS:
- In Pydantic V2:
    * .model_dump(): Converts model to Python dict (Replaces v1 .dict()).
    * .model_dump_json(): Converts model to JSON string (Replaces v1 .json()).
- Useful Parameters:
    * exclude_unset=True: Only exports fields explicitly passed during creation (ignores default values).
    * exclude_none=True: Drops any fields with value None.
    * include={'name', 'age'}: Only export specified fields.
    * exclude={'address'}: Exclude specified fields.
"""

class PatientSerialization(BaseModel):
    name: str
    gender: str = "Male"       # Default value
    age: int
    allergies: Optional[List[str]] = None
    address: Address


def run_section_6_demo():
    print("\n--- SECTION 6: Serialization (.model_dump) ---")
    patient = PatientSerialization(
        name="Vikram",
        age=35,
        address=Address(city="Delhi", state="Delhi", pin="110001")
        # Notice: 'gender' and 'allergies' are not explicitly provided
    )

    print("1. Standard model_dump() (includes defaults and None):")
    print(patient.model_dump())

    print("\n2. model_dump(exclude_unset=True) (excludes untouched defaults & None):")
    print(patient.model_dump(exclude_unset=True))

    print("\n3. model_dump(include={'name', 'age'}):")
    print(patient.model_dump(include={"name", "age"}))

    print("\n4. model_dump_json():")
    print(patient.model_dump_json())


# ==============================================================================
# RUN ALL DEMOS
# ==============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("      PYDANTIC CRASH COURSE - ALL TOPICS REVISION      ")
    print("=" * 60)
    run_section_1_demo()
    run_section_2_demo()
    run_section_3_demo()
    run_section_4_demo()
    run_section_5_demo()
    run_section_6_demo()
    print("\n" + "=" * 60)
    print("      ALL REVISION TOPICS EXECUTED SUCCESSFULLY!      ")
    print("=" * 60)

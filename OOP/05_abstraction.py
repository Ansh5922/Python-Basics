"""
================================================================================
 MODULE 05: ABSTRACTION & INTERFACES (CONTRACTS)
================================================================================

Welcome to the 4th Classical Pillar of Object-Oriented Programming: ABSTRACTION!

Table of Contents:
  1. Real-World Analogy: Car Pedals & The Coffee Machine
  2. What is Abstraction? (Hiding Complexity, Exposing Contracts)
  3. Abstract Base Classes (ABCs) via Python's 'abc' Module
  4. Enforcing Subclass Compliance with @abstractmethod
  5. Abstract Properties: Combining @property with @abstractmethod
  6. Virtual Subclasses & Dynamic Checks (__subclasshook__)
  7. Modern Python: Structural Subtyping with typing.Protocol (PEP 544)
  8. Nominal Subtyping (ABC) vs Structural Subtyping (Protocol)
  9. Common Beginner Pitfall: Forgetting to Implement an Abstract Method
 10. Runnable Hands-on Demonstration
================================================================================
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


# ==============================================================================
# 1. REAL-WORLD ANALOGY: WHAT IS ABSTRACTION?
# ==============================================================================
"""
Think of Driving a Car:
  - When you press the accelerator pedal, the car speeds up.
  - You do NOT need to know:
      * How much fuel the injector sprayed into the combustion cylinder
      * The gear ratio selected inside the transmission
      * The electronic signal voltages sent by the engine control unit (ECU)
  - The pedal is an ABSTRACTION. It hides massive internal complexity behind
    a simple, safe, intuitive interface!

Think of a TV Remote:
  - You press the "Power" button. You don't know the exact infrared pulse frequency
    or circuit board voltages. The button is the abstract contract.

IN SOFTWARE ENGINEERING:
  - Abstraction defines WHAT an object should do without dictating HOW it does it.
  - It establishes a STRICT CONTRACT that all implementations must honor!
"""


# ==============================================================================
# 2, 3, 4. ABSTRACT BASE CLASSES (ABCs) & @abstractmethod
# ==============================================================================
class DatabaseConnector(ABC):
    """
    Abstract Base Class (ABC) serving as an interface contract.
    You CANNOT instantiate this class directly: `db = DatabaseConnector()` -> ERROR!
    """

    @abstractmethod
    def connect(self) -> None:
        """Subclasses MUST provide their own connection logic."""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> list:
        """Subclasses MUST implement query execution."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Subclasses MUST implement disconnection cleanup."""
        pass

    # Concrete helper method (ABCs can still have fully implemented methods!)
    def ping(self) -> str:
        return "[DATABASE STATUS] Heartbeat signal OK."


# Concrete Implementation 1: PostgreSQL
class PostgreSQLConnector(DatabaseConnector):
    def __init__(self, host: str, dbname: str):
        self.host: str = host
        self.dbname: str = dbname
        self.is_connected: bool = False

    def connect(self) -> None:
        self.is_connected = True
        print(f"[PostgreSQL] Connected to {self.dbname} at {self.host}:5432.")

    def execute_query(self, query: str) -> list:
        if not self.is_connected:
            raise ConnectionError("Cannot query: PostgreSQL is not connected!")
        return [f"Row 1 for query: '{query}'", f"Row 2 for query: '{query}'"]

    def disconnect(self) -> None:
        self.is_connected = False
        print("[PostgreSQL] Connection closed.")


# Concrete Implementation 2: MongoDB
class MongoDBConnector(DatabaseConnector):
    def __init__(self, uri: str):
        self.uri: str = uri
        self.is_connected: bool = False

    def connect(self) -> None:
        self.is_connected = True
        print(f"[MongoDB] Connected to cluster: {self.uri}")

    def execute_query(self, query: str) -> list:
        if not self.is_connected:
            raise ConnectionError("Cannot query: MongoDB is not connected!")
        return [{"_id": "1", "data": query}]

    def disconnect(self) -> None:
        self.is_connected = False
        print("[MongoDB] Cluster connection released.")


# ==============================================================================
# 5. ABSTRACT PROPERTIES (@property + @abstractmethod)
# ==============================================================================
class CloudStorage(ABC):
    """Abstract contract enforcing both methods and properties."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Any storage subclass MUST declare its provider name."""
        pass

    @abstractmethod
    def upload_file(self, filename: str) -> str:
        pass


class S3Storage(CloudStorage):
    @property
    def provider_name(self) -> str:
        return "Amazon Web Services (AWS S3)"

    def upload_file(self, filename: str) -> str:
        return f"[AWS S3] Uploaded '{filename}' to S3 bucket."


# ==============================================================================
# 6 & 7. MODERN PYTHON: STRUCTURAL SUBTYPING (typing.Protocol)
# ==============================================================================
"""
ABC vs PROTOCOL:
  - ABC (Nominal Subtyping): A class MUST explicitly inherit: `class MyClass(MyABC)`.
  - Protocol (Structural Subtyping / Compile-Time Duck Typing - PEP 544):
    A class satisfies the contract AUTOMATICALLY if it has the matching methods,
    WITHOUT needing to inherit from the Protocol!

Use `@runtime_checkable` if you want `isinstance(obj, MyProtocol)` to work at runtime.
"""

@runtime_checkable
class Renderable(Protocol):
    """Any object with a render() method satisfies this protocol."""
    def render(self) -> str:
        ...


# Notice: This class DOES NOT inherit from Renderable!
class PDFDocument:
    def render(self) -> str:
        return "[PDF ENGINE] Rendering formatted 300 DPI vector pages."


# Notice: This class DOES NOT inherit from Renderable either!
class HTMLPage:
    def render(self) -> str:
        return "[HTML ENGINE] Rendering DOM tree with CSS styling."


def display_content(doc: Renderable) -> None:
    """Accepts ANY object that conforms to the Renderable protocol."""
    print(doc.render())


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 05: ABSTRACTION & INTERFACES DEMONSTRATION")
    print("=" * 70)

    # 1. Attempting to Instantiate an ABC Directly (Proving it blocks instantiation)
    print("\n--- 1. Testing ABC Instantiation Guard ---")
    try:
        # This MUST fail because DatabaseConnector is an abstract blueprint!
        db = DatabaseConnector()
    except TypeError as err:
        print(f"Instinctive guard passed! Cannot instantiate ABC directly:")
        print(f"  Error: {err}")

    # 2. Polymorphic Database Usage via Common Abstract Interface
    print("\n--- 2. Working with Concrete Database Implementations ---")
    databases: list[DatabaseConnector] = [
        PostgreSQLConnector(host="localhost", dbname="hospital_db"),
        MongoDBConnector(uri="mongodb://cloud.atlas.com:27017")
    ]

    for db in databases:
        print(f"\nTesting database: {db.__class__.__name__}")
        print(db.ping())  # Inherited concrete helper method
        db.connect()
        results = db.execute_query("SELECT * FROM patients")
        print(f"Query Results: {results}")
        db.disconnect()

    # 3. Abstract Properties
    print("\n--- 3. Testing Abstract Properties ---")
    s3 = S3Storage()
    print(f"Storage Provider: {s3.provider_name}")
    print(s3.upload_file("patient_xray.png"))

    # 4. Protocols (Structural Subtyping / Duck Typing Contracts)
    print("\n--- 4. Testing typing.Protocol (Zero-Inheritance Contracts) ---")
    pdf = PDFDocument()
    html = HTMLPage()

    print(f"Is PDFDocument an instance of Renderable? {isinstance(pdf, Renderable)}")
    print(f"Is HTMLPage an instance of Renderable?   {isinstance(html, Renderable)}")

    print("\nRendering polymorphic protocol documents:")
    display_content(pdf)
    display_content(html)

    print("\n" + "=" * 70)
    print("      MODULE 05 COMPLETE: ABSTRACTION MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

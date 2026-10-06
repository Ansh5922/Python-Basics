"""
================================================================================
 MODULE 03: INHERITANCE & CODE REUSE
================================================================================

Welcome to the 2nd Classical Pillar of Object-Oriented Programming: INHERITANCE!

Table of Contents:
  1. Real-World Analogy: Biological Genetics & Vehicle Classification
  2. Single, Multilevel, and Hierarchical Inheritance
  3. Method Overriding: Modifying Parent Behavior in Children
  4. Demystifying 'super()': How It Connects to Parent Classes
  5. Multiple Inheritance & The Infamous "Diamond Problem"
  6. Method Resolution Order (MRO) & C3 Linearization
  7. Mixins: Composable, Reusable Features without Deep Hierarchies
  8. Type Checking: isinstance() vs issubclass() vs type()
  9. Common Beginner Pitfall: Forgetting super().__init__()
 10. Runnable Hands-on Demonstration
================================================================================
"""

import json


# ==============================================================================
# 1. REAL-WORLD ANALOGY: WHAT IS INHERITANCE?
# ==============================================================================
"""
Think of Genetics & Vehicle Classification:
  - Every Car has an engine, wheels, and a steering wheel.
  - An ElectricCar is STILL a Car! It has wheels, doors, and steering, but it also
    has a battery and charging port.
  - Instead of rewriting wheel, door, and steering logic from scratch for ElectricCar,
    ElectricCar INHERITS from Car!

TERMINOLOGY:
  - Parent Class (Superclass / Base Class) -> The generalized class (e.g., Vehicle, Animal).
  - Child Class (Subclass / Derived Class) -> The specialized class (e.g., ElectricCar, Dog).

BENEFIT:
  - DRY Principle (Don't Repeat Yourself). Write once, inherit everywhere.
"""


# ==============================================================================
# 2, 3, 4. SINGLE & MULTILEVEL INHERITANCE, METHOD OVERRIDING, AND super()
# ==============================================================================

# Base Class (Parent)
class Vehicle:
    """Base class representing any motorized vehicle."""

    def __init__(self, brand: str, model: str, year: int):
        self.brand: str = brand
        self.model: str = model
        self.year: int = year
        self.speed: int = 0

    def start_engine(self) -> str:
        return f"{self.brand} {self.model}: Engine started. Ready to roll."

    def accelerate(self, amount: int) -> None:
        self.speed += amount
        print(f"Accelerating to {self.speed} km/h.")

    def get_info(self) -> str:
        return f"{self.year} {self.brand} {self.model}"


# Child Class 1: Single Inheritance (Car inherits from Vehicle)
class Car(Vehicle):
    """
    Subclass that extends Vehicle by adding number of doors and trunk space.
    """

    def __init__(self, brand: str, model: str, year: int, doors: int = 4):
        # super() calls the parent class's __init__ method!
        # This initializes brand, model, and year without duplicating code.
        super().__init__(brand=brand, model=model, year=year)
        self.doors: int = doors

    # METHOD OVERRIDING: Modifying parent's get_info behavior
    def get_info(self) -> str:
        base_info = super().get_info()  # Call parent's get_info
        return f"{base_info} ({self.doors}-door Sedan)"


# Child Class 2: Multilevel Inheritance (ElectricCar inherits from Car -> Vehicle)
class ElectricCar(Car):
    """
    Multilevel inheritance:
    Vehicle ──► Car ──► ElectricCar
    """

    def __init__(self, brand: str, model: str, year: int, battery_kwh: int):
        super().__init__(brand=brand, model=model, year=year, doors=4)
        self.battery_kwh: int = battery_kwh
        self.battery_level: int = 100

    # METHOD OVERRIDING: Completely replacing start_engine
    def start_engine(self) -> str:
        return f"{self.brand} {self.model}: Silent EV startup. [Battery: {self.battery_level}%]"

    def charge(self) -> str:
        self.battery_level = 100
        return f"{self.brand} {self.model}: Fully charged to 100%!"


# ==============================================================================
# 5 & 6. MULTIPLE INHERITANCE, THE DIAMOND PROBLEM & MRO
# ==============================================================================
"""
THE DIAMOND PROBLEM:
What happens if Class D inherits from both B and C, and both B and C inherit from A?
If both B and C override a method from A, which one does D call?

          ┌─────────┐
          │    A    │
          └────┬────┘
           ┌───┴───┐
           ▼       ▼
        ┌─────┐ ┌─────┐
        │  B  │ │  C  │
        └──┬──┘ └──┬──┘
           └───┬───┘
               ▼
            ┌─────┐
            │  D  │
            └─────┘

PYTHON'S SOLUTION: C3 Linearization (Method Resolution Order - MRO).
Python follows a strict, deterministic search order from left to right, depth-first
without visiting the same class twice before its subclasses.
You can view any class's MRO using `Class.mro()`!
"""

class A:
    def greet(self) -> str:
        return "Greeting from A"

class B(A):
    def greet(self) -> str:
        return "Greeting from B"

class C(A):
    def greet(self) -> str:
        return "Greeting from C"

# D inherits from B first, then C: D(B, C)
class D(B, C):
    pass


# ==============================================================================
# 7. MIXIN CLASSES (Modular, Plug-and-Play Reusability)
# ==============================================================================
"""
A MIXIN is a lightweight class designed to add a SPECIFIC feature to other classes,
rather than representing a full "Is-A" relationship.
Rules for Mixins:
  - Do not have state (__init__).
  - Provide helper methods that work on any class having specific attributes.
"""

class JSONExportMixin:
    """Provides a to_json() method to any class that inherits it."""

    def to_json(self) -> str:
        # Serializes the instance's __dict__ to a JSON string
        return json.dumps(self.__dict__, indent=2)


class SmartDevice:
    def __init__(self, device_name: str, ip_address: str):
        self.device_name: str = device_name
        self.ip_address: str = ip_address


# Smartphone inherits core device behavior AND the JSON export capability!
class Smartphone(SmartDevice, JSONExportMixin):
    def __init__(self, device_name: str, ip_address: str, os: str):
        super().__init__(device_name, ip_address)
        self.os: str = os


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 03: INHERITANCE & CODE REUSE DEMONSTRATION")
    print("=" * 70)

    # 1. Single Inheritance
    print("\n--- 1. Single Inheritance (Car -> Vehicle) ---")
    my_car = Car(brand="Toyota", model="Camry", year=2024, doors=4)
    print(my_car.start_engine())
    print(my_car.get_info())

    # 2. Multilevel Inheritance & Overriding
    print("\n--- 2. Multilevel Inheritance (ElectricCar -> Car -> Vehicle) ---")
    my_ev = ElectricCar(brand="Tesla", model="Model 3", year=2025, battery_kwh=75)
    print(my_ev.start_engine())  # Overridden silent startup
    print(my_ev.get_info())      # Inherited from Car
    print(my_ev.charge())        # Unique EV capability

    # 3. Resolving the Diamond Problem via MRO
    print("\n--- 3. Multiple Inheritance & Method Resolution Order (MRO) ---")
    d_obj = D()
    print(f"Calling d_obj.greet(): '{d_obj.greet()}' (Notice B wins because it was listed first!)")

    print("\nMethod Resolution Order (MRO) for Class D:")
    for index, cls in enumerate(D.mro(), start=1):
        print(f"  Step {index}: {cls.__name__}")

    # 4. Using Mixins for Clean Composition
    print("\n--- 4. Mixin Classes (JSONExportMixin) ---")
    phone = Smartphone(device_name="Pixel 9", ip_address="192.168.1.50", os="Android 15")
    print("Exporting Smartphone object directly to JSON via Mixin:")
    print(phone.to_json())

    # 5. Type Checking: isinstance vs issubclass vs type
    print("\n--- 5. Type Checking in Hierarchies ---")
    print(f"Is my_ev an instance of ElectricCar? {isinstance(my_ev, ElectricCar)}")
    print(f"Is my_ev an instance of Car?         {isinstance(my_ev, Car)}")
    print(f"Is my_ev an instance of Vehicle?     {isinstance(my_ev, Vehicle)}")
    print(f"Is ElectricCar a subclass of Vehicle? {issubclass(ElectricCar, Vehicle)}")
    print(f"Is type(my_ev) == Car?               {type(my_ev) == Car} (Strict type check)")

    print("\n" + "=" * 70)
    print("      MODULE 03 COMPLETE: INHERITANCE MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

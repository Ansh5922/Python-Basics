"""
================================================================================
 MODULE 01: CORE BASICS & ANATOMY OF OOP
================================================================================

Welcome to Object-Oriented Programming (OOP) in Python!
This module is designed for beginners to build an intuitive, crystal-clear
foundation of what OOP is, why we use it, and how Python handles objects in memory.

Table of Contents:
  1. Real-World Analogy: What is a Class vs an Object?
  2. Creating Your First Class and Object
  3. Demystifying 'self': What is it really?
  4. The '__init__' Constructor Method
  5. Instance Attributes vs Class Attributes (Memory Model)
  6. The Three Types of Methods: Instance, Class (@classmethod), and Static (@staticmethod)
  7. Common Beginner Pitfalls & Gotchas
  8. Runnable Hands-on Demonstration
================================================================================
"""

import sys


# ==============================================================================
# 1. REAL-WORLD ANALOGY: CLASS VS OBJECT
# ==============================================================================
"""
Think of a CLASS as a Blueprint or Cookie Cutter:
  - An architectural blueprint is NOT a house. You cannot live inside a blueprint!
    It just defines: "Houses built from this will have 3 bedrooms, 2 doors, and a roof."
  - An OBJECT (or Instance) is the actual physical house built from that blueprint.
    You can build 100 different houses from 1 blueprint. Each house has its own
    paint color, address, and occupants, but all share the blueprint's structure!

        CLASS (Blueprint)               OBJECTS (Instances in Memory)
    ┌─────────────────────────┐         ┌─────────────────────────┐
    │  class Car:             │  ───►   │  car1 = Car("Red")      │ (Address: 0x101)
    │     color: str          │         ├─────────────────────────┤
    │     speed: int          │  ───►   │  car2 = Car("Blue")     │ (Address: 0x102)
    │     def drive(): ...    │         └─────────────────────────┘
    └─────────────────────────┘
"""


# ==============================================================================
# 2 & 3 & 4. WRITING A CLASS, 'self', AND '__init__'
# ==============================================================================
class Dog:
    """
    A simple class representing a pet dog.
    """

    # --------------------------------------------------------------------------
    # CLASS ATTRIBUTE (Shared by ALL dogs)
    # Stored once in the class namespace, not duplicated per dog.
    # --------------------------------------------------------------------------
    species: str = "Canis lupus familiaris"  # Every dog belongs to this species
    total_dogs_created: int = 0             # Counter tracking all dogs created

    # --------------------------------------------------------------------------
    # CONSTRUCTOR: __init__
    # Runs AUTOMATICALLY whenever a new Dog object is created: Dog("Buddy", 3)
    # --------------------------------------------------------------------------
    def __init__(self, name: str, breed: str, age: int):
        """
        'self' refers to the SPECIFIC INSTANCE currently being created.
        When you do d1 = Dog("Buddy", ...), Python turns it into:
            Dog.__init__(d1, "Buddy", ...)
        """
        # INSTANCE ATTRIBUTES (Unique to THIS specific dog)
        self.name: str = name
        self.breed: str = breed
        self.age: int = age

        # Track the total count using the class variable
        Dog.total_dogs_created += 1

    # --------------------------------------------------------------------------
    # 1. INSTANCE METHOD
    # Takes 'self' as the first parameter. Can read and modify instance attributes.
    # --------------------------------------------------------------------------
    def bark(self, times: int = 1) -> str:
        """Instance method: Knows who 'self' is and uses its name."""
        sound = "Woof! " * times
        return f"{self.name} says: {sound.strip()}"

    def have_birthday(self) -> None:
        """Mutates this specific dog's age."""
        self.age += 1
        print(f"[HAPPY BIRTHDAY] {self.name}! You are now {self.age} years old.")

    # --------------------------------------------------------------------------
    # 2. CLASS METHOD (@classmethod)
    # Takes 'cls' (the class itself) instead of 'self'.
    # Used when logic affects the ENTIRE class, or for Alternative Constructors!
    # --------------------------------------------------------------------------
    @classmethod
    def get_total_population(cls) -> str:
        """Reads class-level state."""
        return f"Total registered dogs: {cls.total_dogs_created}"

    @classmethod
    def from_hyphen_string(cls, dog_string: str) -> "Dog":
        """
        Alternative Constructor!
        Allows creating a Dog from a formatted string like: "Rocky-Bulldog-4"
        """
        name, breed, age_str = dog_string.split("-")
        return cls(name=name, breed=breed, age=int(age_str))

    # --------------------------------------------------------------------------
    # 3. STATIC METHOD (@staticmethod)
    # Takes NEITHER 'self' NOR 'cls'.
    # A standalone utility function placed inside the class namespace for logical grouping.
    # --------------------------------------------------------------------------
    @staticmethod
    def human_to_dog_years(human_years: int) -> int:
        """
        General rule of thumb: 1 human year ≈ 7 dog years.
        Notice: Doesn't need access to any specific dog's attributes!
        """
        return human_years * 7


# ==============================================================================
# 5. INSTANCE ATTRIBUTES VS CLASS ATTRIBUTES: THE MEMORY GOTCHA
# ==============================================================================
"""
IMPORTANT BEGINNER PITFALL:
Class attributes are shared across ALL instances. If you modify a MUTABLE class
attribute (like a list) from one instance, it affects EVERY OTHER INSTANCE!

WRONG WAY:
  class Student:
      courses = []  # <--- Shared list! If student1 appends, student2 sees it!

CORRECT WAY:
  class Student:
      def __init__(self):
          self.courses = []  # <--- Unique list per student created inside __init__
"""


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 01: CORE BASICS & ANATOMY OF OOP DEMONSTRATION")
    print("=" * 70)

    # 1. Instantiating Objects
    print("\n--- 1. Creating Instances (Objects) ---")
    dog1 = Dog(name="Buddy", breed="Golden Retriever", age=3)
    dog2 = Dog(name="Luna", breed="Husky", age=2)

    print(f"Dog 1: Name = {dog1.name}, Breed = {dog1.breed}, Age = {dog1.age}")
    print(f"Dog 2: Name = {dog2.name}, Breed = {dog2.breed}, Age = {dog2.age}")

    # 2. Inspecting Memory IDs (Proving they are separate objects in RAM)
    print("\n--- 2. Memory Inspection (id) ---")
    print(f"Memory Address of dog1: {hex(id(dog1))}")
    print(f"Memory Address of dog2: {hex(id(dog2))}")
    print(f"Are dog1 and dog2 the exact same object? {dog1 is dog2}")

    # 3. Calling Instance Methods
    print("\n--- 3. Calling Instance Methods ---")
    print(dog1.bark(2))
    print(dog2.bark(1))
    dog1.have_birthday()

    # 4. Class Attribute vs Instance Attribute
    print("\n--- 4. Class Attributes vs Instance Attributes ---")
    print(f"dog1 species: {dog1.species}")
    print(f"dog2 species: {dog2.species}")
    print(f"Directly from Dog class: {Dog.species}")

    # 5. Using Class Methods & Alternative Constructor
    print("\n--- 5. Class Method & Alternative Constructor ---")
    print(Dog.get_total_population())

    # Creating a dog using the alternative string constructor
    dog3 = Dog.from_hyphen_string("Rocky-German Shepherd-5")
    print(f"Created via string: {dog3.name}, {dog3.breed}, {dog3.age} years old.")
    print(Dog.get_total_population())

    # 6. Using Static Methods
    print("\n--- 6. Static Methods ---")
    years = Dog.human_to_dog_years(human_years=5)
    print(f"5 human years is roughly equal to {years} dog years.")

    # 7. Looking inside Python's __dict__ (How Python stores attributes)
    print("\n--- 7. Attribute Namespace Inspection (__dict__) ---")
    print("dog1 internal attributes dictionary:")
    print(dog1.__dict__)

    print("\n" + "=" * 70)
    print("      MODULE 01 COMPLETE: FOUNDATIONS MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

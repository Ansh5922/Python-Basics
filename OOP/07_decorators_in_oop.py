"""
================================================================================
 MODULE 07: DECORATORS IN OBJECT-ORIENTED PYTHON
================================================================================

Welcome to DECORATORS IN OOP!
Decorators allow you to modify or extend the behavior of functions, methods,
or entire classes WITHOUT altering their internal source code.

Table of Contents:
  1. Real-World Analogy: Gift Wrapping
  2. Prerequisites: First-Class Functions and Closures
  3. Anatomy of a Decorator: What does '@' really mean?
  4. Preserving Function Identity with @functools.wraps
  5. Decorating Class Methods: Handling the 'self' Parameter
  6. Class-Based Decorators (Using __call__ for Stateful Decorators)
  7. Class Decorators (Modifying an Entire Class at Runtime)
  8. Built-in OOP Decorators: @cached_property and @dataclass
  9. Common Beginner Pitfall: Forgetting *args and **kwargs in Wrappers
 10. Runnable Hands-on Demonstration
================================================================================
"""

import time
from functools import wraps, cached_property
from dataclasses import dataclass


# ==============================================================================
# 1. REAL-WORLD ANALOGY: WHAT IS A DECORATOR?
# ==============================================================================
"""
Think of Gift Wrapping:
  - You buy a gift (e.g., a wristwatch).
  - You wrap it in shiny decorative paper and add a ribbon.
  - The watch inside hasn't changed at all! It still tells time.
  - But now it has extra presentation, protection, and flare around it!

IN PROGRAMMING:
  - A decorator is a function that takes another function (or method/class)
    as input, wraps extra behavior around it (e.g., logging, timing, security checks),
    and returns the enhanced wrapper!
"""


# ==============================================================================
# 2, 3, 4. ANATOMY OF A DECORATOR & @wraps
# ==============================================================================
def execution_timer(func):
    """
    Measures and logs how long a function or method takes to execute.
    """
    # @wraps preserves the original function's name and __doc__ docstring!
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        # Call the original function
        result = func(*args, **kwargs)
        
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        print(f"[PERFORMANCE] '{func.__name__}' executed in {duration_ms:.4f} ms.")
        return result

    return wrapper


# ==============================================================================
# 5. DECORATING CLASS METHODS (Handling 'self')
# ==============================================================================
"""
KEY RULE FOR METHOD DECORATORS:
Methods always receive `self` as their first positional argument!
Therefore, your wrapper MUST accept `*args, **kwargs` so that `self`
is safely passed through to the original method:
    wrapper(self, *args, **kwargs)
"""

def require_role(allowed_role: str):
    """
    Decorator Factory (Takes arguments)!
    Allows restricting access to specific methods based on user role.
    """
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # Inspect the instance's role attribute
            user_role = getattr(self, "role", "Guest")
            if user_role != allowed_role:
                raise PermissionError(
                    f"[ACCESS DENIED] User '{self.username}' with role '{user_role}' "
                    f"cannot perform '{method.__name__}'. Required: '{allowed_role}'."
                )
            return method(self, *args, **kwargs)
        return wrapper
    return decorator


class UserSession:
    def __init__(self, username: str, role: str):
        self.username: str = username
        self.role: str = role

    @execution_timer
    def view_dashboard(self) -> str:
        return f"[DASHBOARD] Welcome {self.username} ({self.role})!"

    @require_role("Admin")
    def delete_database(self) -> str:
        return f"[DANGER ZONE] Database deleted by Admin '{self.username}'."


# ==============================================================================
# 6. CLASS-BASED DECORATORS (Stateful Decorators)
# ==============================================================================
class CallCounter:
    """
    A class used as a decorator to count how many times a function is called.
    Stores persistent state across multiple calls.
    """

    def __init__(self, func):
        self.func = func
        self.call_count = 0
        wraps(func)(self)  # Preserve metadata

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(f"[AUDIT] Function '{self.func.__name__}' has been called {self.call_count} times.")
        return self.func(*args, **kwargs)


@CallCounter
def process_invoice(invoice_id: int):
    return f"Invoice #{invoice_id} processed."


# ==============================================================================
# 7. CLASS DECORATORS (Modifying an Entire Class)
# ==============================================================================
def add_id_tag(cls):
    """
    A class decorator that injects a unique ID generator into any class.
    """
    cls.system_version = "v2.5.0"
    return cls


@add_id_tag
class PatientRecord:
    def __init__(self, patient_name: str):
        self.patient_name = patient_name


# ==============================================================================
# 8. BUILT-IN OOP DECORATORS: @cached_property AND @dataclass
# ==============================================================================
class AnalyticsReport:
    def __init__(self, raw_numbers: list[int]):
        self.raw_numbers = raw_numbers

    # @cached_property: Runs expensive computation ONCE and caches the result
    # on the instance. Subsequent reads read directly from memory cache!
    @cached_property
    def heavy_calculation(self) -> int:
        print("  [CALCULATION ENGINE] Running heavy number-crunching...")
        return sum(x ** 2 for x in self.raw_numbers)


# MODERN PYTHON: @dataclass
# Automatically writes __init__, __repr__, and __eq__ for you!
@dataclass
class Product:
    name: str
    price: float
    stock: int = 0

    def in_stock(self) -> bool:
        return self.stock > 0


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 07: DECORATORS IN OBJECT-ORIENTED PYTHON DEMO")
    print("=" * 70)

    # 1. Method Decorator with Performance Timing
    print("\n--- 1. Method Timing Decorator ---")
    admin = UserSession(username="Sarah", role="Admin")
    guest = UserSession(username="John", role="Guest")

    print(admin.view_dashboard())

    # 2. Role-Based Access Control Decorator
    print("\n--- 2. Role-Based Security Decorator ---")
    print(admin.delete_database())

    try:
        guest.delete_database()
    except PermissionError as err:
        print(f"Caught expected security violation:\n  {err}")

    # 3. Class-Based Stateful Decorator
    print("\n--- 3. Class-Based Decorator (CallCounter) ---")
    print(process_invoice(101))
    print(process_invoice(102))
    print(process_invoice(103))

    # 4. Class Decorator
    print("\n--- 4. Class Decorator ---")
    patient = PatientRecord("Aman")
    print(f"Patient Name: {patient.patient_name}")
    print(f"Injected class attribute: system_version = {patient.system_version}")

    # 5. @cached_property Demonstration
    print("\n--- 5. Built-in @cached_property ---")
    report = AnalyticsReport(raw_numbers=list(range(1000)))
    print("First access (computes value):")
    print(f"Result: {report.heavy_calculation}")
    print("Second access (cached instantly, no computation logged):")
    print(f"Result: {report.heavy_calculation}")

    # 6. Modern @dataclass Demonstration
    print("\n--- 6. Modern Python @dataclass ---")
    laptop = Product(name="MacBook Pro", price=1999.99, stock=5)
    print(f"Automatic __repr__: {laptop}")
    print(f"In stock? {laptop.in_stock()}")

    print("\n" + "=" * 70)
    print("      MODULE 07 COMPLETE: DECORATORS MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

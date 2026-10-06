"""
================================================================================
 MODULE 04: POLYMORPHISM & DUCK TYPING
================================================================================

Welcome to the 3rd Classical Pillar of Object-Oriented Programming: POLYMORPHISM!

Table of Contents:
  1. Real-World Analogy: The Universal USB Port
  2. What is Polymorphism? ("Many Forms")
  3. Python's Signature Superpower: Duck Typing
  4. Method Overriding (Polymorphism through Inheritance)
  5. The Method Overloading Dilemma in Python:
     - Why traditional C++/Java overloading doesn't exist in Python
     - Alternative 1: Default & Variable Arguments (*args, **kwargs)
     - Alternative 2: functools.singledispatch
     - Alternative 3: typing.overload for Type Hinting
  6. Operator Overloading Preview (Polymorphism with Symbols)
  7. Common Beginner Pitfall: Defining Methods with the Same Name
  8. Runnable Hands-on Demonstration
================================================================================
"""

from functools import singledispatch
from typing import Union, overload


# ==============================================================================
# 1. REAL-WORLD ANALOGY: WHAT IS POLYMORPHISM?
# ==============================================================================
"""
Think of a USB-C Port:
  - Your laptop has a single USB-C port.
  - You can plug in:
      * A Flash Drive (to transfer files)
      * A Smartphone (to charge)
      * An External Monitor (to display video)
      * A Mouse (to navigate)
  - The laptop doesn't care WHAT specific device it is. As long as the device
    has a USB-C connector, the laptop sends and receives data through that same port!

IN PROGRAMMING:
  - Polymorphism means "Different classes can be treated through the SAME unified interface."
  - One function call (e.g., `device.connect()`) behaves appropriately depending
    on which object is passed!
"""


# ==============================================================================
# 2 & 3. DUCK TYPING: PYTHON'S SUPERPOWER
# ==============================================================================
"""
"If it walks like a duck and quacks like a duck, it's a duck."

In languages like Java or C++, two objects MUST inherit from the same parent or interface
to be treated polymorphically.

IN PYTHON: Inheritance is NOT required!
If an object implements the expected method, Python happily runs it.
This is called DUCK TYPING (Dynamic Polymorphism).
"""

class CreditCardPayment:
    def process_payment(self, amount: float) -> str:
        return f"[CREDIT CARD] Successfully charged ${amount:.2f} via Visa/MasterCard."


class PayPalPayment:
    def process_payment(self, amount: float) -> str:
        return f"[PAYPAL] Successfully routed ${amount:.2f} via PayPal Secure Gateway."


class CryptoPayment:
    def process_payment(self, amount: float) -> str:
        return f"[CRYPTO] Successfully transferred ${amount:.2f} worth of Bitcoin."


# Unified polymorphic function (Doesn't care which class it is!)
def checkout(payment_method, amount: float) -> None:
    """
    Duck Typing in action:
    As long as `payment_method` has a `.process_payment()` method, this function works!
    """
    result = payment_method.process_payment(amount)
    print(result)


# ==============================================================================
# 4. METHOD OVERRIDING (INHERITANCE-BASED POLYMORPHISM)
# ==============================================================================
class Shape:
    """Base class defining a contract."""
    def area(self) -> float:
        raise NotImplementedError("Subclasses must implement area()")


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width: float = width
        self.height: float = height

    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius: float = radius

    def area(self) -> float:
        return 3.14159 * (self.radius ** 2)


# ==============================================================================
# 5. METHOD OVERLOADING IN PYTHON: HOW TO DO IT RIGHT
# ==============================================================================
"""
THE GOTCHA:
In Java or C++, you can write:
    void add(int a, int b) { ... }
    void add(int a, int b, int c) { ... }

IN PYTHON: You CANNOT do this!
Because functions are first-class objects, the second definition simply OVERWRITES the first!

HOW PYTHON HANDLES OVERLOADING:
"""

# Pattern A: Using Default Arguments (Most common & beginner-friendly)
class Calculator:
    def add(self, a: int, b: int, c: int = 0) -> int:
        """Handles adding 2 OR 3 numbers seamlessly."""
        return a + b + c


# Pattern B: Using functools.singledispatch (Type-based dispatching)
@singledispatch
def format_data(value):
    """Fallback handler for unsupported types."""
    return f"[GENERIC] String representation: {str(value)}"

@format_data.register(int)
def _(value: int):
    return f"[INTEGER] Number: {value:,} (Hex: {hex(value)})"

@format_data.register(list)
def _(value: list):
    return f"[LIST] Total items: {len(value)} -> Contents: {', '.join(map(str, value))}"


# Pattern C: Using @typing.overload (For IDE & static type checkers)
@overload
def double(x: int) -> int: ...

@overload
def double(x: str) -> str: ...

def double(x: Union[int, str]) -> Union[int, str]:
    """Single implementation that handles both int and str."""
    return x * 2


# ==============================================================================
# 6. OPERATOR OVERLOADING PREVIEW
# ==============================================================================
"""
In Python, even operators (+, *, ==) are polymorphic!
  - 5 + 10       -> 15 (Integer addition)
  - "Hello " + "World" -> "Hello World" (String concatenation)
  - [1, 2] + [3, 4]    -> [1, 2, 3, 4] (List merging)
Behind the scenes, '+' calls the `__add__` dunder method on the left operand!
(We will cover this deeply in Module 06).
"""


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 04: POLYMORPHISM & DUCK TYPING DEMONSTRATION")
    print("=" * 70)

    # 1. Duck Typing in Action
    print("\n--- 1. Duck Typing (Different classes, same interface) ---")
    cart_total = 149.99

    card = CreditCardPayment()
    paypal = PayPalPayment()
    crypto = CryptoPayment()

    # Pass completely unrelated objects to the same checkout function!
    checkout(card, cart_total)
    checkout(paypal, cart_total)
    checkout(crypto, cart_total)

    # 2. Polymorphic Shapes Collection
    print("\n--- 2. Polymorphic Collections (Iterating over different subclasses) ---")
    shapes = [
        Rectangle(width=10, height=5),
        Circle(radius=7),
        Rectangle(width=3, height=8)
    ]

    for s in shapes:
        print(f"Shape: {s.__class__.__name__:<10} | Area: {s.area():.2f}")

    # 3. Method Overloading via Default Arguments
    print("\n--- 3. Method Overloading via Default Arguments ---")
    calc = Calculator()
    print(f"Adding 2 numbers (10, 20):     {calc.add(10, 20)}")
    print(f"Adding 3 numbers (10, 20, 30): {calc.add(10, 20, 30)}")

    # 4. Method Overloading via functools.singledispatch
    print("\n--- 4. Type-Based Polymorphism (singledispatch) ---")
    print(format_data(1000000))
    print(format_data(["Python", "FastAPI", "PostgreSQL"]))
    print(format_data(3.14159))  # Falls back to generic handler

    # 5. Overloaded Double Function
    print("\n--- 5. Function Overloading Behavior ---")
    print(f"double(5):       {double(5)}")
    print(f"double('Echo '): {double('Echo ')}")

    print("\n" + "=" * 70)
    print("      MODULE 04 COMPLETE: POLYMORPHISM MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

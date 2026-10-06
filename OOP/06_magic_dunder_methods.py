"""
================================================================================
 MODULE 06: MAGIC (DUNDER) METHODS & CUSTOMIZATION
================================================================================

Welcome to the Python Data Model: MAGIC (DUNDER) METHODS!
"Dunder" stands for "Double Underscore" (__init__, __str__, etc.).

Table of Contents:
  1. Real-World Analogy: Why Does Python Feel Like Magic?
  2. String Representation: __str__ vs __repr__
  3. Arithmetic Operator Overloading: __add__, __sub__, __mul__
  4. Comparison Protocols & @functools.total_ordering: __eq__, __lt__
  5. Container & Collection Protocol: __len__, __getitem__, __contains__, __iter__
  6. Context Manager Protocol: __enter__ and __exit__ (The 'with' statement)
  7. Callable Objects: __call__ (Making instances callable like functions)
  8. Common Beginner Pitfall: Mutating Operands in __add__
  9. Runnable Hands-on Demonstration
================================================================================
"""

from functools import total_ordering


# ==============================================================================
# 1. REAL-WORLD ANALOGY: WHAT ARE DUNDER METHODS?
# ==============================================================================
"""
Have you ever wondered:
  - Why does `len([1, 2, 3])` give 3? Because the list implements `__len__()`!
  - Why does `3 + 5` work? Because 3 implements `__add__(5)`!
  - Why does `print(user)` show `<__main__.User object at 0x...>` unless customized?
    Because by default, Python falls back to generic object representation!

DUNDER METHODS are Python's built-in hooks that allow YOUR custom classes to
integrate seamlessly with Python's native operators, syntax, and functions.
"""


# ==============================================================================
# 2, 3, 4. STR/REPR, ARITHMETIC OPERATORS, AND COMPARISONS
# ==============================================================================
@total_ordering  # Automatically generates <=, >, >= if __eq__ and __lt__ are defined!
class Currency:
    """
    A custom Money/Currency class supporting addition, subtraction,
    comparisons, and formatted string representations.
    """

    def __init__(self, amount: float, currency_code: str = "USD"):
        self.amount: float = round(float(amount), 2)
        self.currency_code: str = currency_code.upper()

    # --------------------------------------------------------------------------
    # 1. __str__: Human-readable string (Used by print() and str())
    # --------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency_code}"

    # --------------------------------------------------------------------------
    # 2. __repr__: Unambiguous developer string (Shows how to recreate the object)
    # --------------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"Currency(amount={self.amount}, currency_code='{self.currency_code}')"

    # --------------------------------------------------------------------------
    # 3. __add__: Overloading the '+' operator
    # Rule: Always return a NEW instance! Never mutate the existing object!
    # --------------------------------------------------------------------------
    def __add__(self, other: "Currency") -> "Currency":
        if not isinstance(other, Currency):
            raise TypeError(f"Cannot add Currency to non-Currency type '{type(other).__name__}'")
        if self.currency_code != other.currency_code:
            raise ValueError(f"Cannot add different currencies: {self.currency_code} and {other.currency_code}")
        
        return Currency(amount=self.amount + other.amount, currency_code=self.currency_code)

    # --------------------------------------------------------------------------
    # 4. __sub__: Overloading the '-' operator
    # --------------------------------------------------------------------------
    def __sub__(self, other: "Currency") -> "Currency":
        if not isinstance(other, Currency) or self.currency_code != other.currency_code:
            raise ValueError("Currencies must match for subtraction.")
        return Currency(amount=self.amount - other.amount, currency_code=self.currency_code)

    # --------------------------------------------------------------------------
    # 5. __eq__: Overloading the '==' equality operator
    # --------------------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Currency):
            return False
        return self.amount == other.amount and self.currency_code == other.currency_code

    # --------------------------------------------------------------------------
    # 6. __lt__: Overloading the '<' less-than operator
    # --------------------------------------------------------------------------
    def __lt__(self, other: "Currency") -> bool:
        if not isinstance(other, Currency) or self.currency_code != other.currency_code:
            raise ValueError("Currencies must match for comparison.")
        return self.amount < other.amount


# ==============================================================================
# 5. CONTAINER PROTOCOL: MAKING AN OBJECT BEHAVE LIKE A LIST/DICT
# ==============================================================================
class HospitalWard:
    """
    A custom collection representing patients in a hospital room.
    By implementing container dunders, users can use len(), [index], in, and for-loops!
    """

    def __init__(self, ward_name: str):
        self.ward_name: str = ward_name
        self._patients: list[str] = []

    def admit_patient(self, name: str) -> None:
        self._patients.append(name)

    # Allows len(ward)
    def __len__(self) -> int:
        return len(self._patients)

    # Allows indexing: ward[0], ward[1]
    def __getitem__(self, index: int) -> str:
        return self._patients[index]

    # Allows 'in' keyword: if "Aman" in ward:
    def __contains__(self, name: str) -> bool:
        return name in self._patients


# ==============================================================================
# 6. CONTEXT MANAGER PROTOCOL: __enter__ AND __exit__
# ==============================================================================
"""
Ever used `with open("file.txt") as f:`?
That syntax is powered by the Context Manager Protocol!
  - `__enter__`: Runs setup (open file, acquire lock, start transaction).
  - `__exit__`: GUARANTEED to run teardown (close file, release lock, rollback),
    even if an exception occurred!
"""

class DatabaseTransaction:
    """Simulates an ACID database transaction manager."""

    def __init__(self, session_name: str):
        self.session_name: str = session_name

    def __enter__(self):
        print(f"[TRANSACTION BEGIN] Starting transaction for '{self.session_name}'.")
        return self  # The object returned as the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"[TRANSACTION ROLLBACK] Error occurred ({exc_val})! Rolling back changes.")
            # Return False to re-raise the exception after cleanup
            return False
        print(f"[TRANSACTION COMMIT] Successfully committed transaction for '{self.session_name}'.")
        return True


# ==============================================================================
# 7. CALLABLE OBJECTS: __call__
# ==============================================================================
class Multiplier:
    """
    An object that acts like a function!
    When you define __call__, you can execute `instance(args)`.
    """

    def __init__(self, factor: int):
        self.factor: int = factor

    def __call__(self, number: int) -> int:
        return number * self.factor


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 06: MAGIC (DUNDER) METHODS DEMONSTRATION")
    print("=" * 70)

    # 1. __str__ and __repr__
    print("\n--- 1. String Representation (__str__ vs __repr__) ---")
    wallet = Currency(amount=50.75, currency_code="USD")
    bonus = Currency(amount=25.25, currency_code="USD")

    print(f"print() uses __str__: {wallet}")
    print(f"repr() uses __repr__: {repr(wallet)}")

    # 2. Arithmetic Operator Overloading (+ and -)
    print("\n--- 2. Arithmetic Overloading (__add__ and __sub__) ---")
    total = wallet + bonus
    print(f"{wallet} + {bonus} = {total}")
    remaining = total - Currency(15.0, "USD")
    print(f"{total} - 15.00 USD = {remaining}")

    # 3. Rich Comparisons (<, <=, ==, >, >=)
    print("\n--- 3. Comparison Overloading (__eq__, __lt__, total_ordering) ---")
    c1 = Currency(100, "USD")
    c2 = Currency(150, "USD")
    c3 = Currency(100, "USD")

    print(f"c1 == c3: {c1 == c3}")
    print(f"c1 < c2:  {c1 < c2}")
    print(f"c2 >= c1: {c2 >= c1} (Auto-generated by @total_ordering!)")

    # 4. Container Protocol in Action
    print("\n--- 4. Container Protocol (__len__, __getitem__, __contains__) ---")
    icu = HospitalWard(ward_name="ICU")
    icu.admit_patient("Aman")
    icu.admit_patient("Priya")
    icu.admit_patient("Rohan")

    print(f"Total admitted patients via len(icu): {len(icu)}")
    print(f"Patient at index 0 via icu[0]:         {icu[0]}")
    print(f"Is 'Priya' in icu?                    {'Priya' in icu}")
    print(f"Is 'Karan' in icu?                    {'Karan' in icu}")

    print("\nIterating over custom HospitalWard with for-loop:")
    for patient in icu:
        print(f"  - {patient}")

    # 5. Context Manager Protocol (__enter__ and __exit__)
    print("\n--- 5. Context Manager Protocol (with statement) ---")
    with DatabaseTransaction(session_name="UpdatePatientRecords") as tx:
        print("  [WORK] Executing SQL queries inside secure transaction...")

    # 6. Callable Objects (__call__)
    print("\n--- 6. Callable Objects (__call__) ---")
    triple = Multiplier(factor=3)
    print(f"triple(10) -> {triple(10)}")
    print(f"Is triple callable? {callable(triple)}")

    print("\n" + "=" * 70)
    print("      MODULE 06 COMPLETE: DUNDER METHODS MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

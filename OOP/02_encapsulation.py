"""
================================================================================
 MODULE 02: ENCAPSULATION & DATA PROTECTION
================================================================================

Welcome to the 1st Classical Pillar of Object-Oriented Programming: ENCAPSULATION!

Table of Contents:
  1. Real-World Analogy: The Bank ATM & Medicine Capsule
  2. Public, Protected (_), and Private (__) Attributes
  3. Under the Hood: Name Mangling in Python
  4. The Pythonic Way: Getters and Setters with @property
  5. Defensive Programming: Validation inside Setters
  6. Read-Only Properties (Immutable Attributes)
  7. Attribute Deletion with @deleter
  8. Common Beginner Pitfall: Java-Style Getters/Setters vs @property
  9. Runnable Hands-on Demonstration
================================================================================
"""


# ==============================================================================
# 1. REAL-WORLD ANALOGY: WHAT IS ENCAPSULATION?
# ==============================================================================
"""
Think of a Medicine Capsule:
  - Inside the capsule are powdery medical ingredients.
  - The outer gelatin shell keeps them bundled together and prevents the patient
    from contaminating or spilling the powder directly.

Think of a Bank ATM:
  - You do NOT open the ATM vault and take cash directly with your hands.
    (If users could do `account.balance = 1000000`, the bank would go bankrupt!)
  - Instead, the data (`balance`) is protected. You interact with it ONLY through
    controlled interfaces: deposit(), withdraw(), and authentication (PIN check).

ENCAPSULATION DOES TWO JOINS:
  1. Bundling: Keeps data (attributes) and behavior (methods) together in one place.
  2. Data Hiding & Protection: Restricts direct access to prevent accidental or malicious corruption.
"""


# ==============================================================================
# 2 & 3. PUBLIC, PROTECTED, AND PRIVATE ATTRIBUTES
# ==============================================================================
class BankAccount:
    """
    Demonstrates access levels and Name Mangling in Python.
    """

    def __init__(self, account_holder: str, initial_balance: float, pin: str):
        # 1. PUBLIC ATTRIBUTE
        # Accessible anywhere, inside or outside the class.
        self.account_holder: str = account_holder

        # 2. PROTECTED ATTRIBUTE (Single Underscore: _attr)
        # CONVENTION ONLY: Signals to other developers:
        # "Please treat this as internal/private. Do not modify directly outside subclasses."
        # Python does NOT strictly enforce this at runtime!
        self._account_type: str = "Savings"

        # 3. PRIVATE ATTRIBUTE (Double Underscore: __attr)
        # Python enforces this through NAME MANGLING.
        # It internally renames `__balance` to `_BankAccount__balance`.
        self.__balance: float = initial_balance
        self.__pin: str = pin

    # Public method to view the balance securely
    def get_statement(self, entered_pin: str) -> str:
        if entered_pin != self.__pin:
            return "[SECURITY ERROR] Invalid PIN! Access Denied."
        return f"Account [{self.account_holder}]: Balance = ${self.__balance:.2f}"


# ==============================================================================
# 4, 5, 6, 7. THE PYTHONIC WAY: @property GETTERS, SETTERS & DELETERS
# ==============================================================================
class SmartBankAccount:
    """
    Demonstrates the Pythonic way to control attribute access using @property.
    Allows accessing attributes like normal fields (account.balance) while
    silently running validation functions behind the scenes!
    """

    def __init__(self, owner: str, opening_balance: float = 0.0):
        self.owner: str = owner
        # We store the actual value in a private variable _balance
        self._balance: float = 0.0
        # Call the setter to validate the opening balance
        self.balance = opening_balance

    # --------------------------------------------------------------------------
    # 1. GETTER (@property)
    # Allows reading the value: `current = acc.balance`
    # --------------------------------------------------------------------------
    @property
    def balance(self) -> float:
        """Getter: Called whenever someone reads `account.balance`."""
        return self._balance

    # --------------------------------------------------------------------------
    # 2. SETTER (@<property_name>.setter)
    # Allows writing: `acc.balance = 500`
    # Allows adding VALIDATION RULES without breaking existing code!
    # --------------------------------------------------------------------------
    @balance.setter
    def balance(self, new_amount: float) -> None:
        """Setter: Enforces validation rules before modifying data."""
        if not isinstance(new_amount, (int, float)):
            raise TypeError("[VALIDATION ERROR] Balance must be a number!")
        if new_amount < 0:
            raise ValueError("[VALIDATION ERROR] Balance cannot be negative! Debt not allowed.")
        
        self._balance = float(new_amount)

    # --------------------------------------------------------------------------
    # 3. DELETER (@<property_name>.deleter)
    # Allows handling: `del acc.balance`
    # --------------------------------------------------------------------------
    @balance.deleter
    def balance(self) -> None:
        """Deleter: Called when someone runs `del account.balance`."""
        print("[WARNING] Resetting balance to $0.00 instead of deleting attribute.")
        self._balance = 0.0

    # --------------------------------------------------------------------------
    # 4. READ-ONLY PROPERTY (No setter defined)
    # --------------------------------------------------------------------------
    @property
    def account_tier(self) -> str:
        """
        Dynamically computed read-only attribute!
        You CANNOT do: `acc.account_tier = 'Gold'` (raises AttributeError).
        """
        if self._balance >= 10000:
            return "Platinum Member"
        elif self._balance >= 1000:
            return "Gold Member"
        return "Silver Member"


# ==============================================================================
# 8. COMMON BEGINNER PITFALL: JAVA-STYLE GETTERS/SETTERS VS PYTHON @property
# ==============================================================================
"""
THE WRONG / UN-PYTHONIC WAY (Java Style):
  class User:
      def get_name(self):
          return self.name
      def set_name(self, value):
          self.name = value

  user.set_name("Alice")
  print(user.get_name())

THE PYTHONIC WAY:
  Start with plain attributes:
      user.name = "Alice"
      print(user.name)

  If you later need validation, convert it to a `@property`!
  All existing code (`user.name = ...`) continues to work without changing API syntax!
"""


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 02: ENCAPSULATION & DATA PROTECTION DEMONSTRATION")
    print("=" * 70)

    # 1. Public vs Protected vs Private
    print("\n--- 1. Access Levels (Public, Protected, Private) ---")
    acc = BankAccount(account_holder="Alice", initial_balance=5000.0, pin="1234")

    # Public: Accessible directly
    print(f"Public account holder: {acc.account_holder}")

    # Protected: Accessible, but warning convention says don't touch
    print(f"Protected account type: {acc._account_type} (Convention: internal use)")

    # Private: Direct access fails!
    try:
        print(acc.__balance)
    except AttributeError as e:
        print(f"Caught expected error when accessing __balance directly: {e}")

    # Secure access via authorized method
    print(acc.get_statement(entered_pin="1234"))
    print(acc.get_statement(entered_pin="9999"))

    # 2. How Name Mangling works under the hood
    print("\n--- 2. Inspecting Name Mangling in Python ---")
    print("All attributes in acc object:")
    print(list(acc.__dict__.keys()))
    print("Notice how __balance was renamed to: '_BankAccount__balance'!")
    print(f"Direct bypass via mangled name: ${acc._BankAccount__balance:.2f} (Don't do this in production!)")

    # 3. Pythonic Properties with @property and Validation
    print("\n--- 3. Clean Pythonic Properties (@property) ---")
    smart_acc = SmartBankAccount(owner="Bob", opening_balance=250.0)
    print(f"Owner: {smart_acc.owner}")
    print(f"Initial Balance: ${smart_acc.balance:.2f}")
    print(f"Current Tier: {smart_acc.account_tier}")

    # Updating balance through the setter
    print("\nDeposit $1500 (Updating balance to $1750)...")
    smart_acc.balance = 1750.0
    print(f"New Balance: ${smart_acc.balance:.2f}")
    print(f"New Tier automatically updated: {smart_acc.account_tier}")

    # 4. Testing Validation Protection
    print("\n--- 4. Testing Defensive Validation ---")
    try:
        smart_acc.balance = -500  # Attempting illegal negative balance!
    except ValueError as err:
        print(f"Security check passed! Blocked invalid update: {err}")

    # 5. Testing Read-Only Property
    print("\n--- 5. Testing Read-Only Protection ---")
    try:
        smart_acc.account_tier = "Diamond VIP"  # Illegal modification!
    except AttributeError as err:
        print(f"Security check passed! Cannot overwrite read-only property: {err}")

    # 6. Testing Deleter
    print("\n--- 6. Testing Property Deleter ---")
    del smart_acc.balance
    print(f"Balance after deletion reset: ${smart_acc.balance:.2f}")

    print("\n" + "=" * 70)
    print("      MODULE 02 COMPLETE: ENCAPSULATION MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

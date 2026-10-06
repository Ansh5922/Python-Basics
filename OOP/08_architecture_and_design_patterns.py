"""
================================================================================
 MODULE 08: ARCHITECTURAL CONCEPTS & DESIGN PATTERNS
================================================================================

Welcome to ARCHITECTURAL SYSTEM CONCEPTS & DESIGN PATTERNS!
This is the capstone module where we put all our OOP knowledge together to write
clean, scalable, and maintainable enterprise software.

Table of Contents:
  1. Real-World Analogy: Building a Custom PC (Composition vs Inheritance)
  2. The Golden Rule: "Favor Object Composition over Class Inheritance"
  3. The 5 SOLID Principles Explained for Beginners
  4. Creational Pattern: The Singleton Pattern
  5. Creational Pattern: The Factory Method Pattern
  6. Behavioral Pattern: The Strategy Pattern
  7. Behavioral Pattern: The Observer Pattern (Event Pub/Sub)
  8. Common Beginner Pitfall: Premature Over-Engineering
  9. Runnable Hands-on Demonstration
================================================================================
"""

from abc import ABC, abstractmethod
from typing import List


# ==============================================================================
# 1 & 2. COMPOSITION VS INHERITANCE: THE GOLDEN RULE
# ==============================================================================
"""
THE GOLDEN RULE OF OOP:
"Favor Object Composition over Class Inheritance."

INHERITANCE = "IS-A" Relationship
  - A Dog IS-AN Animal.
  - A Car IS-A Vehicle.

COMPOSITION = "HAS-A" Relationship
  - A Computer IS NOT a CPU.
  - A Computer HAS-A CPU, HAS-A RAM, and HAS-A Storage drive!

WHY COMPOSITION WINS IN REAL-WORLD ARCHITECTURE:
Inheritance creates tight, brittle coupling. If you change the base class, 10 child
classes can unexpectedly break.
With Composition, you build systems from interchangeable lego bricks!
"""

class CPU:
    def __init__(self, model: str, cores: int):
        self.model = model
        self.cores = cores

    def process(self) -> str:
        return f"[CPU: {self.model}] Processing data across {self.cores} cores."


class Memory:
    def __init__(self, gigabytes: int):
        self.gigabytes = gigabytes


class Computer:
    """
    Composition in action:
    Computer is composed of independent, swappable components!
    """
    def __init__(self, cpu: CPU, memory: Memory):
        self.cpu: CPU = cpu
        self.memory: Memory = memory

    def boot_up(self) -> str:
        return f"System Booted with {self.memory.gigabytes}GB RAM.\n  -> {self.cpu.process()}"


# ==============================================================================
# 3. THE 5 SOLID PRINCIPLES EXPLAINED SIMPLY
# ==============================================================================
"""
S - Single Responsibility Principle (SRP):
    A class should have ONE, and only one, reason to change.
    Don't make 'God Objects' that handle database access, HTML rendering, and emailing all in one.

O - Open/Closed Principle (OCP):
    Classes should be OPEN for extension, but CLOSED for modification.
    Add new features by creating new subclasses or plugins, NOT by modifying existing battle-tested code.

L - Liskov Substitution Principle (LSP):
    Subclasses should be substitutable for their base class without altering program correctness.
    (If a function expects a Bird, passing a Penguin shouldn't crash because Penguins can't fly!)

I - Interface Segregation Principle (ISP):
    Clients should not be forced to depend on interfaces they do not use.
    Prefer small, specific interfaces over one massive bloated interface.

D - Dependency Inversion Principle (DIP):
    High-level modules should not depend on low-level modules; both should depend on ABSTRACTIONS.
"""


# ==============================================================================
# 4. CREATIONAL PATTERN: THE SINGLETON PATTERN
# ==============================================================================
"""
GOAL: Ensure a class has ONLY ONE instance and provide a global point of access to it.
USE CASES: Application Configuration, Logging Manager, Database Connection Pool.
"""

class AppConfig:
    """Singleton implementation using __new__."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the single instance once
            cls._instance = super().__new__(cls)
            cls._instance.environment = "Production"
            cls._instance.api_timeout = 30
        return cls._instance


# ==============================================================================
# 5. CREATIONAL PATTERN: THE FACTORY METHOD PATTERN
# ==============================================================================
"""
GOAL: Delegate the instantiation of specific concrete classes to a dedicated Factory.
The caller doesn't need to know the specific class name, only the type needed.
"""

class Notification(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> str:
        pass


class EmailNotification(Notification):
    def send(self, message: str, recipient: str) -> str:
        return f"[EMAIL] Sent to '{recipient}': {message}"


class SMSNotification(Notification):
    def send(self, message: str, recipient: str) -> str:
        return f"[SMS] Sent to phone '{recipient}': {message}"


class PushNotification(Notification):
    def send(self, message: str, recipient: str) -> str:
        return f"[PUSH ALERT] Delivered to device '{recipient}': {message}"


class NotificationFactory:
    """The Factory: Centralizes object creation."""
    @staticmethod
    def create_notifier(channel: str) -> Notification:
        channel_lower = channel.lower()
        if channel_lower == "email":
            return EmailNotification()
        elif channel_lower == "sms":
            return SMSNotification()
        elif channel_lower == "push":
            return PushNotification()
        else:
            raise ValueError(f"Unknown notification channel: '{channel}'")


# ==============================================================================
# 6. BEHAVIORAL PATTERN: THE STRATEGY PATTERN
# ==============================================================================
"""
GOAL: Define a family of interchangeable algorithms, encapsulate each one,
and make them swappable at runtime!
"""

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply_discount(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply_discount(self, total: float) -> float:
        return total * (1.0 - (self.percent / 100.0))


class SeasonalFlatDiscount(DiscountStrategy):
    def __init__(self, flat_off: float):
        self.flat_off = flat_off

    def apply_discount(self, total: float) -> float:
        return max(0.0, total - self.flat_off)


class ShoppingCart:
    """Context that uses a DiscountStrategy."""
    def __init__(self, subtotal: float, discount_strategy: DiscountStrategy):
        self.subtotal = subtotal
        self.discount_strategy = discount_strategy  # Injected strategy!

    def calculate_final_total(self) -> float:
        return self.discount_strategy.apply_discount(self.subtotal)


# ==============================================================================
# 7. BEHAVIORAL PATTERN: THE OBSERVER PATTERN (Pub/Sub)
# ==============================================================================
"""
GOAL: One-to-many dependency between objects. When one object (Subject) changes state,
all registered dependents (Observers) are notified automatically!
REAL-WORLD: YouTube channel subscriber alerts, Stock ticker tickers.
"""

class Subscriber(ABC):
    @abstractmethod
    def update(self, video_title: str) -> None:
        pass


class YouTubeChannel:
    """The Subject / Publisher."""
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self._subscribers: List[Subscriber] = []

    def subscribe(self, subscriber: Subscriber) -> None:
        self._subscribers.append(subscriber)

    def upload_video(self, video_title: str) -> None:
        print(f"\n[CHANNEL: {self.channel_name}] Uploaded new video: '{video_title}'!")
        for sub in self._subscribers:
            sub.update(video_title)


class UserSubscriber(Subscriber):
    def __init__(self, username: str):
        self.username = username

    def update(self, video_title: str) -> None:
        print(f"  -> Notification for @{self.username}: Watch '{video_title}' now!")


# ==============================================================================
# RUNNABLE DEMONSTRATION & VERIFICATION
# ==============================================================================
def main():
    print("=" * 70)
    print("      MODULE 08: ARCHITECTURE & DESIGN PATTERNS DEMONSTRATION")
    print("=" * 70)

    # 1. Composition Demonstration
    print("\n--- 1. Composition (Has-A vs Is-A) ---")
    my_pc = Computer(cpu=CPU("Intel Core i9", 16), memory=Memory(32))
    print(my_pc.boot_up())

    # 2. Singleton Pattern
    print("\n--- 2. Singleton Pattern (One Instance Guaranteed) ---")
    config1 = AppConfig()
    config2 = AppConfig()
    print(f"config1 environment: {config1.environment}")
    print(f"Are config1 and config2 the EXACT same memory instance? {config1 is config2}")

    # 3. Factory Method Pattern
    print("\n--- 3. Factory Method Pattern ---")
    notifier_types = ["email", "sms", "push"]
    for n_type in notifier_types:
        notifier = NotificationFactory.create_notifier(n_type)
        print(notifier.send(message="System maintenance at 2 AM", recipient="user_123"))

    # 4. Strategy Pattern (Swapping Algorithms at Runtime)
    print("\n--- 4. Strategy Pattern (Swapping Discount Policies) ---")
    cart_amount = 200.0

    cart_standard = ShoppingCart(cart_amount, NoDiscount())
    cart_ten_percent = ShoppingCart(cart_amount, PercentageDiscount(percent=10))
    cart_holiday_flat = ShoppingCart(cart_amount, SeasonalFlatDiscount(flat_off=50))

    print(f"Original Price:          ${cart_amount:.2f}")
    print(f"With NoDiscount:         ${cart_standard.calculate_final_total():.2f}")
    print(f"With 10% Discount:       ${cart_ten_percent.calculate_final_total():.2f}")
    print(f"With $50 Flat Discount:  ${cart_holiday_flat.calculate_final_total():.2f}")

    # 5. Observer Pattern
    print("\n--- 5. Observer Pattern (Event Pub/Sub) ---")
    channel = YouTubeChannel(channel_name="Python Mastery")
    sub1 = UserSubscriber("Alice")
    sub2 = UserSubscriber("Bob")
    sub3 = UserSubscriber("Charlie")

    channel.subscribe(sub1)
    channel.subscribe(sub2)
    channel.subscribe(sub3)

    channel.upload_video("Mastering Object-Oriented Programming in Python")

    print("\n" + "=" * 70)
    print("      MODULE 08 COMPLETE: ARCHITECTURE & PATTERNS MASTERED! [DONE]")
    print("=" * 70)


if __name__ == "__main__":
    main()

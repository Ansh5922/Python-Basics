# Python Object-Oriented Programming (OOP) Masterclass

Welcome to the comprehensive, beginner-friendly Python Object-Oriented Programming (OOP) guide. This curriculum is designed to guide a learner from fundamental concepts up to enterprise-grade software architecture and design patterns.

---

## 🗺️ Learning Roadmap & File Structure

```text
OOP/
├── README.md                              # Complete index, roadmap, and learning journey
├── 01_core_basics.py                      # Classes, Objects, self, __init__, instance vs class state
├── 02_encapsulation.py                    # Data protection, name mangling, @property getters/setters/deleters
├── 03_inheritance.py                      # Parent/child hierarchies, super(), MRO, diamond problem, mixins
├── 04_polymorphism.py                     # Duck typing, method overriding, overloading alternatives
├── 05_abstraction.py                      # Abstract Base Classes (ABCs), @abstractmethod, typing.Protocol
├── 06_magic_dunder_methods.py             # Python data model, operator overloading, container protocol
├── 07_decorators_in_oop.py                # Wrappers, method/class decorators, @dataclass
└── 08_architecture_and_design_patterns.py # Composition, SOLID principles, Factory, Strategy, Observer
```

---

## 📚 Module Overview

| Module | Core Concept | Real-World Analogy | Key Takeaway |
| :--- | :--- | :--- | :--- |
| [**`01_core_basics.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/01_core_basics.py) | Classes, Objects & Anatomy | Cookie cutter vs Cookie | Blueprint vs memory instance, `self`, `__init__`, instance vs class variables, `@classmethod`, `@staticmethod`. |
| [**`02_encapsulation.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/02_encapsulation.py) | Data Hiding & Properties | Bank ATM & Capsule | Protecting sensitive state, name mangling (`__attr`), Pythonic `@property` getters, setters with validation. |
| [**`03_inheritance.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/03_inheritance.py) | Hierarchies & Code Reuse | Vehicle & Genetics | Eliminating duplicate code, `super()`, Method Resolution Order (MRO), C3 linearization, Mixins. |
| [**`04_polymorphism.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/04_polymorphism.py) | Unified Interfaces | Universal USB-C Port | Duck Typing (*"If it quacks like a duck..."*), method overriding, handling overloading via `default args` & `singledispatch`. |
| [**`05_abstraction.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/05_abstraction.py) | Interfaces & Contracts | Car Accelerator Pedal | Hiding internal complexity, Abstract Base Classes (`abc.ABC`), enforcing `@abstractmethod`, `typing.Protocol`. |
| [**`06_magic_dunder_methods.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/06_magic_dunder_methods.py) | Python Data Model | Natural English Syntax | Overloading `+`, `-`, `==`, container indexing (`ward[0]`), `len()`, context managers (`with` statement), `__call__`. |
| [**`07_decorators_in_oop.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/07_decorators_in_oop.py) | Behavioral Augmentation | Gift Wrapping | Decorating methods with `*args, **kwargs`, `@wraps`, class decorators, `@cached_property`, modern `@dataclass`. |
| [**`08_architecture_and_design_patterns.py`**](file:///c:/Users/LENOVO/Desktop/DSA_basics/OOP/08_architecture_and_design_patterns.py) | Scalable Architecture | Custom Built PC | "Favor Composition over Inheritance", 5 SOLID principles, Singleton, Factory Method, Strategy, Observer. |

---

## 🚀 How to Run the Modules

Every module is **100% self-contained and runnable**. You can run any module individually to see interactive terminal demonstrations:

```bash
cd OOP

# Run any module
python 01_core_basics.py
python 02_encapsulation.py
python 03_inheritance.py
python 04_polymorphism.py
python 05_abstraction.py
python 06_magic_dunder_methods.py
python 07_decorators_in_oop.py
python 08_architecture_and_design_patterns.py
```

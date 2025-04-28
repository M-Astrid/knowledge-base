Here's the text with all the labels translated to English, while leaving the rest of the content unchanged:

```markdown
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Creational Patterns](#creational-patterns)
  - [Singleton](#singleton)
  - [Builder](#builder)
  - [Factory Method](#factory-method)
  - [Prototype](#prototype)
  - [Abstract Factory](#abstract-factory)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Creational Patterns

### Singleton

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Check if an instance already exists
        if cls._instance is None:
            # If not, create a new instance
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
```

### Builder
```python
class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None

    def __str__(self):
        return (f"Computer specifications:\n"
                f"CPU: {self.cpu}\n"
                f"RAM: {self.ram}\n"
                f"Storage: {self.storage}\n"
                f"GPU: {self.gpu}\n")


class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu: str):
        self.computer.cpu = cpu
        return self

    def set_ram(self, ram: str):
        self.computer.ram = ram
        return self

    def set_storage(self, storage: str):
        self.computer.storage = storage
        return self

    def set_gpu(self, gpu: str):
        self.computer.gpu = gpu
        return self

    def build(self):
        return self.computer


# Example usage
if __name__ == "__main__":
    builder = ComputerBuilder()
    my_computer = (builder
                   .set_cpu("Intel i9")
                   .set_ram("32GB")
                   .set_storage("1TB SSD")
                   .set_gpu("NVIDIA RTX 3080")
                   .build())
```

### Factory Method

```python 
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            return None
```

### Prototype
```python
import copy

# Rectangle class
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __str__(self):
        return f"Rectangle({self.width}, {self.height})"

    # Method for cloning the object
    def clone(self):
        return copy.deepcopy(self)
```

### Abstract Factory
```python
from abc import ABC, abstractmethod

# Interface for Window
class Window(ABC):
    @abstractmethod
    def draw(self):
        pass

# Interface for Scrollbar
class Scrollbar(ABC):
    @abstractmethod
    def scroll(self):
        pass

# Implementation of Window for macOS
class MacOSWindow(Window):
    def draw(self):
        return "Drawing a macOS Window"

# Implementation of Scrollbar for macOS
class MacOSScrollbar(Scrollbar):
    def scroll(self):
        return "Scrolling in macOS Scrollbar"

# Implementation of Window for Windows
class WindowsWindow(Window):
    def draw(self):
        return "Drawing a Windows Window"

# Implementation of Scrollbar for Windows
class WindowsScrollbar(Scrollbar):
    def scroll(self):
        return "Scrolling in Windows Scrollbar"

# Abstract Factory interface
class GUIFactory(ABC):
    @abstractmethod
    def create_window(self) -> Window:
        pass

    @abstractmethod
    def create_scrollbar(self) -> Scrollbar:
        pass

# Factory for macOS
class MacOSFactory(GUIFactory):
    def create_window(self) -> Window:
        return MacOSWindow()

    def create_scrollbar(self) -> Scrollbar:
        return MacOSScrollbar()

# Factory for Windows
class WindowsFactory(GUIFactory):
    def create_window(self) -> Window:
        return WindowsWindow()

    def create_scrollbar(self) -> Scrollbar:
        return WindowsScrollbar()
```

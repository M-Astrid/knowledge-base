<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Behavioral Patterns](#behavioral-patterns)
  - [Command](#command)
  - [Chain of Responsibility](#chain-of-responsibility)
  - [Interpreter](#interpreter)
  - [Iterator](#iterator)
  - [Memento](#memento)
  - [Mediator](#mediator)
  - [Oserver](#oserver)
  - [State](#state)
  - [Strategy](#strategy)
  - [Template Method](#template-method)
  - [Visitor](#visitor)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Behavioral Patterns

### Command
The Command Pattern is a behavioral design pattern that encapsulates a request as an object, thereby allowing for parameterization of clients with queues, requests, and operations. This pattern provides support for undoable operations and helps to decouple objects that issue requests from those that execute them.
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
class Light:
    def on(self):
        print("The light is ON")

    def off(self):
        print("The light is OFF")
        
class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()


class LightOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.off()
        
class RemoteControl:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def press_button(self):
        if self.command:
            self.command.execute()
            
if __name__ == "__main__":
    # Create a receiver
    light = Light()

    # Create commands
    light_on = LightOnCommand(light)
    light_off = LightOffCommand(light)

    # Create invoker
    remote = RemoteControl()

    # Turn the light on
    remote.set_command(light_on)
    remote.press_button()  # Output: The light is ON

    # Turn the light off
    remote.set_command(light_off)
    remote.press_button()  # Output: The light is OFF
```

### Chain of Responsibility
Pattern that allows an object to pass a request along a chain of potential handlers until one of them handles the request. This pattern decouples the sender of a request from its receivers, letting multiple objects handle the request in different ways.
```python
class Handler:
    """Abstract Handler class that defines a method for handling requests."""
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, level, message):
        if self.successor:
            self.successor.handle(level, message)


class InfoHandler(Handler):
    """Concrete Handler that processes INFO level messages."""
    def handle(self, level, message):
        if level == "INFO":
            print(f"[INFO] {message}")
        else:
            super().handle(level, message)


class WarningHandler(Handler):
    """Concrete Handler that processes WARNING level messages."""
    def handle(self, level, message):
        if level == "WARNING":
            print(f"[WARNING] {message}")
        else:
            super().handle(level, message)


class ErrorHandler(Handler):
    """Concrete Handler that processes ERROR level messages."""
    def handle(self, level, message):
        if level == "ERROR":
            print(f"[ERROR] {message}")
        else:
            super().handle(level, message)


# Setting up the chain of responsibility
error_handler = ErrorHandler()
warning_handler = WarningHandler(successor=error_handler)
info_handler = InfoHandler(successor=warning_handler)

# Client code
def log_message(level, message):
    info_handler.handle(level, message)

# Testing the chain
log_message("INFO", "This is an informational message.")
log_message("WARNING", "This is a warning message.")
log_message("ERROR", "This is an error message.")
log_message("DEBUG", "This debug message will not be handled.")
```

### Interpreter
Design pattern that defines a grammatical representation for a language and provides an interpreter to deal with this grammar.
```python
class Expression:
    """Abstract class for expressions."""
    def interpret(self):
        raise NotImplementedError("You should implement this method!")

class Number(Expression):
    """Class to interpret numbers."""
    def __init__(self, value):
        self.value = value

    def interpret(self):
        return self.value

class Addition(Expression):
    """Class to interpret addition operations."""
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self):
        return self.left.interpret() + self.right.interpret()

class Subtraction(Expression):
    """Class to interpret subtraction operations."""
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def interpret(self):
        return self.left.interpret() - self.right.interpret()

# Client code
if __name__ == "__main__":
    # Represents the expression 5 + 3 - 2
    expression = Subtraction(Addition(Number(5), Number(3)), Number(2))
    result = expression.interpret()
    print(f"Result: {result}")  # Output: Result: 6
```

### Iterator
A design pattern that allows for traversing a collection without exposing its underlying representation.
```python
class MyCollection:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def __iter__(self):
        return MyIterator(self.items)

class MyIterator:
    def __init__(self, items):
        self._items = items
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._items):
            item = self._items[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration
```

### Memento
```python

```

### Mediator
```python

```

### Oserver
```python

```

### State
```python

```

### Strategy
```python

```

### Template Method
```python

```

### Visitor
```python

```





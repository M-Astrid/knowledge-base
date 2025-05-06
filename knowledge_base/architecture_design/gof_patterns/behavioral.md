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
Design pattern that allows you to save and restore the previous state of an object without revealing the details of its implementation.
```python
import datetime

# 1. Memento
class EditorMemento:
    def __init__(self, content):
        self._content = content
        self._timestamp = datetime.datetime.now()

    def get_content(self):
        return self._content

    def get_timestamp(self):
        return self._timestamp

    def __str__(self):
        return f"Memento created at: {self._timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

# 2. Originator
class Editor:
    def __init__(self):
        self._content = ""

    def set_content(self, content):
        print(f"Editor: Setting content to '{content}'")
        self._content = content

    def get_content(self):
        return self._content

    def create_memento(self):
        print("Editor: Creating Memento...")
        return EditorMemento(self._content)

    def restore_memento(self, memento):
        print(f"Editor: Restoring content from Memento...")
        self._content = memento.get_content()

# 3. Caretaker
class History:
    def __init__(self):
        self._mementos = []

    def save(self, editor):
        memento = editor.create_memento()
        self._mementos.append(memento)
        print(f"History: Saved Memento. Total mementos: {len(self._mementos)}")

    def undo(self, editor):
        if not self._mementos:
            print("History: No mementos to undo.")
            return

        # Remove the last saved memento
        memento = self._mementos.pop()
        print(f"History: Undoing to previous state. Remaining mementos: {len(self._mementos)}")
        editor.restore_memento(memento)

    def show_history(self):
        print("\nHistory of Mementos:")
        for memento in self._mementos:
            print(f"- {memento}")
        print("-" * 20)

# Client Code
if __name__ == "__main__":
    editor = Editor()
    history = History()

    editor.set_content("Initial content.")
    history.save(editor) # Save the initial state

    editor.set_content("Second version of content.")
    history.save(editor) # Save the second state

    editor.set_content("Third and final version.")
    history.save(editor) # Save the third state

    print("\nCurrent Editor Content:", editor.get_content())
    history.show_history()

    print("\nPerforming Undo...")
    history.undo(editor)
    print("Current Editor Content after undo:", editor.get_content())
    history.show_history()

    print("\nPerforming another Undo...")
    history.undo(editor)
    print("Current Editor Content after second undo:", editor.get_content())
    history.show_history()

    print("\nPerforming one more Undo...")
    history.undo(editor)
    print("Current Editor Content after third undo:", editor.get_content())
    history.show_history()

    print("\nAttempting to Undo with no mementos...")
    history.undo(editor)
    print("Current Editor Content after attempted undo:", editor.get_content())
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





<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Structural Patterns](#structural-patterns)
  - [Adapter](#adapter)
  - [Bridge](#bridge)
  - [Composite](#composite)
  - [Decorator](#decorator)
  - [Facade](#facade)
  - [Flyweight](#flyweight)
  - [Proxy](#proxy)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Structural Patterns

### Adapter
The Adapter Pattern is a design pattern that allows incompatible interfaces to work together. It acts as a bridge between two incompatible interfaces by converting the interface of a class into another interface that the client expects.
```python
# Старый интерфейс
class OldSystem:
    def specific_request(self):
        return "Result from Old System"

# Новый интерфейс
class NewSystemInterface:
    def request(self):
        pass

# Адаптер, который реализует новый интерфейс и делегирует запросы старой системе
class Adapter(NewSystemInterface):
    def __init__(self, old_system: OldSystem):
        self.old_system = old_system

    def request(self):
        return self.old_system.specific_request()
```

### Bridge
The Bridge pattern is a structural design pattern that separates an abstraction from its implementation, allowing the two to vary independently. This is particularly useful when you want to avoid a permanent binding between an abstraction and its implementation, enabling you to change them independently.
```python
from abc import ABC, abstractmethod

# Implementor
class Device(ABC):
    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass


# Concrete Implementor 1
class TV(Device):
    def on(self):
        return "TV is ON"

    def off(self):
        return "TV is OFF"


# Concrete Implementor 2
class Radio(Device):
    def on(self):
        return "Radio is ON"

    def off(self):
        return "Radio is OFF"


# Abstraction
class RemoteControl(ABC):
    def __init__(self, device: Device):
        self.device = device

    @abstractmethod
    def press_on_button(self):
        pass

    @abstractmethod
    def press_off_button(self):
        pass


# Refined Abstraction
class BasicRemote(RemoteControl):
    def press_on_button(self):
        return self.device.on()

    def press_off_button(self):
        return self.device.off()
```

### Composite
The Composite pattern is a structural design pattern that allows you to compose objects into tree structures to represent part-whole hierarchies.
```python 
from abc import ABC, abstractmethod

# Component
class FileComponent(ABC):
    @abstractmethod
    def show_info(self):
        pass

# Leaf
class File(FileComponent):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size  # Size in bytes

    def show_info(self):
        return f"File: {self.name}, Size: {self.size} bytes"

# Composite
class Directory(FileComponent):
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, component: FileComponent):
        self.children.append(component)

    def remove(self, component: FileComponent):
        self.children.remove(component)

    def show_info(self):
        info = [f"Directory: {self.name}"]
        for child in self.children:
            info.append("  " + child.show_info())
        return "\n".join(info)

# Client code
if __name__ == "__main__":
    # Create files
    file1 = File("file1.txt", 150)
    file2 = File("file2.jpg", 5000)
    file3 = File("file3.pdf", 800)

    # Create directories
    dir1 = Directory("Documents")
    dir2 = Directory("Pictures")

    # Add files to directories
    dir1.add(file1)
    dir1.add(file3)
    dir2.add(file2)

    # Create a root directory
    root_dir = Directory("Root")
    root_dir.add(dir1)
    root_dir.add(dir2)

    # Show the file system structure
    print(root_dir.show_info())
```

### Decorator
The Decorator pattern is a structural design pattern that allows you to extend the behavior of an object without modifying its structure.
```python
class Message:
    def get_content(self):
        return "Hello, World!"

# Base decorator
class MessageDecorator:
    def __init__(self, message):
        self._message = message

    def get_content(self):
        return self._message.get_content()

# Concrete decorators
class BoldDecorator(MessageDecorator):
    def get_content(self):
        return f"<b>{super().get_content()}</b>"

class ItalicDecorator(MessageDecorator):
    def get_content(self):
        return f"<i>{super().get_content()}</i>"

# Client code
if __name__ == "__main__":
    # Original message
    message = Message()
    print("Original Message:")
    print(message.get_content())

    # Creating decorators
    bold_message = BoldDecorator(message)
    italic_message = ItalicDecorator(message)

    print("\nBold Message:")
    print(bold_message.get_content())

    print("\nItalic Message:")
    print(italic_message.get_content())

    # Combining decorators
    bold_and_italic_message = BoldDecorator(ItalicDecorator(message))
    print("\nBold and Italic Message:")
    print(bold_and_italic_message.get_content())
```

### Facade
The Facade pattern is a structural design pattern that provides a simplified interface to a complex system.
```python
# Subsystem classes
class DVDPlayer:
    def on(self):
        return "DVD Player is ON"

    def play(self, movie):
        return f"Playing '{movie}'"

    def stop(self):
        return "Stopping DVD Player"

class Projector:
    def on(self):
        return "Projector is ON"

    def set_input(self, input):
        return f"Setting input to {input}"

    def off(self):
        return "Projector is OFF"

class SoundSystem:
    def on(self):
        return "Sound System is ON"

    def set_volume(self, volume):
        return f"Volume set to {volume}"

    def off(self):
        return "Sound System is OFF"

# Facade
class HomeTheaterFacade:
    def __init__(self):
        self.dvd_player = DVDPlayer()
        self.projector = Projector()
        self.sound_system = SoundSystem()

    def watch_movie(self, movie):
        self.dvd_player.on()
        self.projector.on()
        self.projector.set_input("DVD")
        self.sound_system.on()
        self.sound_system.set_volume(10)
        return f"{self.dvd_player.play(movie)}\n{self.sound_system.set_volume(10)}"

    def end_movie(self):
        results = [
            self.dvd_player.stop(),
            self.sound_system.off(),
            self.projector.off()
        ]
        return "\n".join(results)

# Client code
if __name__ == "__main__":
    home_theater = HomeTheaterFacade()
    
    print(home_theater.watch_movie("Inception"))
    print("\nEnding Movie...")
    print(home_theater.end_movie())
```

### Flyweight
The Flyweight Pattern is a structural design pattern that aims to minimize memory usage by sharing as much data as possible with similar objects. It is particularly useful when you need to create a large number of objects that share common properties.
```python
class CharFlyweight:
    """Flyweight class that contains shared character data."""
    def __init__(self, char: str):
        self.char = char

    def display(self, font):
        return f"Character: {self.char}, Font: {font}"


class FlyweightFactory:
    """Factory class to manage the creation and storage of flyweight objects."""
    def __init__(self):
        self.flyweights = {}

    def get_flyweight(self, char: str) -> CharFlyweight:
        if char not in self.flyweights:
            self.flyweights[char] = CharFlyweight(char)
            print(f"Created flyweight for character: {char}")
        return self.flyweights[char]


class TextFormatter:
    """Client class to demonstrate the use of flyweights."""
    def __init__(self):
        self.factory = FlyweightFactory()

    def format_text(self, text: str, font: str):
        formatted_text = []
        for char in text:
            flyweight = self.factory.get_flyweight(char)
            formatted_text.append(flyweight.display(font))
        return "\n".join(formatted_text)


# Client code
if __name__ == "__main__":
    text_formatter = TextFormatter()
    print(text_formatter.format_text("hello", "Arial"))
    print(text_formatter.format_text("world", "Times New Roman"))
```

### Proxy

```python
from abc import ABC, abstractmethod

# Subject Interface
class Image(ABC):
    @abstractmethod
    def display(self):
        pass

# Real subject
class RealImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self.load_image_from_disk()

    def load_image_from_disk(self):
        print(f"Loading {self.filename}")

    def display(self):
        print(f"Displaying {self.filename}")

# Proxy
class ProxyImage(Image):
    def __init__(self, filename: str):
        self.filename = filename
        self.real_image = None  # Placeholder for RealImage

    def display(self):
        if self.real_image is None:
            self.real_image = RealImage(self.filename)
        self.real_image.display()

# Client code
if __name__ == "__main__":
    # Create a proxy image
    image1 = ProxyImage("photo_1.jpg")
    
    # Image is loaded when displayed for the first time
    image1.display()  
    # Image is displayed again without loading it from disk
    image1.display()  
```
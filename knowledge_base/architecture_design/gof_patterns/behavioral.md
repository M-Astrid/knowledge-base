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
- Mediator: Defines an interface for communicating with Colleague objects.
- Concrete Mediator: Implements the Mediator interface and coordinates communication between Colleague objects. It knows and maintains references to the Colleague objects it manages.
- Colleague: Defines an interface for objects that communicate with the Mediator.
- Concrete Colleague: Implements the Colleague interface. Each Concrete Colleague communicates with the Mediator instead of directly with other Colleagues.

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
Design pattern that aims to reduce coupling between a set of objects by encapsulating how these objects interact. Instead of objects communicating directly with each other, they communicate through a Mediator object. This centralizes the communication logic and makes it easier to manage and modify interactions.
```python
# 1. Mediator Interface
class ChatRoomMediator:
    def send_message(self, message, user):
        pass

# 2. Concrete Mediator
class ConcreteChatRoom(ChatRoomMediator):
    def __init__(self):
        self._users = []

    def add_user(self, user):
        self._users.append(user)
        print(f"ChatRoom: {user.get_name()} joined the room.")

    def send_message(self, message, sender):
        print(f"ChatRoom: Message received from {sender.get_name()}. Broadcasting...")
        for user in self._users:
            # Don't send the message back to the sender
            if user != sender:
                user.receive_message(message, sender)

# 3. Colleague Interface
class User:
    def __init__(self, name, mediator):
        self._name = name
        self._mediator = mediator  # The user knows its mediator

    def get_name(self):
        return self._name

    def send(self, message):
        print(f"User {self._name}: Sending message: '{message}'")
        self._mediator.send_message(message, self) # Communicate through the mediator

    def receive_message(self, message, sender):
        print(f"User {self._name}: Received message from {sender.get_name()}: '{message}'")

# Client Code
if __name__ == "__main__":
    # Create the Mediator
    chat_room = ConcreteChatRoom()

    # Create Colleague objects (Users) and associate them with the Mediator
    user1 = User("Alice", chat_room)
    user2 = User("Bob", chat_room)
    user3 = User("Charlie", chat_room)

    # Add users to the chat room (the Mediator keeps track of them)
    chat_room.add_user(user1)
    chat_room.add_user(user2)
    chat_room.add_user(user3)

    print("\n--- Starting Conversation ---")

    # Users send messages through the Mediator
    user1.send("Hi everyone!")
    print("-" * 20)
    user2.send("Hello Alice and Charlie!")
    print("-" * 20)
    user3.send("Hey guys!")
    print("-" * 20)

    print("\n--- Conversation Ended ---")
```

### Oserver
Pattern that defines a one-to-many dependency between objects so that when one object (the Subject) changes state, all its dependents (the Observers) are notified and updated automatically.
Core Components:

- Subject (Observable): The object that holds the state and notifies its Observers when the state changes. It maintains a list of registered Observers and provides methods for attaching, detaching, and notifying them.
- Observer: The interface that defines the update method to be called by the Subject when its state changes.
- Concrete Subject: Implements the Subject interface. It stores the state of interest to the Observers and notifies them when the state changes.
- Concrete Observer: Implements the Observer interface. It registers with a Concrete Subject and implements the update method to react to state changes.

```python
# 2. Observer Interface
class Observer:
    def update(self, subject):
        pass

# 1. Subject (Observable)
class WeatherStation:
    def __init__(self):
        self._observers = []
        self._temperature = None

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"WeatherStation: Attached observer: {type(observer).__name__}")

    def detach(self, observer):
        try:
            self._observers.remove(observer)
            print(f"WeatherStation: Detached observer: {type(observer).__name__}")
        except ValueError:
            print(f"WeatherStation: Observer not found: {type(observer).__name__}")

    def notify(self):
        print("WeatherStation: Notifying observers...")
        for observer in self._observers:
            observer.update(self) # Pass the subject (itself) to the observer

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, temperature):
        print(f"\nWeatherStation: Setting temperature to {temperature}°C")
        self._temperature = temperature
        self.notify() # Notify observers when the temperature changes

# 4. Concrete Observers
class TemperatureDisplay(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, subject):
        temperature = subject.get_temperature()
        print(f"{self._name}: Temperature updated to {temperature}°C")

class WeatherWarningSystem(Observer):
    def __init__(self):
        self._warning_threshold = 30

    def update(self, subject):
        temperature = subject.get_temperature()
        if temperature is not None and temperature > self._warning_threshold:
            print("WeatherWarningSystem: WARNING! High temperature detected!")

# Client Code
if __name__ == "__main__":
    # Create the Subject
    weather_station = WeatherStation()

    # Create Concrete Observers
    display1 = TemperatureDisplay("Display 1")
    display2 = TemperatureDisplay("Display 2")
    warning_system = WeatherWarningSystem()

    # Attach Observers to the Subject
    weather_station.attach(display1)
    weather_station.attach(display2)
    weather_station.attach(warning_system)

    # Change the state of the Subject, triggering notifications
    weather_station.set_temperature(25)
    weather_station.set_temperature(28)
    weather_station.set_temperature(32) # This should trigger the warning system

    # Detach an Observer
    weather_station.detach(display1)

    # Change the state again, only remaining observers will be notified
    weather_station.set_temperature(20)

    # Attempt to detach an observer that's not attached
    weather_station.detach(display1)
```

### State
The State pattern is a behavioral design pattern that allows an object to alter its behavior when its internal state changes. The object will appear to change its class. This is achieved by creating separate classes for each state the object can be in and delegating the state-specific behavior to the current state object.

Core Components:

- Context: The object whose behavior changes depending on its state. It maintains a reference to the current State object and delegates state-specific requests to it.
- State: An interface or abstract class that defines the methods for the state-specific behavior.
- Concrete States: Implement the State interface and define the behavior for a specific state of the Context.
```python
# 2. State Interface (Abstract Base Class)
from abc import ABC, abstractmethod

class TrafficLightState(ABC):
    @abstractmethod
    def handle(self, traffic_light):
        pass

# 3. Concrete States
class RedLightState(TrafficLightState):
    def handle(self, traffic_light):
        print("Traffic Light: Red Light - STOP")
        # Transition to the next state (Yellow) after some time (simulated)
        print("Traffic Light: Changing to Yellow...")
        traffic_light.set_state(YellowLightState())

class YellowLightState(TrafficLightState):
    def handle(self, traffic_light):
        print("Traffic Light: Yellow Light - PREPARE TO STOP")
        # Transition to the next state (Green) after some time (simulated)
        print("Traffic Light: Changing to Green...")
        traffic_light.set_state(GreenLightState())

class GreenLightState(TrafficLightState):
    def handle(self, traffic_light):
        print("Traffic Light: Green Light - GO")
        # Transition to the next state (Red) after some time (simulated)
        print("Traffic Light: Changing to Red...")
        traffic_light.set_state(RedLightState())

# 1. Context
class TrafficLight:
    def __init__(self):
        # Set the initial state
        self._current_state = RedLightState()
        print("Traffic Light: Initialized to Red Light.")

    def set_state(self, state: TrafficLightState):
        self._current_state = state

    def request(self):
        # Delegate the request to the current state object
        self._current_state.handle(self)

# Client Code
if __name__ == "__main__":
    traffic_light = TrafficLight()

    # Simulate the traffic light cycling through states
    print("\nSimulating Traffic Light Cycle:")
    traffic_light.request() # Start with Red, will transition to Yellow
    print("-" * 20)
    traffic_light.request() # In Yellow, will transition to Green
    print("-" * 20)
    traffic_light.request() # In Green, will transition to Red
    print("-" * 20)
    traffic_light.request() # Back to Red
```

### Strategy
The Strategy pattern is a behavioral design pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable. It allows a client to choose an algorithm from a family of algorithms and use it without knowing the details of its implementation.
```python
# 1. Strategy Interface
class PaymentStrategy:
    def pay(self, amount):
        pass

# 2. Concrete Strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number, expiry_date, cvv):
        self._card_number = card_number
        self._expiry_date = expiry_date
        self._cvv = cvv

    def pay(self, amount):
        print(f"Paying ${amount:.2f} using Credit Card: ****{self._card_number[-4:]}")
        # Simulate payment processing...
        print("Payment processed successfully!")

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self._email = email

    def pay(self, amount):
        print(f"Paying ${amount:.2f} using PayPal account: {self._email}")
        # Simulate payment processing...
        print("Payment processed successfully!")

class BitcoinPayment(PaymentStrategy):
    def __init__(self, wallet_address):
        self._wallet_address = wallet_address

    def pay(self, amount):
        print(f"Paying ${amount:.2f} using Bitcoin to wallet: {self._wallet_address}")
        # Simulate payment processing...
        print("Payment processed successfully!")

# 3. Context
class ShoppingCart:
    def __init__(self, payment_strategy):
        self._payment_strategy = payment_strategy
        self._items = []

    def add_item(self, item, price):
        self._items.append({"item": item, "price": price})
        print(f"Added '{item}' to cart.")

    def calculate_total(self):
        total = sum(item["price"] for item in self._items)
        return total

    def set_payment_strategy(self, payment_strategy):
        self._payment_strategy = payment_strategy
        print(f"Payment strategy set to: {type(payment_strategy).__name__}")

    def checkout(self):
        total = self.calculate_total()
        print(f"\nCheckout initiated. Total amount: ${total:.2f}")
        if self._payment_strategy:
            self._payment_strategy.pay(total)
        else:
            print("No payment strategy selected.")

# Client Code
if __name__ == "__main__":
    # Create Concrete Strategy objects
    credit_card_strategy = CreditCardPayment("1234567890123456", "12/25", "123")
    paypal_strategy = PayPalPayment("customer@example.com")
    bitcoin_strategy = BitcoinPayment("abc123xyz789")

    # Create a Context (ShoppingCart) with an initial strategy
    cart = ShoppingCart(credit_card_strategy)

    # Add items to the cart
    cart.add_item("Laptop", 1200.00)
    cart.add_item("Mouse", 25.00)

    # Checkout using the current strategy
    cart.checkout()

    print("\n--- Switching Payment Strategy ---")

    # Switch to a different payment strategy
    cart.set_payment_strategy(paypal_strategy)

    # Add another item
    cart.add_item("Keyboard", 75.00)

    # Checkout using the new strategy
    cart.checkout()

    print("\n--- Switching to Bitcoin ---")

    # Switch to Bitcoin payment
    cart.set_payment_strategy(bitcoin_strategy)

    # Checkout again (total includes all items added so far)
    cart.checkout()

    print("\n--- No Strategy Selected ---")
    cart_no_strategy = ShoppingCart(None)
    cart_no_strategy.add_item("Book", 30.00)
    cart_no_strategy.checkout()
```

### Template Method
The Template Method pattern is a behavioral design pattern that defines the skeleton of an algorithm in a superclass but lets subclasses override specific steps of the algorithm without changing its structure.
```python
import time

# 1. Abstract Class (AbstractClass)
class HouseBuilder:
    def build_house(self):
        """
        The template method defines the skeleton of the algorithm.
        """
        self.prepare_foundation()
        self.build_walls()
        self.build_roof()
        self.install_windows()
        self.install_doors()
        self.decorate_interior()
        print("House construction complete!")

    # Abstract operations (must be implemented by subclasses)
    def prepare_foundation(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def build_walls(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def build_roof(self):
        raise NotImplementedError("Subclass must implement abstract method")

    # Concrete operations (can be overridden by subclasses)
    def install_windows(self):
        print("Installing standard windows.")
        time.sleep(1)

    def install_doors(self):
        print("Installing standard doors.")
        time.sleep(1)

    # Hook method (optional, can be overridden by subclasses)
    def decorate_interior(self):
        """
        This is a hook method. Subclasses can override it to customize
        the interior decoration, but it's not mandatory.
        """
        print("Performing basic interior decoration.")
        time.sleep(1)

# 2. Concrete Classes (ConcreteClass)
class WoodenHouseBuilder(HouseBuilder):
    def prepare_foundation(self):
        print("Preparing a simple wooden foundation.")
        time.sleep(1)

    def build_walls(self):
        print("Building wooden walls.")
        time.sleep(2)

    def build_roof(self):
        print("Building a wooden roof.")
        time.sleep(1.5)

    # Override a concrete operation
    def install_windows(self):
        print("Installing wooden-framed windows.")
        time.sleep(1)

    # Override the hook method
    def decorate_interior(self):
        print("Decorating interior with a rustic wooden theme.")
        time.sleep(2)

class BrickHouseBuilder(HouseBuilder):
    def prepare_foundation(self):
        print("Preparing a reinforced concrete foundation.")
        time.sleep(2)

    def build_walls(self):
        print("Building brick walls.")
        time.sleep(3)

    def build_roof(self):
        print("Building a tiled roof.")
        time.sleep(2)

    # We can choose not to override concrete operations like install_doors
    # and use the default implementation from the base class.

    # We can also choose not to override the decorate_interior hook method,
    # using the basic decoration.

# Client Code
if __name__ == "__main__":
    print("--- Building a Wooden House ---")
    wooden_builder = WoodenHouseBuilder()
    wooden_builder.build_house()

    print("\n--- Building a Brick House ---")
    brick_builder = BrickHouseBuilder()
    brick_builder.build_house()
```
When to Use the Template Method Pattern:

- When you have a family of algorithms that have a similar structure but differ in specific steps.
- When you want to enforce a particular sequence of operations while allowing subclasses to customize the implementation of individual steps.
- When you want to provide a common framework for subclasses to follow

### Visitor
```python

```





---
title: "Strategy Pattern with Python"
date: "2024-09-16"
description: "A practical guide to the Strategy design pattern in Python, using a payment processor as the running example."
tags: ["python", "design-patterns"]
---

This article introduces strategy design pattern with examples and use cases. The example codes are in Python, and a brief intro to Python abstract classes is included.

## Strategy Pattern

Strategy pattern suggests a simple but very useful paradigm to design OOP systems where there are multiple algorithms/strategies to do a task. The pattern prescribes encapsulating algorithms into a common interface and using that interface to invoke those algorithms. This gives the client (the part of the code that uses the algorithms) the flexibility to choose any algorithm at runtime.

## Example Scenarios

Let's think of the map app we all have in our phones. Users can find routes from place A to place B, and the app gives us a couple of possible modes of transportation — walking, cycling, bike riding, public bus or car — along with the time each would take.

This feature is a nice candidate for the strategy pattern. Modes of transportation are different algorithms/strategies and a common interface provides the travel time from A to B.

Let's look at another example. A payment processor in an e-commerce site can accept payment in multiple ways — cards, MFS (Mobile Financial System), or cryptocurrency. Designing this payment processor is a prime candidate for strategy pattern. Here modes of payment are the algorithms, and the payment processor is the client.

## Code Examples

Examples with code are even better. Here I will use Python, but this pattern — or any design pattern for that matter — is applicable and implementable in all OOP-supported languages.

So, we are designing a service for processing payments for an e-commerce site. For starters, users can pay through Visa and Mastercard. What would the code structure look like?

```python
# visa card related processing
def visa_pay(self, amount):
  print("Doing visa card related processing")
  print(f"Receiving a payment through Visa card of amount {amount}")

# master card related processing
def master_pay(self, amount):
  print("Doing Master card related processing")
  print(f"Receiving a payment through Master card of amount {amount}")

# this is our payment processor
def payment_processor(payment_type: str, amount: float):
  if payment_type == "visa":
    visa_pay(amount)
  else payment_type == "master":
    master_pay(amount)
```

Simple, right? Now what if users want to pay with American Express (Amex)? We add another function `amex_pay` and update `payment_processor`:

```python
...

def amex_pay(self, amount):
  print("Doing Amex card related processing")
  print(f"Receiving a payment through Amex card of amount {amount}")


def payment_processor(payment_type: str, amount: float):
  if payment_type == "visa":
    visa_pay(amount)
  elif payment_type == "master":
    master_pay(amount)
  elif payment_type == "amex":
    amex_pay(amount)
```

No matter how simple this looks, one thing is clear: every time we add a new payment mode we have to change `payment_processor` in addition to adding the new payment code. Our `payment_processor` is tightly coupled to individual payment modes, even though all of them take the same arguments and return the same data.

In cases such as this, **Strategy Pattern** suggests a better way to organise our code and make it more extensible and portable. The suggestion: payment modes share a common interface and `payment_processor` codes to that interface instead of to individual functions. New payment modes can be added without changing `payment_processor` at all — they'll be supported right out of the bat.

Let's try it out. But before that, some Python language prerequisites. If you're familiar with Python's abstract class system, you may skip the next section and jump straight to the code.

### Abstract Class in Python

An interface provides a blueprint through abstract functions, and interface-implementing classes must concretely implement those abstract functions. All classes that implement the same interface will therefore have the same API.

Python has no `interface` keyword as Java does. Abstract classes give us the same facility. We declare an abstract class with abstract methods; all concrete subclasses must implement those methods, giving them the same methods.

To get abstract classes we use the `abc` module from Python's standard library. It supplies two components: `ABC` (the base class all abstract classes must inherit) and `abstractmethod` (a decorator marking methods that subclasses must implement).

### Code Example of Strategy Pattern

Now let's hop into the code-wagon.

```python
from abc import ABC, abstractmethod

# our interface made out of an abstract class.
class PaymentInterface(ABC):

  # all payment mode will implement this abstract method
  @abstractmethod
  def pay(self, amount):
    pass


class VisaPayment(PaymentInterface):   # inherits the PaymentInterface and implements the `pay` method

  def pay(self, amount):
    print("Doing visa card related processing")
    print(f"Receiving a payment through Visa of amount {amount}")


class MasterPayment(PaymentInterface):

  def pay(self, amount):
    print("Doing Master card related processing")
    print(f"Receiving a payment through Master of amount {amount}")


class AmexPayment(PaymentInterface):

  def pay(self, amount):
    print("Doing Amex card related processing")
    print(f"Receiving a payment through Amex of amount {amount}")


def payment_processor(payment_method: PaymentInterface, amount: float):
  payment_method.pay(amount)
```

`payment_processor` looks **clean** and is very **unlikely to need change** if we add new payment modes. Adding Bkash (MFS) only requires a new `BkashPayment` class — no change in `payment_processor`. This is neat and a win for code maintainability.

How do we map names to actual payment methods at runtime? One example:

```python
class PaymentService:
    def __init__(self):
        self.payment_methods = {
            "visa": VisaPayment(),
            "master": MasterPayment(),
            "amex": AmexPayment()
        }

    def process_payment(self, method: str, amount: float):
        if method not in self.payment_methods:
            raise ValueError(f"Unsupported payment method: {method}")

        payment_method = self.payment_methods[method]
        payment_processor(payment_method, amount)
```

The class initializes a dictionary that maps payment method names to `PaymentInterface` implementations. When a new payment method is added, we add the corresponding class and a single entry in the mapper. This mapper part is totally dependent on the context of implementation.

### When to Use Strategy Pattern

* You've got a bunch of related algorithms and want to switch between them dynamically.
* You want to avoid a monster `if-elif-else` chain in your code. Trust me, future you will thank present you for not creating that mess.

Remember, design patterns are tools, not rules. Use them only when you have time and reason to do so.

**Skip the Strategy Pattern when:**

* You've only got a couple of algorithms that rarely change.
* The algorithms and their context are very simple. Sometimes a plain `if-else` is all you need. Don't over-complicate things!

### Wrapping Up

Strategy pattern is a cool code-toolkit. It gives us:

* **Flexibility:** add new strategies or algorithms without changing or impacting existing client code.
* **Cleaner Code:** no more long `if-elif-else` chains.

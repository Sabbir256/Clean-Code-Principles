# Liskov Substitution Principle
This states that, if you have objects in the program, then you should be able to replace those objects with instances of their subtypes or subclasses.

> If S is a subtype of T, then objects of type T maybe replaced with objects of type S.

Let's take an example:
```python
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order:Order, securite_code: str) -> None:
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def pay(self, order: Order, securite_code: str) -> None:
        print('security code for payment is: {}'.format(securite_code))
        print('Order has been paid in debit')
        order.status = 'paid'

class CreditPaymentProcessor(PaymentProcessor):
    def pay(self, order: Order, securite_code: str) -> None:
        print('security code for payment is: {}'.format(securite_code))
        print('Order has been paid in credit')
        order.status = 'paid'

class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self, order: Order, securite_code: str) -> None:
        print('security code for payment is: {}'.format(securite_code))
        print('Order has been paid in paypal')
        order.status = 'paid'
```

The above code already follows Liskov Principle but has a slight problem. Paypal does not use security code for verification, it uses email address to verify. Now if we change `security_code` to `email` in `PaypalPaymentProcessor` class, then still we can substitute objects, but that would break the Liskov Substitution Principle. We would be forcing something to do that its not suppossed to. Also it would create confusion later on.

One way to fix that is to remove security code altogether and initialize it when creating the object.

# Solution
```python
from abc import ABC, abstractmethod

class Order:
    items = []
    quantities = []
    price = []
    status = ''

    def add_item(self, name: str, quantity: int, price: float) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.price.append(price)

    def total_price(self) -> float:
        total = 0
        for price in self.price:
            total += price
        return total

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order:Order) -> None:
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str) -> None:
        self.security_code = security_code

    def pay(self, order: Order) -> None:
        print('security code for payment is: {}'.format(self.securite_code))
        print('Order has been paid in debit')
        order.status = 'paid'

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str) -> None:
        self.security_code = security_code

    def pay(self, order: Order) -> None:
        print('security code for payment is: {}'.format(self.securite_code))
        print('Order has been paid in credit')
        order.status = 'paid'

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email: str) -> None:
        self.email = email

    def pay(self, order: Order) -> None:
        print('security code for payment is: {}'.format(self.email))
        print('Order has been paid in paypal')
        order.status = 'paid'
        
order = Order()
order.add_item('pen', 1, 5.0)
order.add_item('paper', 5, 10.0)

total = order.total_price()
print('total price: {}'.format(total))

make_payment = PaypalPaymentProcessor('hi@world.com')
make_payment.pay(order)
```

Here `DebitPaymentProcessor, CreditPaymentProcessor ` & `PaypalPaymentProcessor` are subtypes of each other and we can substitute any of them for `make_payment` object and it will work properly.
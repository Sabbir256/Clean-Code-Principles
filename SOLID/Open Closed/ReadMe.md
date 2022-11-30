# Open-Closed Principle
This principle indicates that, classes should be open for extension and closed for modification. In simple terms, you can extend a class through inheritance but you can not modify the class for implementing a new feature.

Lets take the example from SRP.
```python
class PaymentProcessor:
    def pay_debit(self, order: Order) -> None:
        print('Order has been paid in debit')
        order.status = 'paid'

    def pay_credit(self, order: Order) -> None:
        print('Order has been paid in credit')
        order.status = 'paid'
```
If we take a look at the ```PaymentProcessor``` class we will see that it contains two payment methods, but what if we want to add another payment method, suppose bitcoin or paypal. Then we will have to modify this class and add that payment method, then it will break the Open-Closed principle.

To solve that we need to extend this class and create abstract classes and methods for different types of payment. That way the system will not break even if we add multiple payment methods. We will not have to change code from whole codebase.

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
    def pay(self, order: Order) -> None:
        print('Order has been paid in debit')
        order.status = 'paid'

class CreditPaymentProcessor(PaymentProcessor):
    def pay(self, order: Order) -> None:
        print('Order has been paid in credit')
        order.status = 'paid'

class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self, order: Order) -> None:
        print('Order has been paid in paypal')
        order.status = 'paid'
        

order = Order()
order.add_item('pen', 1, 5.0)
order.add_item('paper', 5, 10.0)

total = order.total_price()
print('total price: {}'.format(total))

make_payment = PaypalPaymentProcessor()
make_payment.pay(order)

"""
    output:
    total price: 15.0
    Order has been paid in paypal
"""
```

This way we can extend the ```PaymentProcessor``` abstract class and we do not need to modify the base class. 
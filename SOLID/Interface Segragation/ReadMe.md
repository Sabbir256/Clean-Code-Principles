# Interface Segragation
Overall it's better if you have several specific interface, rather than one general purpose interface.

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

    @abstractmethod
    def auth(self, code: str) -> None:
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str) -> None:
        self.security_code = security_code
        self.verified = False

    def auth(self, code: str) -> None:
        print(f'authorization code: {code}')
        self.verified = True

    def pay(self, order: Order) -> None:
        if not self.verified:
            raise Exception('Payment not authorized')
        print('security code for payment is: {}'.format(self.security_code))
        print('Order has been paid in debit')
        order.status = 'paid'

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str) -> None:
        self.security_code = security_code

    def auth(self, code: str) -> None:
        raise Exception('Credit payment does not support authorization')

    def pay(self, order: Order) -> None:
        print('security code for payment is: {}'.format(self.securite_code))
        print('Order has been paid in credit')
        order.status = 'paid'

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email: str) -> None:
        self.email = email
        self.verified = False

    def auth(self, code: str) -> None:
        print(f'authorization code: {code}')
        self.verified = True

    def pay(self, order: Order) -> None:
        if not self.authorized:
            raise Exception('Payment not authorized')
        print('security code for payment is: {}'.format(self.email))
        print('Order has been paid in paypal')
        order.status = 'paid'

if __name__ == '__main__':      
    order = Order()
    order.add_item('pen', 1, 5.0)
    order.add_item('paper', 5, 10.0)

    total = order.total_price()
    print('total price: {}'.format(total))

    make_payment = DebitPaymentProcessor('345678')
    make_payment.auth('1234')
    make_payment.pay(order)
```

From the code above, we can see that the auth function implementation is not necessary for credit payments, still it is inheriting from the parent class. That is the problem with one general interface. We can solve this by splitting the interface and creating subclass.

# Solution
```python
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order:Order) -> None:
        pass

class PaymentProcessor_SMS(PaymentProcessor):
    @abstractmethod
    def auth(self, code: str) -> None:
        pass


class DebitPaymentProcessor(PaymentProcessor_SMS):
    def __init__(self, security_code: str) -> None:
        self.security_code = security_code
        self.verified = False

    def auth(self, code: str) -> None:
        print(f'authorization code: {code}')
        self.verified = True

    def pay(self, order: Order) -> None:
        if not self.verified:
            raise Exception('Payment not authorized')
        print('security code for payment is: {}'.format(self.security_code))
        print('Order has been paid in debit')
        order.status = 'paid'

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str) -> None:
        self.security_code = security_code

    def pay(self, order: Order) -> None:
        print('security code for payment is: {}'.format(self.security_code))
        print('Order has been paid in credit')
        order.status = 'paid'

class PaypalPaymentProcessor(PaymentProcessor_SMS):
    def __init__(self, email: str) -> None:
        self.email = email
        self.verified = False

    def auth(self, code: str) -> None:
        print(f'authorization code: {code}')
        self.verified = True

    def pay(self, order: Order) -> None:
        if not self.authorized:
            raise Exception('Payment not authorized')
        print('security code for payment is: {}'.format(self.email))
        print('Order has been paid in paypal')
        order.status = 'paid'
```

By splitting the interface for auth, we can inherit this class only where the SMS authentication is necessary. 

But we can do better. Rather than importing from different classes, we can use <b>composition</b> to solve the problem.

```python
class SMS_Auth:
    verified = False
    
    def verify_payment(self, code: str)->None:
        print(f'authorization code: {code}')
        self.verified = True

    def is_verified(self) -> bool:
        return self.verified


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order:Order) -> None:
        pass

class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str, auth: SMS_Auth) -> None:
        self.security_code = security_code
        self.auth = auth

    def pay(self, order: Order) -> None:
        if not self.auth.is_verified():
            raise Exception('Payment not authorized')
        print('security code for payment is: {}'.format(self.security_code))
        print('Order has been paid in debit')
        order.status = 'paid'

class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code: str) -> None:
        self.security_code = security_code

    def pay(self, order: Order) -> None:
        print('security code for payment is: {}'.format(self.security_code))
        print('Order has been paid in credit')
        order.status = 'paid'

class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email: str, auth: SMS_Auth) -> None:
        self.email = email
        self.auth = auth

    def pay(self, order: Order) -> None:
        if not self.auth.is_verified():
            raise Exception('Payment not authorized')
        print('security code for payment is: {}'.format(self.email))
        print('Order has been paid in paypal')
        order.status = 'paid'
```

Composition makes everything simple, child classes can inherit from only one parent class (`PaymentProcessor`). We dont need to override methods (`auth`) in child classes, and everything is handled in the constructor of the child class.
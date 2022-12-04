# Dependency Inversion

A class is to depend on abstraction, not on concrete subclasses.

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

There is a slight problem with this code. The `DebitPaymentProcessor` and `PaypalPaymentProcessor` classes are directly dependent on `SMS_Auth` class, which breaks dependency inversion principle. Because if we want to add another authorization functionality then it would not work with this subclass.

We can fix this by creating an authorization interface and passing that to every function instead of concrete subclasses.

```python
class Authorizer(ABC):
    @abstractmethod
    def is_verified(self) -> bool:
        pass

class NotARobot(Authorizer):
    verified = False
    def not_a_robot(self):
        print(f'not a robot...')
        self.verified = True

    def is_verified(self) -> bool:
        return self.verified

class SMS_Auth(Authorizer):
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
    def __init__(self, security_code: str, auth: Authorizer) -> None:
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
    def __init__(self, email: str, auth: Authorizer) -> None:
        self.email = email
        self.auth = auth

    def pay(self, order: Order) -> None:
        if not self.auth.is_verified():
            raise Exception('Payment not authorized')
        print('security code for payment is: {}'.format(self.email))
        print('Order has been paid in paypal')
        order.status = 'paid'

if __name__ == '__main__':
    auth = NotARobot()
    make_payment = DebitPaymentProcessor('345678', auth)
    auth.not_a_robot()
    make_payment.pay(order)
```
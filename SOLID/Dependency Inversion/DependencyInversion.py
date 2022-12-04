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
    order = Order()
    order.add_item('pen', 1, 5.0)
    order.add_item('paper', 5, 10.0)

    total = order.total_price()
    print('total price: {}'.format(total))

    auth = NotARobot()
    make_payment = DebitPaymentProcessor('345678', auth)
    # auth.verify_payment('1234')
    auth.not_a_robot()
    make_payment.pay(order)
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
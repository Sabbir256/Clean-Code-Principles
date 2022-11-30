# SRP - Single Responsibility Principle
This principle indicated that, one class will have only one responsibility that aligns with that class.

```python
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

    def pay(self, type: str) -> None:
        if type == 'debit':
            print('Order has been paid in debit')
            self.status = 'paid'
        elif type == 'credit':
            print('Order has been paid in credit')
            self.status = 'paid'

order = Order()
order.add_item('pen', 1, 5.0)
order.add_item('paper', 5, 10.0)

total = order.total_price()
print('total price: {}'.format(total))

order.pay('credit')
```

If we notice this class then we will find that, the ```Order``` class contains ```pay()``` method which is not suppossed to be there, and it breaks the single responsibility principle. We can solve this by removing this method from the above class and creating a seperate class for anything related to payment.

# Solution

```python
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

class PaymentProcessor:
    def pay_debit(self, order: Order) -> None:
        print('Order has been paid in debit')
        order.status = 'paid'

    def pay_credit(self, order: Order) -> None:
        print('Order has been paid in credit')
        order.status = 'paid'

order = Order()
order.add_item('pen', 1, 5.0)
order.add_item('paper', 5, 10.0)

total = order.total_price()
print('total price: {}'.format(total))

make_payment = PaymentProcessor()
make_payment.pay_credit(order)
```

From above we can see that each class contains only the methods that they are supposed to. This way each class maintains SRP.
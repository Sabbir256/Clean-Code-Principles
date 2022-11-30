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
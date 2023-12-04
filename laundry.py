from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

# Singleton Pattern
class LaundryManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(LaundryManager, cls).__new__(cls)
            cls._instance.orders = []
            cls._instance.customers = []
        return cls._instance

    def register(self, customer):
        self._instance.customers.append(customer)
 
    def notify_all(self, message, done=False):
        for customer in self._instance.customers:
            customer.update(message, done)

# Observer Pattern
class Observer(ABC):
    @abstractmethod
    def update(self, message, done):
        pass

class Customer(Observer):
    def __init__(self, name):
        self.name = name
        self.orders = []
        self.done = False

    def update(self, message, done=False):
        print(f"Message: {message}")
        self.done = done

# Strategy Pattern
class PaymentStrategy(ABC):
    @abstractmethod
    def make_payment(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    def make_payment(self, amount):
        print(f"Paid ${amount} using a credit card.")

class CashPayment(PaymentStrategy):
    def make_payment(self, amount):
        print(f"Paid ${amount} in cash.")

# Decorator Pattern
class Order(ABC):
    @abstractmethod
    def generate_slip(self):
        pass

class BasicSlip(Order):
    def __init__(self, order):
        self._order = order

    def generate_slip(self):
        return f"Order ID: {self._order.order_id}, Customer: {self._order.customer.name}, Total Cost: ${self._order.cost}"

class SpecialSlip(Order):
    def __init__(self, order_decorator, additional_info):
        self._order_decorator = order_decorator
        self._additional_info = additional_info

    def generate_slip(self):
        base_slip = self._order_decorator.generate_slip()
        return f"{base_slip}, Additional Info: {self._additional_info}"

# Template Pattern
class Order(ABC):
    @abstractmethod
    def process_order(self):
        pass

class LaundryOrder(Order):
    def __init__(self, customer, clothes, payment_strategy):
        self.order_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.customer = customer
        self.clothes = clothes
        self.payment_strategy = payment_strategy
        self.cost = self.calculate_cost()
        self.delivery_date = datetime.now() + timedelta(days=3)

    def calculate_cost(self):
        # Calculate cost based on clothes and laundry type
        return len(self.clothes) * 5

    def process_order(self):
        self.payment_strategy.make_payment(self.cost)
        basic_slip = BasicSlip(self)
        additional_info_slip = SpecialSlip(basic_slip, "Express Service")
        slip = additional_info_slip.generate_slip()
        print(f"Transaction Successful! {slip}")
        self.customer.update(f"Your order with ID {self.order_id} is ready for delivery.", True)
        self.customer.orders.append(self)
        LaundryManager()._instance.orders.append(self)

# Iterator Pattern
class OrderIterator:
    def __init__(self, orders):
        self._orders = orders
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._orders):
            order = self._orders[self._index]
            self._index += 1
            return order
        else:
            raise StopIteration

# Comprehension Pattern
def get_orders_by_username(username):
    return [order for order in LaundryManager()._instance.orders if order.customer.name == username]

# Generator Pattern
def generate_reports(start_date, end_date):
    return (order for order in LaundryManager()._instance.orders
            if start_date <= order.delivery_date <= end_date)

# Usage example
customer1 = Customer("John Doe")
manager = LaundryManager()._instance
manager.register(customer1)

clothes_order = ["Shirt", "Pants", "Socks"]
credit_card_payment = CreditCardPayment()

# Customer places an order and makes a transaction
order1 = LaundryOrder(customer1, clothes_order, credit_card_payment)
order1.process_order()

# Manager sends a message to the customer
manager.notify_all("Laundry service won't be available today due to rain.")

# Manager views all orders and searches by username
print("All Orders:")
for order in OrderIterator(manager.orders):
    print(order.order_id, order.customer.name, order.delivery_date)

print("\nOrders by Username:")
for order in get_orders_by_username("John Doe"):
    print(order.order_id, order.delivery_date)

# Manager generates reports for the last week
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
print("\nReports for the Last Week:")
for order in generate_reports(start_date, end_date):
    print(order.order_id, order.delivery_date)

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict
import pickle

class Message:
    def __init__(self, message, username = 'All') -> None:
        self.username = username
        self.message = message
        self.date = datetime.now()
        
    def __repr__(self) -> str:
        return f"\nUsername: {self.username}\nMessage: {self.message}\nTime: {self.date}"
    
def save_user(user):
    with open('users.pkl', 'ab') as file:
        pickle.dump(user, file)
        
def save_all_users(ls):
    with open('users.pkl', 'wb') as file:
        for user in ls:
            pickle.dump(user, file)

def load_users():
    try:
        with open('users.pkl', 'rb') as file:
            users = []
            while True:
                try:
                    user = pickle.load(file)
                    users.append(user)
                except EOFError:
                    break
    except FileNotFoundError:
        users = []
    return users

names = []
def update_all(message):
        global names
        new_ls = []
        try:
            with open('users.pkl', 'rb') as file:
                while True:
                    try:
                        u = pickle.load(file)
                        names.append(u.username)
                        u.messages.append(message)
                        new_ls.append(u)
                    except EOFError:
                        break
        except FileNotFoundError:
            pass    
        save_all_users(new_ls)
        
# Singleton Pattern
class LaundryManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(LaundryManager, cls).__new__(cls)
            cls._instance.pending_orders = []
            cls._instance.orders = []
            cls._instance.customers = []
            cls._instance.cloth_prices = {"Shirt": 7, "Tshirt": 5, "Pant": 20, "Bedsheet": 40}
        return cls._instance

    def add_order(self, order):
        with open('orders.pkl', 'ab') as file:
            pickle.dump(order, file)
        
    def get_all_orders(self):
        try:
            with open('orders.pkl', 'rb') as file:
                orders = []
                while True:
                    try:
                        order = pickle.load(file)
                        orders.append(order)
                    except EOFError:
                        break
        except FileNotFoundError:
            orders = []
        return orders
        
    def get_all_orders_by_username(self, name):
        try:
            with open('orders.pkl', 'rb') as file:
                orders = []
                while True:
                    try:
                        order = pickle.load(file)
                        if order.customer.username == name:
                            orders.append(order)
                    except EOFError:
                        break
        except FileNotFoundError:
            orders = []
        return orders
    
    def register(self, customer):
        self._instance.customers.append(customer)
        save_user(customer)

    def notify_all(self, message):
        update_all(message)

    def notify(self, customer, message):
        customer.update(message)

# Observer Pattern
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class Customer(Observer):
    def __init__(self, username, password, address, phone):
        self.username = username
        self.password = password
        self.address = address
        self.phone = phone
        self.messages = []
        self.pending_orders = []
        self.orders = []
    
    def update(self, message):
        new_ls = []
        try:
            with open('users.pkl', 'rb') as file:
                while True:
                    try:
                        u = pickle.load(file)
                        if self.username == u.username:
                            u.messages.append(message)
                        new_ls.append(u)
                    except EOFError:
                        break
        except FileNotFoundError:
            pass    
        save_all_users(new_ls)
    
    
    def __repr__(self) -> str:
        return f"\nUsername: {self.username}\nPassword: {self.password}\nAddress: {self.address}\nPhone: {self.phone}\nMessages:{self.messages}"

# Strategy Pattern
class PaymentStrategy(ABC):
    @abstractmethod
    def make_payment(self, amount):
        pass

class UPIPayment(PaymentStrategy):
    def make_payment(self, amount):
        print(f"Paid ${amount} using a UPI.")

class CashPayment(PaymentStrategy):
    def make_payment(self, amount):
        print(f"Paid ${amount} in cash.")

# Template Pattern
class Order(ABC):
    @abstractmethod
    def process_order(self):
        pass

    @abstractmethod
    def generate_slip(self):
        pass

class LaundryOrder(Order):
    def __init__(self, order_data: Dict, payment_strategy):
        self.customer = order_data.get('username')
        self.cloth_orders = {
            'Shirt': order_data.get('Shirt', (0, '')),
            'Tshirt': order_data.get('Tshirt', (0, '')),
            'Pant': order_data.get('Pant', (0, '')),
            'Bedsheet': order_data.get('Bedsheet', (0, ''))
        }
        ls = []
        for k in self.cloth_orders:
            if self.cloth_orders[k][0] == 0:
                ls.append(k)
        
        for i in ls:
            del self.cloth_orders[i]
                
        self.payment_strategy = payment_strategy
        self.cost = self.calculate_cost()
        self.order_date = order_data['order_date']
        self.delivery_date = order_data['delivery_date']
        self.process_order()

    def calculate_cost(self):
        # Calculate cost based on cloth types and their prices
        total_cost = sum(count * LaundryManager()._instance.cloth_prices.get(cloth, 0) for cloth, (count, _) in self.cloth_orders.items())
        return total_cost

    def process_order(self):
        self.payment_strategy.make_payment(self.cost)
        slip = self.generate_slip()
        print(f"Transaction Successful! {slip}")
        self.customer.orders.append(self)
        LaundryManager().add_order(self)

    def generate_slip(self):
        cloth_details = "\n".join(f"{cloth}: {count * LaundryManager()._instance.cloth_prices.get(cloth, 0)} rupees" for cloth, (count, _) in self.cloth_orders.items())
        return f"\nUsername: {self.customer}\nClothes:\n{self.cloth_orders}\nCost: {self.cost}\n"

    def __repr__(self):
        return f"\n{self.customer}\nClothes:\n{self.cloth_orders}\nCost: {self.cost}\nOrder_date: {self.order_date}\nDelivery_date: {self.delivery_date}"

# if __name__ == '__main__':
#     # Create a LaundryManager instance
#     laundry_manager = LaundryManager()

#     # Create some customers
#     customer1 = Customer(username="Mathavaroopan", password="passPass123", address="123 Main St", phone="1234567890")
#     customer2 = Customer(username="Mathesh", password="passPass321", address="456 Oak St", phone="0987654321")

#     # Register customers with the LaundryManager
#     laundry_manager.register(customer1)
#     laundry_manager.register(customer2)

#     # Create a UPI payment strategy
#     upi_payment = UPIPayment()

#     mathavaroopan = None
#     mathesh = None
#     for user in load_users():
#         if user.username == 'Mathavaroopan':
#             mathavaroopan = user
#         if user.username == 'Mathesh':
#             mathesh = user
            
#     # Create a laundry order for Mathavaroopan
#     order_data_mathavaroopan = {'username': mathavaroopan, 'Shirt': (2, 'Blue'), 'Tshirt': (3, 'Red'),
#                                 'order_date': datetime.now(), 'delivery_date': datetime.now() + timedelta(days=3)}
#     order_mathavaroopan = LaundryOrder(order_data_mathavaroopan, upi_payment)

#     # Create a Cash payment strategy
#     cash_payment = CashPayment()

#     # Create a laundry order for Mathesh
#     order_data_mathesh = {'username': mathesh, 'Pant': (1, 'Black'), 'Bedsheet': (2, 'White'),
#                         'order_date': datetime.now(), 'delivery_date': datetime.now() + timedelta(days=2)}
#     order_mathesh = LaundryOrder(order_data_mathesh, cash_payment)

#     # Display all orders for Mathavaroopan
#     mathavaroopan_orders = laundry_manager.get_all_orders_by_username("Mathavaroopan")
#     print("Mathavaroopan's Orders:")
#     for order in mathavaroopan_orders:
#         print(order)

#     # Display all orders for Mathesh
#     mathesh_orders = laundry_manager.get_all_orders_by_username("Mathesh")
#     print("\nMathesh's Orders:")
#     for order in mathesh_orders:
#         print(order)

#     # Notify all customers with a message
#     message = Message("Laundry processing is complete!")
#     laundry_manager.notify_all(message)

#     for user in load_users():
#         print(f"{user.username}\n{user.messages}" )




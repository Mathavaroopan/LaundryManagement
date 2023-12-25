from flask import Flask, render_template, redirect, url_for, request
import pickle
from laundry import Customer, LaundryManager
import re

app = Flask(__name__)

def save_user(user):
    with open('users.pkl', 'ab') as file:
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

username = None


@app.route('/')
def login():
    return render_template('userlogin.html')

@app.route('/user_login', methods=['POST'])
def user_login():
    global username
    username = request.form['username']
    password = request.form['password']
    print(f'Login - Username: {username}, Password: {password}')
    
    for user in load_users():
        if user.username == username and user.password == password:
            user_orders = []
            try:
                with open('orders.pkl', 'rb') as file:
                    while True:
                        try:
                            order = pickle.load(file)
                            if order.customer.username == username and order.delivery_date == None:
                                user_orders.append(order)
                        except EOFError:
                            break
            except FileNotFoundError:
                pass
               
            return render_template('u_current_orders.html', user_orders = user_orders)
    
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('user_signup.html', error = False)

@app.route('/user_signup', methods=['POST'])
def user_signup():
    global username
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    phone = request.form['phone']

    # Simple regex patterns for username, password, and phone
    username_pattern = r'^[a-zA-Z0-9_]{3,20}$'
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
    phone_pattern = r'^\d{10}$'

    # Validate username
    if not re.match(username_pattern, username):
        return render_template('user_signup.html', error= True)

    # Validate password
    if not re.match(password_pattern, password):
        return render_template('user_signup.html', error=True)

    # Validate phone
    if not re.match(phone_pattern, phone):
        return render_template('user_signup.html', error=True)

    new_user = Customer(username, password, address, phone)

    LaundryManager().register(new_user)
                
    return render_template('u_current_orders.html', user_orders=[])


@app.route('/u_pending_orders', methods=['GET', 'POST'])
def u_pending_orders():
    global username
    user_orders = []
    try:
        with open('orders.pkl', 'rb') as file:
            while True:
                try:
                    order = pickle.load(file)
                    if order.delivery_date == None and order.customer.username == username:
                        user_orders.append(order)
                except EOFError:
                    break
    except FileNotFoundError:
        pass
    return render_template('u_current_orders.html', user_orders = user_orders)

@app.route('/u_delivered_orders', methods=['GET', 'POST'])
def u_delivered_orders():
    global username
    user_orders = []
    try:
        with open('orders.pkl', 'rb') as file:
            while True:
                try:
                    order = pickle.load(file)
                    if order.delivery_date is not None and order.customer.username == username:
                        user_orders.append(order)
                except EOFError:
                    break
    except FileNotFoundError:
        pass
    return render_template('u_delivered_orders.html', user_orders = user_orders)

@app.route('/u_notification', methods=['GET', 'POST'])
def u_notification():
    global username
    notifications = []
    for user in load_users():
        if user.username == username:
            notifications = user.messages
            print(user.messages)
            break
    return render_template('u_notification.html', notifications = notifications)

if __name__ == '__main__':
    app.run(debug=True)

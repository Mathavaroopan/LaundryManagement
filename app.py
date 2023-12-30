from flask import Flask, render_template, redirect, url_for, request
import datetime
import pickle
from laundry import Customer, LaundryManager, CashPayment, LaundryOrder, UPIPayment, Message

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

def save_all_orders(ls):
    with open('orders.pkl', 'wb') as file:
        for order in ls:
            pickle.dump(order, file)
    
@app.route('/')
def home():
    usernames = [user.username for user in load_users()]
    return render_template('website.html', usernames=usernames)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.get_json()
    lm = LaundryManager()
    u = None
    for user in load_users():
        if user.username == data['username']:
            u = user
            break
    order = {'username' : u, 'Shirt': (data['shirt']['count'], data['shirt']['laundryType']), 'Tshirt': (data['tshirt']['count'], data['tshirt']['laundryType']), 'Pant': (data['pant']['count'], data['pant']['laundryType']), 'Bedsheet': (data['bedsheet']['count'], data['bedsheet']['laundryType']), 'order_date' : datetime.datetime.now(), 'delivery_date' : None}
    payment = None
    if data['payment'] == 'cash':
        payment = CashPayment()
    else:
        payment = UPIPayment()
    
    LaundryOrder(order, payment)  
    print("Ordered") 
    return redirect(url_for('home'))

@app.route('/pending_orders', methods=['GET', 'POST'])
def pending_orders():
    user_orders = []
    try:
        with open('orders.pkl', 'rb') as file:
            while True:
                try:
                    order = pickle.load(file)
                    if order.delivery_date == None:
                        user_orders.append(order)
                except EOFError:
                    break
    except FileNotFoundError:
        pass
        
    return render_template('current_orders.html', user_orders = user_orders)
    
@app.route('/delivered_orders', methods=['GET', 'POST'])
def delivered_orders():
    user_orders = []
    try:
        with open('orders.pkl', 'rb') as file:
            while True:
                try:
                    order = pickle.load(file)
                    if order.delivery_date != None:
                        user_orders.append(order)
                except EOFError:
                    break
    except FileNotFoundError:
        pass    
        
    return render_template('delivered_orders.html', user_orders = user_orders)

@app.route('/send_notification', methods=['GET', 'POST'])
def send_notification():
    usernames = [user.username for user in load_users()]
    usernames.append('All')
    return render_template('send_notification.html', usernames=usernames)

@app.route('/handle_notification', methods=['POST'])
def handle_notification():
    data = request.get_json()
    notification_message = data.get('message', '')
    selected_username = data.get('username', '')
    lm = LaundryManager()
    user = None
    for i in load_users():
        if i.username == selected_username:
            user = i
            break
    message = Message(notification_message, selected_username)
    if selected_username == 'All':
        lm._instance.notify_all(message)
    else:
        lm._instance.notify(user, message)
    return redirect(url_for('send_notification'))

@app.route('/notification', methods=['GET', 'POST'])
def notification():
    notifications = []
    for user in load_users():
        for message in user.messages:
            status = True
            for i in notifications:
                if i.date == message.date:
                    status = False
                    break
            if status:
                notifications.append(message)
            
    return render_template('notification.html', notifications = notifications)

@app.route('/deliver', methods=['POST'])
def deliver():
    data = request.get_json()
    order_date = data.get('order_date')
    
    orders = LaundryManager()._instance.get_all_orders()
    for order in orders:
        if str(order.order_date) == order_date:
            print(str(order.order_date), " ", order_date)
            order.delivery_date = datetime.datetime.now()
    save_all_orders(orders)
    return render_template('current_orders.html', user_orders = orders)


@app.route('/get_report/<report_type>')
def get_report(report_type):
    laundry_manager = LaundryManager()
    
    if report_type == 'daily':
        # Get daily orders for today
        from datetime import datetime
        today = datetime.now().date()
        daily_orders = laundry_manager.get_daily_orders(today)
        return render_template('report.html', user_orders=daily_orders)
    elif report_type == 'monthly':
        from datetime import datetime
        current_year = datetime.now().year
        current_month = datetime.now().month
        monthly_orders = laundry_manager.get_monthly_orders(current_year, current_month)
        return render_template('report.html', user_orders=monthly_orders)
    else:
        from datetime import datetime
        current_year = datetime.now().year
        yearly_orders = laundry_manager.get_yearly_orders(current_year)
        return render_template('report.html', user_orders=yearly_orders)


print([order.order_date for order in LaundryManager()._instance.get_all_orders()])

if __name__ == '__main__':
    app.run(debug=True)

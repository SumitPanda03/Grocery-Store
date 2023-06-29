from flask import Flask, request, render_template, url_for, redirect, session
from pymongo import MongoClient
from flask_login import login_manager, UserMixin, login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
import os


app = Flask(__name__, template_folder='templates')
app.secret_key = 'ad15a082fe69aad481086b06c43001e4a347e35a28d17e3f9f0b2c35e3fafe07'
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient('mongodb://localhost:27017')
db = client['Store']
items_db = db['items']
customers_db = db['customers']
auth_db = db['auth']

# login_manager = LoginManager()
# # login_manager.login_view = 'login'
# login_manager.init_app(app)


@login_manager.user_loader
def load_user():
    return auth_db.get(auth_db['_id'])

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=["POST"])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    auth_db.insert_one({'name': name, 'email': email, 'password': generate_password_hash(password,method='sha256')})

    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user_details = auth_db.find_one({'email': email})
    if check_password_hash(user_details['password'], password):
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/catalogue')
def catalogue():
    outlet = list(items_db.find())
    return render_template('catalogue.html', outlet=outlet)


@app.route('/update_item', methods=["GET", "POST"])
def update_item():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        price = request.form.get('price')

        items_db.update_one({'_id': item_id}, {'$set': {'name': name, 'price': price}})

    return render_template('update.html')


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        new_id = request.form.get('new-item-id')
        new_name = request.form.get('new-item-name')
        new_price = request.form.get('new-item-price')
        items_db.insert_one({'_id': new_id, 'name': new_name, 'price': new_price})

    return render_template('add.html')


@app.route('/buy', methods=["GET", "POST"])
def buy():
    outlet = list(items_db.find())
    if request.method == "POST":
        item_name = request.form.get('choose-item')
        item_quantity = request.form.get('choose-quantity')
        item = items_db.find_one({'name': item_name})
        item_id = item['_id']
        item_price = item['price']
        customers_db.insert_one({'_id': item_id, 'NAME': item_name, 'PRICE': item_price, 'QUANTITY': item_quantity})
    return render_template('buy.html', outlet=outlet)


@app.route('/cart')
def cart():
    bought_items = customers_db.find({})
    item_billing = customers_db.find({})
    user_details = auth_db.find({})
    net_price = 0
    net_quantity = 0
    for i in item_billing:
        net_quantity = net_quantity + int(i['QUANTITY'])
        net_price = net_price + (int(i['PRICE']) * int(i['QUANTITY']))

    return render_template('cart.html', bought_items=bought_items, net_price=net_price, net_quantity=net_quantity,user_details=user_details)


@app.route('/reset')
def reset():
    customers_db.delete_many({})
    return redirect(url_for('index'))


@app.route('/delete_itemid', methods=["GET", "POST"])
def delete_itemid():
    if request.method == "POST":
        to_delete_itemid = request.form.get('delete-item-id')
        items_db.delete_one({'_id': to_delete_itemid})

    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)

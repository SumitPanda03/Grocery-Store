from flask import Flask, request, render_template, url_for, redirect, session, flash, make_response, jsonify, g
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__, template_folder='templates')
secret_key = "thisissecretkey"
app.config['SECRET_KEY'] = "123456789"
client = MongoClient('mongodb://localhost:27017')
db = client['Store']
items_db = db['items']
customers_db = db['customers']
auth_db = db['credentials']
blacklisted_tokens = set()


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=["POST"])
def signup_post():
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    check_username_exists = auth_db.find_one({'username': username})
    if check_username_exists:
        return "User already exists , Please Login"
    else:
        auth_db.insert_one({'name': name, 'username': username, 'email': email,
                            'password': generate_password_hash(password, method='sha256')})
        flash('You are now signed-up and can log-in', 'success')
        return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user_details = auth_db.find_one({'username': username})
    if user_details:
        if check_password_hash(user_details['password'], password):
            # time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            # token = jwt.encode(
            #     {'username': user_details['username'], 'email': user_details['email'], 'name': user_details['name'],
            #      'password': user_details['password'], 'exp': time}, app.config['SECRET_KEY'])
            token_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            token = jwt.encode({'user_id': str(user_details['_id']), 'exp': str(token_expiry)},
                               app.config['SECRET_KEY'], algorithm='HS256')
            app.logger.info(token)
            app.logger.info('PASSWORD MATCHED')
            # return token
            # return jsonify({'token': token.decode('utf-8')})
            return redirect(url_for('index'))
        else:
            app.logger.info('WRONG PASSWORD,LOGIN FAILED, TRY AGAIN')
            flash("Wrong Password, Try Again", 'error')
            return redirect(url_for('login'))
    else:
        app.logger.info("NO USER")
        flash("No User Exists, Try Again", 'error')
        return redirect(url_for('login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid token'}), 401
        token = token.split(' ')[1]
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated_function


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
    net_price = 0
    net_quantity = 0
    for i in item_billing:
        net_quantity = net_quantity + int(i['QUANTITY'])
        net_price = net_price + (int(i['PRICE']) * int(i['QUANTITY']))

    return render_template('cart.html', bought_items=bought_items, net_price=net_price, net_quantity=net_quantity)


@app.route('/logout')
def logout():
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

from flask import Flask, request, render_template, url_for, redirect, session, flash, jsonify, g
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import jwt
from flask_cors import CORS
from flasgger import Swagger, swag_from
from config.swagger import template, swagger_config
from functools import wraps
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token

#APP SETUP
app = Flask(__name__, template_folder='templates')
CORS(app)
secret_key = "thisissecretkey"
app.config['SECRET_KEY'] = "123456789"
client = MongoClient('mongodb://localhost:27017')
db = client['Store']
items_db = db['items']
customers_db = db['customers']
auth_db = db['credentials']
JWTManager(app)
blacklisted_tokens = set()
SWAGGER = {
    'title': "Store API",
    'uiversion': 5
}
Swagger(app, config=swagger_config, template=template)

#CORS DATA
@app.route('/options_req', methods=["OPTIONS"])
@swag_from('./docs/options.yaml')
def options_req():
    response_headers = {
        'Allow': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    print('Returns CORS data')
    
    return jsonify(response_headers), 200, response_headers

#SIGNUP PAGE
@app.route('/signup')
@swag_from('./docs/signup.yaml')
def signup():
    print('Renders SignUp Page on site')
    return render_template('signup.html')

#SIGNUP PROCESS
@app.route('/signup', methods=["POST"])
@swag_from('./docs/signup.yaml')
def signup_post():
    print('Takes user input for signup')
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    check_username_exists = auth_db.find_one({'username': username})
    if check_username_exists:
        return "User already exists , Please Login"
    else:
        print('Stores signup information in auth database')
        auth_db.insert_one({'name': name, 'username': username, 'email': email,
                            'password': generate_password_hash(password, method='sha256')}) #HASHING THE PASSWORD
        flash('You are now signed-up and can log-in', 'success')
        return redirect(url_for('login'))

#LOGIN PAGE
@app.route('/login')
@swag_from('./docs/login.yaml')
def login():
    print('Renders Login Page on site')
    return render_template('login.html')

# MY JWT AUTHENTICATION WITHOUT FLASK-JWT LIBRARY
'''
@app.route('/login', methods=["POST"])
@swag_from('./docs/login.yaml')
def login_post():
    print('Takes user input for login')
    username = request.form.get('username')
    password = request.form.get('password')
    user_details = auth_db.find_one({'username': username})
    if user_details:
        print('Verifying user details for login')
        if check_password_hash(user_details['password'], password):
            # time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            # token = jwt.encode(
            #     {'username': user_details['username'], 'email': user_details['email'], 'name': user_details['name'],
            #      'password': user_details['password'], 'exp': time}, app.config['SECRET_KEY'])
            token_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            token = jwt.encode({'user_id': str(user_details['_id']), 'exp': str(token_expiry)},
                               app.config['SECRET_KEY'], algorithm='HS256')
            print(token)
            print('PASSWORD MATCHED')
            # return jsonify({'token': token})
            # return jsonify({'token': token.decode('utf-8')})
            # return render_template('layout.html',token=token)
            return redirect(url_for('index'))
        else:
            print('WRONG PASSWORD,LOGIN FAILED, TRY AGAIN')
            flash("Wrong Password, Try Again", 'error')
            return redirect(url_for('login'))
    else:
        print("NO USER")
        flash("No User Exists, Try Again", 'error')
        return redirect(url_for('login'))
'''

#LOGIN PROCESS
@app.route('/login', methods=["POST"])
@swag_from('./docs/login.yaml')
def login_post():
    print('Takes user input for login')
    username = request.form.get('username')
    password = request.form.get('password')
    user_details = auth_db.find_one({'username': username})
    if user_details:
        print('Verifying user details for login')
        if check_password_hash(user_details['password'], password):
            refresh = create_refresh_token(identity=username)
            access = create_access_token(identity=username)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': username,
                    'email': user_details['email']
                }
            })
            # app.logger.info(username,user_details['email'],refresh,access)
            # print(f"'refresh': {refresh},'access': {access},'username': {username},'email': {user_details['email']}")
            # return redirect(url_for('catalogue'))
        else:
            print('WRONG PASSWORD,LOGIN FAILED, TRY AGAIN')
            flash("Wrong Password, Try Again", 'error')
            return redirect(url_for('login'))
    else:
        print("NO USER")
        flash("No User Exists, Try Again", 'error')
        return redirect(url_for('login'))
    
#USING DECORATORS TO IMPLEMENT AUTHENTICATION - TRY
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

#ADDING DATA TO DATABASE OF STORE
def preload_data():
    if items_db.count_documents({}) > 0:
        print("Data already pre-loaded. Skipping insertion.")
        return

    items = [
        {"_id": "A1KG", "name": "Apple", "price": "80"},
        {"_id": "S1GM", "name": "Soya", "price": "60"},
        {"_id": "R1KG", "name": "Rice", "price": 60},
        {"_id": "F2KG", "name": "Flour", "price": 40},
        {"_id": "T4PK", "name": "Tea", "price": 80},
        {"_id": "C5GM", "name": "Cumin Seeds", "price": 120},
        {"_id": "T6PK", "name": "Turmeric Powder", "price": 55},
        {"_id": "M7LT", "name": "Mustard Oil", "price": 150},
        {"_id": "B8KG", "name": "Bengal Gram Split", "price": 90},
        {"_id": "C9GM", "name": "Cardamom", "price": 300},
        {"_id": "C1LT", "name": "Cooking Oil", "price": 120},
        {"_id": "S2KG", "name": "Salt", "price": 20},
        {"_id": "C3GM", "name": "Coriander Powder", "price": 40},
        {"_id": "T4KG", "name": "Tomato", "price": 25},
        {"_id": "P5KG", "name": "Potato", "price": 30},
        {"_id": "O6KG", "name": "Onion", "price": 35},
        {"_id": "S2GM", "name": "Soap", "price": "60"},
        {"_id": "B7KG", "name": "Beef", "price": "180"},
        {"_id": "N4GM", "name": "Noodles", "price": "80"}
    ]

    items_db.insert_many(items)
    print("Data pre-loaded successfully.")

#Verification testing of jwt token, paste the token recieved in the bearer token of POSTMAN
@app.route('/verify', methods=["GET"])
@swag_from('./docs/verify.yaml')
@jwt_required()
def verify():
    return jsonify({"message":"User logged in and verified using jwt access token"})


#HOME PAGE
@app.route('/')
def index():
    print('Renders Home page on server')
    return render_template('layout.html')

#ABOUT PAGE
@app.route('/about')
@swag_from('./docs/about.yaml')
def about():
    print('Renders About page on server')
    return render_template('about.html')

#CATALOGUE OF STORE
@app.route('/catalogue')
@swag_from('./docs/catalogue.yaml')
def catalogue():
    outlet = list(items_db.find())
    print('Renders Catalogue page on server with all items displayed from items Database')
    return render_template('catalogue.html', outlet=outlet)

#UPDATE ITEMS OF STORE FROM DATABASE -- PUT METHOD
@app.route('/update_item', methods=["GET", "POST", "PUT"])
@swag_from('./docs/update.yaml')
def update_item():
    if request.method == 'POST' or 'PUT':
        print('Takes input from user from html form to update item in items database')
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        price = request.form.get('price')
        print('Updates the item details in database')
        items_db.update_one({'_id': item_id}, {'$set': {'name': name, 'price': price}})

    print('Renders Update page on server')
    return render_template('update.html')

#IMPLEMENTING PATCH METHOD FOR SELECTIVE UPDATE OF PRICE
@app.route('/items/<item_id>', methods=["PATCH"])
@swag_from('./docs/update_price.yaml')
def update_price(item_id):
    if request.method == "PATCH":
        print('Takes updated price of an item as json')
        new_price = request.json.get('new_price')

        item = items_db.find_one({'_id': item_id})
        if item:
            items_db.update_one({'_id': item_id}, {'$set': {'price': new_price}})
            print('Updates the price of item in items database')
            return jsonify({'message': 'Item price updated successfully'})
        else:
            print('Item not found')
            return jsonify({'message': 'Item not found'})

#ADD ITEMS TO DATABASE OF STORE
@app.route('/add', methods=["GET", "POST"])
@swag_from('./docs/add.yaml')
def add():
    if request.method == 'POST':
        print('Takeing data from user to add items to items Database')
        new_id = request.form.get('new-item-id')
        new_name = request.form.get('new-item-name')
        new_price = request.form.get('new-item-price')
        print('Inserting data to database')
        items_db.insert_one({'_id': new_id, 'name': new_name, 'price': new_price})
    print('Renders Add Page on site')
    return render_template('add.html')

#BUYING ITEMS FROM STORE
@app.route('/buy', methods=["GET", "POST"])
@swag_from('./docs/buy.yaml')
def buy():
    outlet = list(items_db.find())
    if request.method == "POST":
        print('Taking data from user to buy items')
        item_name = request.form.get('choose-item')
        item_quantity = request.form.get('choose-quantity')
        item = items_db.find_one({'name': item_name})
        item_id = item['_id']
        item_price = item['price']
        print('Inserting bought items into customers Database')
        customers_db.insert_one({'_id': item_id, 'NAME': item_name, 'PRICE': item_price, 'QUANTITY': item_quantity})
    print('Renders Buy Page on site')
    return render_template('buy.html', outlet=outlet)

#GENERATES A CART FOR THE BOUGHT ITEMS
@app.route('/cart')
@swag_from('./docs/cart.yaml')
def cart():
    print('Calculated Price and Quantity')
    bought_items = customers_db.find({})
    item_billing = customers_db.find({})
    net_price = 0
    net_quantity = 0
    for i in item_billing:
        net_quantity = net_quantity + int(i['QUANTITY'])
        net_price = net_price + (int(i['PRICE']) * int(i['QUANTITY']))
    print('Renders Cart page on client')  
    return render_template('cart.html', bought_items=bought_items, net_price=net_price, net_quantity=net_quantity)

#LOGOUT FEATURE -- CLEARS THE CART FOR THAT PARTICULAR USER
@app.route('/logout')
@swag_from('./docs/logout.yaml')
def logout():
    print('Logs out user and clears cart for that user')
    customers_db.delete_many({})
    return redirect(url_for('index'))

#DELETES A SPECIFIC ITEM FROM DATABASE
@app.route('/delete_itemid', methods=["GET", "POST", "DELETE"])
@swag_from('./docs/delete.yaml')
def delete_itemid():
    if request.method == "POST" or "DELETE":
        print('Takes user input of ID to delete item')
        to_delete_itemid = request.form.get('delete-item-id')
        print('Deletes item from items database')
        items_db.delete_one({'_id': to_delete_itemid})

    return render_template('delete.html')

#RUNNING THE APP
if __name__ == '__main__':
    preload_data()
    print('Started Server')
    app.run()

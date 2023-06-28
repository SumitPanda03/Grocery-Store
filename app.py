from flask import Flask, request, render_template, url_for, redirect
from pymongo import MongoClient


app = Flask(__name__, template_folder='templates')
client = MongoClient('mongodb://localhost:27017')
db = client['Store']
items_db= db['items']
customers_db = db['customers']


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

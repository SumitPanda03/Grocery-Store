from flask import Flask, request, jsonify, json, render_template, url_for, redirect
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='templates')
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/Store'
# mongo = PyMongo(app)
# items = mongo.db.items
# user = mongo.db.user
client = MongoClient('mongodb://localhost:27017')
db = client['Store']
collection = db['items']


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/about')
def about():
    return render_template(('about.html'))


'''
@app.route('/all_items', methods=["GET"])
def all_items():
    outlet = list(collection.find())
    # return dumps(outlet)
    return render_template('layout.html', outlet=outlet)
'''


@app.route('/catalogue')
def catalogue():
    outlet = list(collection.find())
    # return dumps(outlet)
    return render_template('catalogue.html', outlet=outlet)


@app.route('/update_item', methods=["GET", "POST"])
def update_item():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        price = request.form.get('price')

        collection.update_one({'_id': item_id}, {'$set': {'name': name, 'price': price}})

    return render_template('update.html')


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        new_id = request.form.get('new-item-id')
        new_name = request.form.get('new-item-name')
        new_price = request.form.get('new-item-price')
        collection.insert_one({'_id': new_id, 'name': new_name, 'price': new_price})

    return render_template('add.html')
    # return redirect((url_for('catalogue')))


@app.route('/reset')
def reset():
    collection.delete_many({})
    return redirect(url_for('index'))


@app.route('/delete_itemid', methods=["GET", "POST"])
def delete_itemid():
    if request.method == "POST":
        to_delete_itemid = request.form.get('delete-item-id')
        collection.delete_one({'_id': to_delete_itemid})

    # return redirect(url_for('all_items'))
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)

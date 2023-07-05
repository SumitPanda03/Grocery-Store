@app.route('/items/<item_id>', methods=["PATCH"])
def update_price(item_id):
    if request.method == "PATCH":
        new_price = request.json.get('new_price')

        item = items_db.find_one({'_id': item_id})
        if item:
            items_db.update_one({'_id': item_id}, {'$set': {'price': new_price}})
            return jsonify({'message': 'Item price updated successfully'})
        else:
            return jsonify({'message': 'Item not found'})
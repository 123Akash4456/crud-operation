from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__,template_folder='template')

# Connect to the MongoDB database
client = MongoClient('mongodb+srv://neil:1234@cluster0.udfwo2s.mongodb.net/')
db = client['Test']
collection = db['Test']

@app.route('/')
def list_items():
    items = collection.find()
    return render_template('list.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        name = request.form.get('name')
        collection.insert_one({'name': name})
        return redirect('/')
    return render_template('create.html')

@app.route('/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = collection.find_one({'_id': (item_id)})
    if request.method == 'POST':
        new_name = request.form.get('name')
        collection.update_one({'_id': (item_id)}, {'$set': {'name': new_name}})
        return redirect('/')
    return render_template('edit.html', item=item)

@app.route('/delete/<item_id>')
def delete_item(item_id):
    collection.delete_one({'_id':(item_id)})
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)
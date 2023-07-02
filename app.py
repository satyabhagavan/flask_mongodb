from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
mongodb_uri = 'mongodb+srv://satya:satya@cluster0.eb3co.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(mongodb_uri)
db = client['information']

@app.route('/')
def hello():
    return render_template('welcome.html')

@app.route("/data", methods=['GET'])
def get_data():
    data = db['data']

    try:
        items = []
        for item in data.find({}, {}):
            items.append(item)
            
        return json_util.dumps({'tasks': items, "message": "data retrived"}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route("/details", methods=['GET'])
def display_details():
    data = db['data']

    try:
        items = []
        for item in data.find({}, {}):
            items.append(item)
            
        return render_template('Details.html', data=items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route("/submit", methods=['POST'])
def store_data():
    
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'error': 'Empty request body'}), 400

    info = db['data']

    try:
        info.insert_one({'first_name': data['first_name'], 'last_name': data['last_name'], 'email': data['email'], 'university': data['university'],  'phone_number': data['phone_number']})
    except Exception as e:
        print(e)
        return jsonify({'error': 'error in creating task'}), 400

    return jsonify({'message': 'data insertion successful'}), 201

if __name__ == '__main__':
    app.run()


#asking because if that's so the task is straight forward right so just want to be clear thanks
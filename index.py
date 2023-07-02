from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
# mongodb_uri = "please passs the mongodb database url"
mongodb_uri = 'mongodb+srv://satya:satya@cluster0.eb3co.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(mongodb_uri)
db = client['tasks']


@app.route("/tasks", methods=['GET'])
def get_tasks():
    tasks = db['tasks']

    try:
        items = []
        for item in tasks.find({}, {"_id": 1, "name": 1, "status": 1}):
            items.append(item)
            
        return json_util.dumps({'tasks': items, "message": "tasks retrived"}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create', methods=['POST'])
def create_task():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'error': 'Empty request body'}), 400

    tasks = db['tasks']
    try:
        tasks.insert_one({'name': data['task'], 'status': 'to-do'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'error in creating task'}), 400

    return 'task created'

@app.route('/taskDone', methods=['POST'])
def complete_task():
    data = request.get_json()
    print(data)
    if not data or 'id' not in data:
        return jsonify({'error': 'Empty request body or Id is needed'}), 400

    try:
        filter_condition = {'_id': ObjectId(data['id'])}
        update = {'$set': {'status': 'Done'}}
        result = db['tasks'].find_one_and_update(filter_condition, update, return_document=True)
        if result:
            return json_util.dumps({'document': result, "message": "task updated"}), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/deleteTask', methods=['DELETE'])
def delete_post():
    data = request.get_json()
    try:
        print(data["id"])
        result = db.tasks.delete_one({'_id': ObjectId(data["id"])})
        if result.deleted_count == 1:
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/editTask', methods=['POST'])
def edit_post():
    data = request.get_json()
    print(data)
    if not data or 'id' not in data:
        return jsonify({'error': 'Empty request body or Id is needed'}), 400

    try:
        filter_condition = {'_id': ObjectId(data['id'])}
        update = {'$set': {'name': data['task']}}
        result = db['tasks'].find_one_and_update(filter_condition, update, return_document=True)
        if result:
            return json_util.dumps({'document': result, "message": "task updated"}), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
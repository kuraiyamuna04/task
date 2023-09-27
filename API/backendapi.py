from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# Replace the following URL with your MongoDB connection string
app.config['MONGO_URI'] = 'mongodb://localhost:27017/knowledge_base'
mongo = PyMongo(app)

# Endpoint to store data in the database
@app.route('/knowledge_base', methods=['POST'])
def create_entry():
    data = request.get_json()
    if 'name' in data and 'class' in data and 'date_of_birth' in data:
        entry_id = mongo.db.knowledge_base.insert_one(data).inserted_id
        return jsonify({'message': 'Entry created successfully', 'id': str(entry_id)})
    else:
        return jsonify({'error': 'Missing fields (name, class, date_of_birth)'}), 400

# Endpoint to update data in the database
@app.route('/knowledge_base/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    data = request.get_json()
    result = mongo.db.knowledge_base.update_one({'_id': entry_id}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Entry updated successfully'})
    else:
        return jsonify({'error': 'Entry not found'}), 404

# Endpoint to delete data from the database
@app.route('/knowledge_base/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    result = mongo.db.knowledge_base.delete_one({'_id': entry_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Entry deleted successfully'})
    else:
        return jsonify({'error': 'Entry not found'}), 404

# Endpoint to fetch all data from the database
@app.route('/knowledge_base', methods=['GET'])
def get_all_entries():
    entries = list(mongo.db.knowledge_base.find({}, {'_id': False}))
    return jsonify(entries)

if __name__ == '__main__':
    app.run(debug=True)

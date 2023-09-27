from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Replace the following values with your MongoDB connection string and database name
mongo_uri = "mongodb://localhost:27017/"
db_name = "knowledge_base"

# Function to establish a connection to MongoDB
def get_db_connection():
    client = MongoClient(mongo_uri)
    return client[db_name]

# Create operation
@app.route('/knowledge-base', methods=['POST'])
def create_entry():
    try:
        entry = request.json['entry']
        db = get_db_connection()
        knowledge_base = db['knowledge_base']
        new_entry = {"entry": entry}
        knowledge_base.insert_one(new_entry)
        return jsonify({"message": "Entry created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Read operation
@app.route('/knowledge-base', methods=['GET'])
def get_entries():
    try:
        db = get_db_connection()
        knowledge_base = db['knowledge_base']
        entries = list(knowledge_base.find({}, {"_id": 0}))
        return jsonify(entries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update operation
@app.route('/knowledge-base/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    try:
        entry = request.json['entry']
        db = get_db_connection()
        knowledge_base = db['knowledge_base']
        knowledge_base.update_one({"id": entry_id}, {"$set": {"entry": entry}})
        return jsonify({"message": "Entry updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete operation
@app.route('/knowledge-base/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        db = get_db_connection()
        knowledge_base = db['knowledge_base']
        knowledge_base.delete_one({"id": entry_id})
        return jsonify({"message": "Entry deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

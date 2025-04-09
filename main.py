from flask import Flask, request, jsonify
from creds import MONGO_URI
from flask_pymongo import PyMongo
import time

# Save MONGO_URI in a creds.py file
app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app).cx.bookstore


@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        required_fields = ['password', 'email']
        data = request.json
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields", "required_fields": required_fields}), 400

        email = data['email']
        password = data['password']
        mongo.users.insert_one({'email': email, 'password': password})
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400
    

@app.route('/api/login', methods=['POST'])
def login():
    try:
        required_fields = ['password', 'email']
        data = request.json
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields", "required_fields": required_fields}), 400

        email = data['email']
        password = data['password']
        user = mongo.users.find_one({'email': email, 'password': password})
        if user:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True, port=15000)
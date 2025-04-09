from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from creds import MONGO_URI
from flask_pymongo import PyMongo
import secrets
import hashlib

from flask_jwt_extended import create_access_token, jwt_required, JWTManager

# Save MONGO_URI in a creds.py file
app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
app.config["JWT_SECRET_KEY"] = secrets.token_hex(16)

mongo = PyMongo(app).cx.bookstore
jwt = JWTManager(app)

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        required_fields = ['password', 'email']
        data = request.json
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields", "required_fields": required_fields}), 400

        email = data['email']
        password = data['password']
        mongo.users.insert_one({'email': email, 'password': hashlib.sha256(password.encode()).hexdigest()})
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
        user = mongo.users.find_one({'email': email, 'password': hashlib.sha256(password.encode()).hexdigest()})
        if user:
            access_token = create_access_token(identity=email)
            return jsonify({"message": "Login successful", 'access_token_type': 'Bearer', 'access_token': access_token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400

@app.route('/api/create', methods=['POST'])
@jwt_required()
def create():
    try:
        required_fields = ['title', 'author', 'category', 'price', 'rating', 'published_date', 'genre']
        data = request.json
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing fields", "required_fields": required_fields}), 400
        
        new_id = str(mongo.books.count_documents({}) + 1)

        book = {
            'id': new_id,
            'title': data['title'],
            'author': data['author'],
            'category': data['category'],
            'price': data['price'],
            'rating': data['rating'],
            'published_date': data['published_date'],
            'genre': data['genre']
        }
        mongo.books.insert_one(book)
        return jsonify({"message": "Book created successfully", "book_id": new_id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400

@app.route('/api/books', methods=['GET'])
@jwt_required()
def all_books():
    try:
        books = mongo.books.find()
        return jsonify([book for book in books]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400
    
@app.route('/api/book/<book_id>', methods=['GET'])
@jwt_required()
def get_book(book_id):
    try:
        book = mongo.books.find_one({'id': book_id})
        if book:
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400

@app.route('/api/book/<book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    book_params = ['title', 'author', 'category', 'price', 'rating', 'published_date', 'genre']
    try:
        data = request.json
        if not any(param in data for param in book_params):
            return jsonify({"error": "No fields to update"}), 400

        update_data = {param: data[param] for param in book_params if param in data}
        mongo.books.update_one({'id': book_id}, {'$set': update_data})
        return jsonify({"message": "Book updated successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400

@app.route('/api/book/<book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    try:
        mongo.books.delete_one({'id': book_id})
        return jsonify({"message": "Book deleted successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"{e}"}), 400
    

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True, port=15000)
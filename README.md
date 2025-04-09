# Bookstore REST API

A simple, secure REST API built with Flask for managing a bookstore. It supports user authentication with JWT and CRUD operations on books stored in MongoDB.

---

## Features

- **User Signup & Login** (with JWT authentication)
- **Create, Read, Update, Delete (CRUD)** operations on books
- **Secure Passwords** using SHA-256 hashing
- **JWT-Protected Endpoints**

---

## Endpoints

### Auth Routes

#### `POST /api/signup`
- **Description**: Register a new user.
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```

#### `POST /api/login`
- **Description**: Login and receive a JWT token.
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response**:
  ```json
  {
    "access_token_type": "Bearer",
    "access_token": "<JWT_TOKEN>"
  }
  ```

---

### Book Routes (Protected, require Bearer JWT token in headers)

#### `POST /api/create`
- **Description**: Add a new book.
- **Body**:
  ```json
  {
    "title": "Book Title",
    "author": "Author Name",
    "category": "Fiction",
    "price": 20.99,
    "rating": 4.5,
    "published_date": "2024-03-15",
    "genre": "Adventure"
  }
  ```

#### `GET /api/books`
- **Description**: Get all books.

#### `GET /api/book/<book_id>`
- **Description**: Get a specific book by ID.

#### `PUT /api/book/<book_id>`
- **Description**: Update details of a specific book.
- **Body**: Any combination of the following fields:
  ```json
  {
    "title": "New Title",
    "author": "New Author",
    ...
  }
  ```

#### `DELETE /api/book/<book_id>`
- **Description**: Delete a book by ID.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create & Activate a Virtual Environment (optional but recommended)
```bash
python -m venv .venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `creds.py` File
In the root directory, create a file named `creds.py` and add:

```python
MONGO_URI = "<YOUR_MONGO_DB_URI>"
```

### 5. Run the API
```bash
python main.py
```

API will start at:  
**http://localhost:15000**

---

## Dependencies (from `requirements.txt`)
Make sure your `requirements.txt` includes:
```
Flask
Flask-JWT-Extended
Flask-PyMongo
```
---
## Screenshots
![IMAGE]('images/Screenshot (156).png')
![IMAGE]('images/Screenshot (157).png')
![IMAGE]('images/Screenshot (158).png')
![IMAGE]('images/Screenshot (159).png')
![IMAGE]('images/Screenshot (160).png')
![IMAGE]('images/Screenshot (161).png')
![IMAGE]('images/Screenshot (162).png')
![IMAGE]('images/Screenshot (163).png')

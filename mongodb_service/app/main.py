import bcrypt
import dotenv
from flask import Flask, request, jsonify, session
from auth.auth import create_user, authenticate_user
from services.user_lists import (
    get_lists, add_list, delete_list,
    add_movie_to_list, remove_movie_from_list,
    rename_list, update_movie_rating
)
from services.users import (get_user_by_username, get_user_by_id, 
                            update_user, delete_user)

app = Flask(__name__)
app.secret_key = dotenv.get_key(dotenv.find_dotenv(), "SECRET_KEY")

# --- User Authentication Endpoints ---

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400
    result = create_user(username, email, password)
    if result == 1:
        return jsonify({"message": "User created"}), 201
    else:
        return jsonify({"error": "User already exists"}), 409


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    username = data.get('username')
    password = data.get('password')
    if authenticate_user(username, password):
        session['username'] = username
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"message": "Logged out"}), 200

# --- Helper: Require Login Decorator ---

from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Movie List Endpoints (require login) ---

@app.route('/lists', methods=['GET'])
@login_required
def get_user_lists():
    lists = get_lists(session['username'])
    return jsonify(lists), 200


@app.route('/lists', methods=['POST'])
@login_required
def create_list():
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    list_name = data.get('name')
    if not list_name:
        return jsonify({"error": "Missing list name"}), 400
    if add_list(session['username'], list_name):
        return jsonify({"message": "List added"}), 201
    else:
        return jsonify({"error": "Could not add list"}), 400


@app.route('/lists/<list_name>', methods=['DELETE'])
@login_required
def remove_list(list_name):
    if delete_list(session['username'], list_name):
        return jsonify({"message": "List deleted"}), 200
    else:
        return jsonify({"error": "Could not delete list"}), 400


@app.route('/lists/<list_name>/movies', methods=['POST'])
@login_required
def add_movie(list_name):
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    movie_id = data.get('movie_id')
    title = data.get('title')
    rating = data.get('rating')
    if not movie_id or not title:
        return jsonify({"error": "Missing movie_id or title"}), 400
    if add_movie_to_list(session['username'], list_name, movie_id, title, rating):
        return jsonify({"message": "Movie added"}), 201
    else:
        return jsonify({"error": "Could not add movie"}), 400


@app.route('/lists/<list_name>/movies/<movie_id>', methods=['DELETE'])
@login_required
def remove_movie(list_name, movie_id):
    if remove_movie_from_list(session['username'], list_name, movie_id):
        return jsonify({"message": "Movie removed"}), 200
    else:
        return jsonify({"error": "Could not remove movie"}), 400


@app.route('/lists/<list_name>/movies/<movie_id>/rating', methods=['PUT'])
@login_required
def update_rating(list_name, movie_id):
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    new_rating = data.get('rating')
    if new_rating is None:
        return jsonify({"error": "Missing rating"}), 400
    if update_movie_rating(session['username'], list_name, movie_id, new_rating):
        return jsonify({"message": "Rating updated"}), 200
    else:
        return jsonify({"error": "Could not update rating"}), 400


@app.route('/lists/<old_name>/rename', methods=['PUT'])
@login_required
def rename_user_list(old_name):
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    new_name = data.get('new_name')
    if not new_name:
        return jsonify({"error": "Missing new_name"}), 400
    if rename_list(session['username'], old_name, new_name):
        return jsonify({"message": "List renamed"}), 200
    else:
        return jsonify({"error": "Could not rename list"}), 400
    
@app.route('/user/<username>', methods=['GET'])
@login_required
def view_user(username):
    user = get_user_by_username(username)
    if user:
        return jsonify({
            "username": user["username"],
            "email": user["email"],
            "lists": user["lists"]
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404
@app.route('/user/id/<user_id>', methods=['GET'])
@login_required
def view_user_by_id(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify({
            "username": user["username"],
            "email": user["email"],
            "lists": user["lists"]
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404
@app.route('/user/<username>', methods=['PUT'])
@login_required
def upd_user(username):
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    update_fields = {}
    if 'email' in data:
        update_fields['email'] = data['email']
    if 'password' in data:
        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        update_fields['password'] = hashed
    if update_fields:
        result = update_user(username, update_fields)
        if result:
            return jsonify({"message": "User updated"}), 200
        else:
            return jsonify({"error": "Could not update user"}), 400
    else:
        return jsonify({"error": "No fields to update"}), 400
@app.route('/user/<username>', methods=['DELETE'])
@login_required
def del_user(username):
    result = delete_user(username)
    if result:
        session.pop('username', None)
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "Could not delete user"}), 400

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, port=8000)
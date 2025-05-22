from bson.objectid import ObjectId
import bcrypt
from pymongo import MongoClient
import dotenv

client = MongoClient(dotenv.get_key(dotenv.find_dotenv(), "MONGO_URI"))

db = client["users"]
collection = db["users"]


def create_user(username, email, password):
    """
    Create a new user in the database.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        int: 1 if user is created successfully, 0 otherwise.
    """
    if collection.find_one({"username": username}):
        print("User already exists")
        return 0
    else:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_doc = {
            "_id": str(ObjectId()),
            "username": username,
            "email": email,
            "password": hashed,
            "lists": []
        }
        collection.insert_one(user_doc)
        print("User created successfully")
        return 1


def authenticate_user(username, password):
    """Authenticate a user by checking the username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        int: 1 if authentication is successful, 0 otherwise.
    """
    user = collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return 1
    else:
        return 0


__all__ = ["collection"]

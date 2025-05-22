from bson.objectid import ObjectId
from auth.auth import collection  # Import collection from auth module


def get_user_by_username(username):
    """Retrieve a user document by username.

    Args:
        username (str): The username of the user.

    Returns:
        dict: The user document, or None if not found.
    """
    return collection.find_one({"username": username})


def get_user_by_id(user_id):
    """Retrieve a user document by MongoDB _id.

    Args:
        user_id (str): The _id of the user.

    Returns:
        dict: The user document, or None if not found.
    """
    return collection.find_one({"_id": ObjectId(user_id)})


def update_user(username, update_fields):
    """
    Update user fields.
    
    Args:
        username (str): The username of the user to update.
        update_fields (dict): Fields to update.
    
    Returns:
        dict: The updated user document, or None if not found.
    """
    result = collection.find_one_and_update(
        {"username": username},
        {"$set": update_fields},
        return_document=True
    )
    return result


def delete_user(username):
    """
    Delete a user by username.

    Args:
        username (str): The username of the user to delete.

    Returns:
        int: 1 if deleted, 0 if not found.
    """
    result = collection.delete_one({"username": username})
    return 1 if result.deleted_count > 0 else 0

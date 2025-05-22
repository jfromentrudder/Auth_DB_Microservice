from auth.auth import collection

def get_lists(username):
    """
    Retrieve all lists for a user.

    Args:
        username (str): The username of the user.

    Returns:
        list: A list of the user's lists, or an empty list if not found.
    """
    user = collection.find_one({"username": username}, {"_id": 0, "lists": 1})
    return user.get("lists", []) if user else []

def add_list(username, list_name):
    """
    Add a new list for the user.

    Args:
        username (str): The username of the user.
        list_name (str): The name of the list to add.

    Returns:
        bool: True if the list was added, False otherwise.
    """
    result = collection.update_one(
        {"username": username},
        {"$push": {"lists": {"name": list_name, "movies": []}}}
    )
    return result.modified_count > 0

def delete_list(username, list_name):
    """
    Delete a list by name for the user.

    Args:
        username (str): The username of the user.
        list_name (str): The name of the list to delete.

    Returns:
        bool: True if the list was deleted, False otherwise.
    """
    result = collection.update_one(
        {"username": username},
        {"$pull": {"lists": {"name": list_name}}}
    )
    return result.modified_count > 0

def add_movie_to_list(username, list_name, movie_id, title, rating=None):
    """
    Add a movie to a specific list.

    Args:
        username (str): The username of the user.
        list_name (str): The name of the list to add the movie to.
        movie_id (str): The ID of the movie to add.
        title (str): The title of the movie.
        rating (float, optional): The rating of the movie. Defaults to None.

    Returns:
        bool: True if the movie was added, False otherwise.
    """
    movie = {"movie_id": movie_id, "title": title}
    if rating is not None:
        movie["rating"] = rating
    result = collection.update_one(
        {"username": username, "lists.name": list_name},
        {"$push": {"lists.$.movies": movie}}
    )
    return result.modified_count > 0

def remove_movie_from_list(username, list_name, movie_id):
    """
    Remove a movie from a specific list by movie_id.

    Args:
        username (str): The username of the user.
        list_name (str): The name of the list to remove the movie from.
        movie_id (str): The ID of the movie to remove.

    Returns:
        bool: True if the movie was removed, False otherwise.
    """
    result = collection.update_one(
        {"username": username, "lists.name": list_name},
        {"$pull": {"lists.$.movies": {"movie_id": movie_id}}}
    )
    return result.modified_count > 0

def rename_list(username, old_name, new_name):
    """
    Rename a user's list.

    Args:
        username (str): The username of the user.
        old_name (str): The current name of the list.
        new_name (str): The new name for the list.

    Returns:
        bool: True if the list was renamed, False otherwise.
    """
    result = collection.update_one(
        {"username": username, "lists.name": old_name},
        {"$set": {"lists.$.name": new_name}}
    )
    return result.modified_count > 0

def update_movie_rating(username, list_name, movie_id, new_rating):
    """
    Update the rating of a movie in a specific list.

    Args:
        username (str): The username of the user.
        list_name (str): The name of the list containing the movie.
        movie_id (str): The ID of the movie to update.
        new_rating (float): The new rating for the movie.

    Returns:
        bool: True if the rating was updated, False otherwise.
    """
    result = collection.update_one(
        {"username": username, "lists.name": list_name, "lists.movies.movie_id": movie_id},
        {"$set": {"lists.$[listElem].movies.$[movieElem].rating": new_rating}},
        array_filters=[
            {"listElem.name": list_name},
            {"movieElem.movie_id": movie_id}
        ]
    )
    return result.modified_count > 0
import requests

BASE_URL = "http://localhost:8000"
session = requests.Session()

def register():
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    resp = session.post(f"{BASE_URL}/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    print(resp.json())

def login():
    username = input("Username: ")
    password = input("Password: ")
    resp = session.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })
    print(resp.json())

def logout():
    resp = session.post(f"{BASE_URL}/logout")
    print(resp.json())

def view_lists():
    resp = session.get(f"{BASE_URL}/lists")
    print(resp.json())

def create_list():
    name = input("List name: ")
    resp = session.post(f"{BASE_URL}/lists", json={"name": name})
    print(resp.json())

def rename_list():
    old_name = input("Current list name: ")
    new_name = input("New list name: ")
    resp = session.put(f"{BASE_URL}/lists/{old_name}/rename", json={"new_name": new_name})
    print(resp.json())

def delete_list():
    name = input("List name to delete: ")
    resp = session.delete(f"{BASE_URL}/lists/{name}")
    print(resp.json())

def add_movie():
    list_name = input("List name: ")
    movie_id = input("Movie ID: ")
    title = input("Movie title: ")
    rating = input("Rating (optional): ")
    data = {"movie_id": movie_id, "title": title}
    if rating:
        data["rating"] = rating
    resp = session.post(f"{BASE_URL}/lists/{list_name}/movies", json=data)
    print(resp.json())

def remove_movie():
    list_name = input("List name: ")
    movie_id = input("Movie ID: ")
    resp = session.delete(f"{BASE_URL}/lists/{list_name}/movies/{movie_id}")
    print(resp.json())

def update_rating():
    list_name = input("List name: ")
    movie_id = input("Movie ID: ")
    new_rating = input("New rating: ")
    resp = session.put(
        f"{BASE_URL}/lists/{list_name}/movies/{movie_id}/rating",
        json={"rating": new_rating}
    )
    print(resp.json())

def view_user():
    username = input("Username to view: ")
    resp = session.get(f"{BASE_URL}/user/{username}")
    print(resp.json())

def view_user_by_id():
    user_id = input("User ID to view: ")
    resp = session.get(f"{BASE_URL}/user/id/{user_id}")
    print(resp.json())

def update_user():
    username = input("Username to update: ")
    print("Leave a field blank to skip updating it.")
    new_email = input("New email: ")
    new_password = input("New password: ")
    update_fields = {}
    if new_email:
        update_fields["email"] = new_email
    if new_password:
        update_fields["password"] = new_password
    if not update_fields:
        print("No fields to update.")
        return
    resp = session.put(f"{BASE_URL}/user/{username}", json=update_fields)
    print(resp.json())

def delete_user():
    username = input("Username to delete: ")
    resp = session.delete(f"{BASE_URL}/user/{username}")
    print(resp.json())

def main():
    actions = {
        "register": register,
        "login": login,
        "logout": logout,
        "view_lists": view_lists,
        "create_list": create_list,
        "rename_list": rename_list,
        "delete_list": delete_list,
        "add_movie": add_movie,
        "remove_movie": remove_movie,
        "update_rating": update_rating,
        "view_user": view_user,
        "view_user_by_id": view_user_by_id,
        "update_user": update_user,
        "delete_user": delete_user,
        "quit": exit
    }
    print("Welcome to the Movie List Tracker CLI!")
    print("Available commands:", ", ".join(actions.keys()))
    while True:
        cmd = input("\nEnter command: ").strip()
        if cmd in actions:
            actions[cmd]()
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
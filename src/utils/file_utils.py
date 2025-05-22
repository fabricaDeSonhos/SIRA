import json, os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

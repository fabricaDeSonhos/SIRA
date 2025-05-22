from src.utils.file_utils import load_users, save_users
import uuid, bcrypt

def create_user(name, email, password):
    users = load_users()
    if any(user["email"] == email for user in users):
        return {"success": False, "error": "Email já cadastrado!"}, 400

    new_user = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "ativo": 1
    }
    users.append(new_user)
    save_users(users)
    return {"success": True, "user_id": new_user["id"]}, 201

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import bcrypt
from utils.json_manager import ler_json, escrever_json

app = Flask(__name__)
CORS(app, supports_credentials=True)

USERS_FILE = "users.json"

# Rota de cadastro
@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ["name", "email", "password"]

    if not all(field in data for field in required_fields):
        return jsonify({"success": False, "error": "Campos obrigatórios faltando!"}), 400

    users = ler_json(USERS_FILE)
    if any(user["email"] == data["email"] for user in users):
        return jsonify({"success": False, "error": "Email já cadastrado!"}), 400

    new_user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "email": data["email"],
        "password": bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        "ativo": 1
    }

    users.append(new_user)
    escrever_json(USERS_FILE, users)

    return jsonify({"success": True, "user_id": new_user["id"]}), 201

# Rota de teste para listar usuários
@app.route("/auth/users", methods=["GET"])
def list_users():
    return jsonify(ler_json(USERS_FILE)), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)

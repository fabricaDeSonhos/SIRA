from flask import Blueprint, request, jsonify
from src.services.user_service import create_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    for field in ["name", "email", "password"]:
        if not data.get(field):
            return jsonify({"success": False, "error": "Campos obrigatórios faltando!"}), 400

    response, status = create_user(data["name"], data["email"], data["password"])
    return jsonify(response), status

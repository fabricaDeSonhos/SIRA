import json
import os
from models.user import User, Admin

# Caminho absoluto para o arquivo JSON na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_JSON_PATH = r"C:\Users\gabri\OneDrive\codigos\desenvolvimentoWeb\padrõres2\users.json"


def carregar_usuarios():
    if not os.path.exists(USERS_JSON_PATH):
        return []
    with open(USERS_JSON_PATH, "r") as f:
        try:
            dados = json.load(f)
        except json.JSONDecodeError:
            return []
        usuarios = []
        for d in dados:
            if d["tipo"] == "admin":
                usuarios.append(Admin.from_dict(d))
            else:
                usuarios.append(User.from_dict(d))
        return usuarios

def salvar_usuario(usuario):
    usuarios = carregar_usuarios()
    usuarios.append(usuario)
    with open(USERS_JSON_PATH, "w") as f:
        json.dump([u.to_dict() for u in usuarios], f, indent=4)

def usuario_existe(email, lista_usuarios):
    return any(u["email"] == email for u in lista_usuarios)


def gerar_novo_id(lista_usuarios):
    if not lista_usuarios:
        return 1
    return max(u.id for u in lista_usuarios) + 1

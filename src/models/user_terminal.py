# File: src/models/user_terminal.py

import os
import sys
from getpass import getpass
import hashlib

src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_dir)  

from models.user import TipoUsuario, UserFactory
from models.user_utils import usuario_existe
from utils.json_manager import ler_json, escrever_json
from models.reserva import Sala, ReservaProxy, EmailNotificador, LogReserva

USERS_JSON_PATH    = r"C:\Users\gabri\OneDrive\codigos\desenvolvimentoWeb\padrõres2\users.json"
RESERVAS_JSON_PATH = r"C:\Users\gabri\OneDrive\codigos\desenvolvimentoWeb\padrõres2\reservas.json"

logged_in_user = None  # guarda dict do JSON do usuário logado


def cadastrar_usuario_terminal():
    print("=== Cadastro de Usuário ===")
    nome  = input("Nome: ").strip()
    email = input("Email: ").strip()
    if '@' not in email:
        print("Email inválido."); return

    usuarios = ler_json(USERS_JSON_PATH)
    if usuario_existe(email, usuarios):
        print("Erro: Este email já está cadastrado."); return

    senha = getpass("Senha: ")
    tipo  = input("Tipo de usuário (admin/comum): ").strip().lower()
    if tipo not in ("admin","comum"):
        print("Tipo inválido."); return

    tipo_enum = TipoUsuario.ADMIN if tipo=="admin" else TipoUsuario.COMUM
    novo_usuario = UserFactory().criar_usuario(nome, email, senha, tipo_enum)
    usuarios.append(novo_usuario.to_dict())
    escrever_json(USERS_JSON_PATH, usuarios)
    print(f"{nome.capitalize()} cadastrado com sucesso!")

def listar_usuarios_terminal():
    usuarios = ler_json(USERS_JSON_PATH)
    if not usuarios:
        print("Nenhum usuário cadastrado."); return

    print("\n=== Lista de Usuários ===")
    for u in usuarios:
        status = "Ativo" if u.get("status", True) else "Inativo"
        print(f"ID: {u['id']} | Nome: {u['nome']} | Email: {u['email']} | Tipo: {u['tipo']} | Status: {status}")

def login_terminal():
    global logged_in_user
    print("=== Login ===")
    email = input("Email: ").strip()
    senha  = getpass("Senha: ")

    usuarios = ler_json(USERS_JSON_PATH)
    for u in usuarios:
        if u["email"].lower() == email.lower():
            # compara hash
            if u["senha"] == hashlib.sha256(senha.encode()).hexdigest():
                print(f"Bem-vindo(a), {u['nome']}!")
                logged_in_user = u
                return
            else:
                print("Senha incorreta.")
                return
    print("Usuário não encontrado.")

def listar_reservas():
    reservas = ler_json(RESERVAS_JSON_PATH)
    if not reservas:
        print("Nenhuma reserva cadastrada.")
        return

    print("\n=== Lista de Todas as Reservas ===")
    for r in reservas:
        data    = r.get("data", "[sem data]")
        hi      = r.get("hora_inicial", "[sem hi]")
        hf      = r.get("hora_final", "[sem hf]")
        sala    = r.get("sala", "[sem sala]")
        nome    = r.get("nome", "[sem nome]")
        email   = r.get("email", "[sem email]")
        materia = r.get("nome_materia", "[sem matéria]")
        ativo   = r.get("ativo", True)

        status_str = "ATIVA" if ativo else "DESATIVADA"
        print(
            f"{data} | {hi}-{hf} | Sala: {sala} | Usuário: {nome} | {email} "
            f"| Matéria: {materia} | Status: {status_str}"
        )

def fazer_reserva_terminal():
    if not logged_in_user:
        print("Você precisa fazer login primeiro."); return

    print("=== Nova Reserva ===")
    data         = input("Data (YYYY-MM-DD): ").strip()
    hi           = input("Hora inicial (HH:MM): ").strip()
    hf           = input("Hora final    (HH:MM): ").strip()
    sala_nome    = input("Sala: ").strip()
    nome_mat     = input("Nome da matéria: ").strip()

    # carrega lista de usuários cadastrados (como dicts)
    usuarios_dicts = ler_json(USERS_JSON_PATH)
    proxy = ReservaProxy(usuarios_dicts)

    sala = Sala(sala_nome)
    try:
        reserva = proxy.fazer_reserva(
            # crio temporariamente um objeto User para passar ao proxy
            UserFactory().criar_usuario(
                logged_in_user["nome"],
                logged_in_user["email"],
                logged_in_user["senha"],
                TipoUsuario(logged_in_user["tipo"])
            ),
            sala,
            data,
            hi,
            hf,
            nome_mat
        )
        reserva.adicionar_observador(EmailNotificador())
        reserva.adicionar_observador(LogReserva())

        # persiste no JSON
        todas = ler_json(RESERVAS_JSON_PATH)
        todas.append({
            "data": data,
            "hora_inicial": hi,
            "hora_final": hf,
            "nome": logged_in_user["nome"],
            "nome_materia": nome_mat,
            "email": logged_in_user["email"],
            "sala": sala_nome
        })
        escrever_json(RESERVAS_JSON_PATH, todas)

        print("Reserva realizada com sucesso!")
    except Exception as e:
        print("Erro ao fazer reserva:", e)

def menu_terminal():
    while True:
        print("\n=== Menu Geral ===")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Login")
        print("4. Listar reservas")
        print("5. Fazer reserva")
        print("0. Sair")
        op = input("Escolha: ").strip()
        if   op=="1": cadastrar_usuario_terminal()
        elif op=="2": listar_usuarios_terminal()
        elif op=="3": login_terminal()
        elif op=="4": listar_reservas()
        elif op=="5": fazer_reserva_terminal()
        elif op=="0":
            print("Saindo..."); break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_terminal()

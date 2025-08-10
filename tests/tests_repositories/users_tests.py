# tests/test_user_repository.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.models.database import Base
from src.models.user_models import User, Admin, TipoUsuario
from src.repositories.user_repository import UserRepository
from src.utils.exceptions import DuplicateEmailError

# Arquivo de banco para inspeção
DB_FILE = "tests/tests_outputs/userRepository_test.db"

@pytest.fixture(scope="session")
def engine():
    # Remove banco antigo
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print(f"\n[SETUP] removido banco antigo em {DB_FILE} (se existia).")

    eng = create_engine(f"sqlite:///{DB_FILE}", echo=False)
    Base.metadata.create_all(eng)
    print("[SETUP] tabelas criadas no banco de usuários.")
    yield eng
    print(f"\n[TEARDOWN] sessão finalizada, banco mantido em {DB_FILE}.")
    eng.dispose()

@pytest.fixture(scope="function")
def session(engine) -> Session:
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    sess = SessionLocal()
    yield sess
    sess.rollback()
    sess.close()

@pytest.fixture(autouse=True)
def patch_utils(monkeypatch):
    # Evita verificação real de email
    monkeypatch.setattr(
        'src.utils.email_verifications.verificar_email_para_cadastro',
        lambda email, db: None
    )
    # Hash padrão
    monkeypatch.setattr(
        'src.utils.hashing_senha.hash_and_validate',
        lambda pw: ("salt123", "hash123")
    )

# --- Testes de criação de usuários comuns ---

def test_create_common_user_success(session):
    repo = UserRepository(session)
    user = repo.create_user(
        name="João Comum",
        email="joao@example.com",
        password="SenhaForte!1",
        user_type=TipoUsuario.COMUM
    )
    # Verifica atributos básicos
    assert user.id is not None
    assert isinstance(user, User)
    assert not isinstance(user, Admin)
    assert user.email == "joao@example.com"
    assert user.hashed_password == "hash123"
    assert user.salt == "salt123"
    assert user.is_active is True

# --- Testes de criação de admin ---

def test_create_admin_user_success(session):
    repo = UserRepository(session)
    admin = repo.create_user(
        name="Admin",
        email="admin@example.com",
        password="SenhaAdmin!2",
        user_type=TipoUsuario.ADMIN
    )
    assert admin.id is not None
    assert isinstance(admin, Admin)
    assert admin.email == "admin@example.com"
    assert admin.hashed_password == "hash123"

# --- Teste de e-mail duplicado ---

def test_duplicate_email_raises(session):
    repo = UserRepository(session)
    # Cria primeiro usuário
    repo.create_user("A", "dup@example.com", "Senha!3")
    # Tenta criar segundo com mesmo e-mail
    with pytest.raises(DuplicateEmailError):
        repo.create_user("B", "dup@example.com", "Senha!4")

# --- Teste de senha fraca ---

def test_weak_password_raises(monkeypatch, session):
    # Faz hash lançar ValueError
    monkeypatch.setattr(
        'src.utils.hashing_senha.hash_and_validate',
        lambda pw: (_ for _ in ()).throw(ValueError("Senha fraca"))
    )
    repo = UserRepository(session)
    with pytest.raises(ValueError) as exc:
        repo.create_user("C", "c@example.com", "123")
    assert "Senha fraca" in str(exc.value)

# --- Testes de leitura e atualização ---

def test_get_and_update_and_toggle_active(session):
    repo = UserRepository(session)
    user = repo.create_user("D", "d@example.com", "Senha!5")
    # get_by_id e get_by_email
    fetched = repo.get_by_id(user.id)
    assert fetched.id == user.id
    fetched2 = repo.get_by_email(user.email)
    assert fetched2.id == user.id
    # update
    updated = repo.update_user(user, {"name": "D2"})
    assert updated.name == "D2"
    # toggle active
    off = repo.set_active_status(user, False)
    assert off.is_active is False
    on = repo.set_active_status(user, True)
    assert on.is_active is True

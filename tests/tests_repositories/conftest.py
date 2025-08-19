# tests/tests_repositories/conftest.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Importe TODOS os seus modelos aqui.
# Isso garante que a Base do SQLAlchemy conheça todas as tabelas e relacionamentos
# antes que qualquer teste seja executado, resolvendo o erro 'failed to locate a name'.
from src.models.database import Base
from src.models.user_models import User, Admin
from src.models.room_models import Room
from src.models.reserva_models import Reserva

from src.repositories.user_repository import UserRepository
from src.repositories.room_repositories import RoomRepository
from src.repositories.reserva_repositories import ReservaRepository

DB_FILE = "tests/test_outputs/repository_tests.db"

@pytest.fixture(scope="session")
def engine():
    """
    Fixture de escopo de sessão para criar o engine e as tabelas do banco de dados uma única vez.
    Garante que o diretório de saída exista.
    """
    db_dir = os.path.dirname(DB_FILE)
    os.makedirs(db_dir, exist_ok=True)
    
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    eng = create_engine(f"sqlite:///{DB_FILE}", echo=False)
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()

@pytest.fixture(scope="function")
def session(engine):
    """
    Fixture que fornece uma sessão limpa para cada teste.
    Ela cria uma transação externa que é revertida no final,
    garantindo isolamento total entre os testes.
    """
    connection = engine.connect()
    # Inicia uma transação
    transaction = connection.begin()
    
    # Cria a sessão vinculada a essa transação
    SessionLocal = sessionmaker(bind=connection, autocommit=False, autoflush=False)
    sess = SessionLocal()

    yield sess

    # No final do teste, fecha a sessão e reverte a transação
    sess.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def user_repo(session):
    """
    Fixture que cria uma instância do UserRepository para cada teste,
    já injetando a sessão do banco de dados.
    """
    return UserRepository(session)

@pytest.fixture(scope="function")
def room_repo(session):
    """
    Fixture que cria uma instância do RoomRepository para cada teste.
    """
    return RoomRepository(session)

@pytest.fixture(scope="function")
def reserva_repo(session):
    """
    Fixture que cria uma instância do ReservaRepository para cada teste.
    """
    return ReservaRepository(session)

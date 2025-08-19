# test para fazer os primeiros testes de inicialização, de modo simplificado

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import date, time


# Importe todas as peças necessárias da sua aplicação
from src.models.database import Base
from src.models.user_models import User, Admin, TipoUsuario
from src.models.room_models import Room
from src.models.reserva_models import Reserva
from src.repositories.user_repository import UserRepository
from src.repositories.room_repositories import RoomRepository
from src.repositories.reserva_repositories import ReservaRepository

# --- Fixtures do Pytest (Configuração do Teste) ---

# nome do arquivo .db onde todo mundo vai olhar depois
DB_FILE = "tests/tests_outputs/introduce_test.db"

@pytest.fixture(scope="session")
def engine():

        # Garante que o diretório de saída para o banco de dados de teste exista.
    db_dir = os.path.dirname(DB_FILE)
    os.makedirs(db_dir, exist_ok=True)

    # 1) Remove banco velho
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print(f"\n[SETUP] removido banco antigo em {DB_FILE} (se existia).")

    # 2) Cria engine SQLite físico
    eng = create_engine(f"sqlite:///{DB_FILE}", echo=False)
    Base.metadata.create_all(eng)
    print("[SETUP] todas as tabelas criadas no banco.")

    yield eng

    # 3) Ao fim da sessão, mantém o arquivo para inspeção
    print(f"\n[TEARDOWN] sessão finalizada, banco mantido em {DB_FILE}.")
    eng.dispose()

@pytest.fixture(scope="function")
def session(engine) -> Session:
    """Para cada teste, fornece uma sessão limpa."""
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    sess = SessionLocal()
    yield sess
    sess.rollback()
    sess.close()

# --- Teste de fluxo completo ---

def test_fluxo_completo_de_reserva(session: Session):
    """
    1) Cria um admin e um usuário comum.
    2) Admin cria uma sala.
    3) Usuário comum faz uma reserva nessa sala.
    4) Verifica persistência correta.
    """
    # 1) Repositórios
    user_repo   = UserRepository(session)
    room_repo   = RoomRepository(session)
    reserva_repo = ReservaRepository(session)

    # 2) Cria admin e common user
    admin = user_repo.create_user(
        name="Admin Teste",
        email="admin@teste.com",
        password="SenhaForte!23",
        user_type=TipoUsuario.ADMIN
    )
    comum = user_repo.create_user(
        name="Usuário Comum",
        email="comum@teste.com",
        password="OutraSenha!45",
        # por padrão TipoUsuario.COMUM
    )

    assert admin is not None
    assert isinstance(admin, Admin)
    assert comum is not None
    assert isinstance(comum, User) and not isinstance(comum, Admin)

    # 3) Admin cria sala
    sala = room_repo.create(
        acting_user=admin,
        room_data={
            "name": "sala-teste",
            "description": "Sala de testes",
            "capacity": 5
        }
    )
    assert sala is not None
    assert sala.name == "sala-teste"
    assert sala.is_active is True

    # 4) Usuário comum faz reserva
    hoje = date(2025, 7, 21)   # data fixa de exemplo
    inicio = time(10, 0)
    fim    = time(11, 0)

    reserva = reserva_repo.create(
        acting_user=comum,
        reserva_data={
            "reservation_date": date(2025, 7, 21),
            "start_time": time(10, 0),
            "end_time": time(11, 0),
            "subject_name": "Reunião de Teste",
            "details": "Detalhes da reunião",
            "room_id": sala.id
        }
    )
    assert reserva is not None
    assert reserva.user_id == comum.id
    assert reserva.room_id == sala.id
    assert reserva.reservation_date == hoje
    assert reserva.start_time == inicio
    assert reserva.end_time == fim

    # 5) Verifica consultas diretas ao banco
    todos_users  = session.query(User).all()
    todas_salas  = session.query(Room).all()
    todas_reservas = session.query(Reserva).all()

    assert len(todos_users) == 2,      "Deveriam existir 2 usuários"
    assert len(todas_salas) == 1,      "Deveria existir 1 sala"
    assert len(todas_reservas) == 1,   "Deveria existir 1 reserva"

    # 6) Verifica relacionamentos via ORM
    #   - sala.reservas deve conter a reserva
    assert hasattr(sala, "reservas")
    assert len(sala.reservas) == 1
    #   - comum.reservas idem, se tiver bi-direcional
    if hasattr(comum, "reservas"):
        assert len(comum.reservas) == 1

    print("\n✔ Fluxo completo de criação de usuário, sala e reserva validado.")

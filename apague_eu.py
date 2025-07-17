# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.database import Base

@pytest.fixture(scope="session")
def engine():
    # usa SQLite em memória para testes
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def tables(engine):
    # cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine, tables):
    """
    Fornece uma sessão de banco limpa a cada teste.
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

# test_user_repository.py
import pytest
import uuid

from src.repositories.user_repositories import UserRepository
from src.models.user_models import User, Admin, TipoUsuario

@pytest.fixture(autouse=True)
def patch_utils(monkeypatch):
    # evita validações externas
    monkeypatch.setattr(
        'src.utils.email_verifications.verificar_email_para_cadastro',
        lambda email, db: None
    )
    monkeypatch.setattr(
        'src.utils.hashing_sennha.hash_and_validate',
        lambda pw: ("salt", "hashed")
    )

def test_create_user_comum(db_session):
    repo = UserRepository(db_session)
    user = repo.create_user(
        name="Gabriel",
        email="gabriel@example.com",
        password="SenhaForte123",
        user_type=TipoUsuario.COMUM
    )
    assert user.id is not None
    assert isinstance(user, User)
    assert not isinstance(user, Admin)
    assert user.email == "gabriel@example.com"
    assert user.hashed_password == "hashed"
    assert user.salt == "salt"

@pytest.mark.parametrize("user_type,cls", [
    (TipoUsuario.COMUM, User),
    (TipoUsuario.ADMIN, Admin)
])
def test_create_user_tipo(db_session, user_type, cls):
    repo = UserRepository(db_session)
    user = repo.create_user(
        name="Test", email=f"test@{user_type.value}.com", password="pw123", user_type=user_type
    )
    assert isinstance(user, cls)


def test_get_and_update_and_activate(db_session):
    repo = UserRepository(db_session)
    user = repo.create_user("User", "user@x.com", "pw", TipoUsuario.COMUM)
    fetched = repo.get_by_id(user.id)
    assert fetched.id == user.id
    by_email = repo.get_by_email(user.email)
    assert by_email.id == user.id

    # update
    updated = repo.update_user(user, {"name": "NovoNome"})
    assert updated.name == "NovoNome"

    # desativar e ativar
    off = repo.set_active_status(user, False)
    assert not off.is_active
    on = repo.set_active_status(user, True)
    assert on.is_active

# test_reserva_repository.py
import pytest
import uuid
from datetime import datetime

from src.repositories.reserva_repositories import ReservaRepository
from src.models.reserva_models import Reserva
from src.models.user_models import User, TipoUsuario

class DummyPolicy:
    def can_create(self, acting_user, data):
        return True
    def can_update(self, acting_user, reserva):
        return True

@pytest.fixture(autouse=True)
def patch_policy(monkeypatch):
    monkeypatch.setattr(
        'src.repositories.reserva_repositories.ReservaPolicy',
        lambda: DummyPolicy()
    )

@pytest.fixture
def user_factory(db_session):
    # cria e retorna usuário
    user = User(name="U", email="u@x.com", hashed_password="h", salt="s")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def reserva_data():
    return {
        'room': 'A1',
        'start_time': datetime.utcnow(),
        'end_time': datetime.utcnow(),
        'is_active': True
    }


def test_create_and_get_reserva(db_session, user_factory, reserva_data):
    repo = ReservaRepository(db_session)
    reserva = repo.create(user_factory, reserva_data)
    assert reserva.id is not None
    fetched = repo.get_by_id(reserva.id)
    assert fetched.id == reserva.id


def test_list_by_user(db_session, user_factory, reserva_data):
    repo = ReservaRepository(db_session)
    # cria duas ativas e uma inativa
    r1 = repo.create(user_factory, reserva_data)
    r2 = repo.create(user_factory, reserva_data)
    r2.is_active = False
    db_session.commit()
    all_active = repo.list_by_user(user_factory.id, active_only=True)
    assert all(r.is_active for r in all_active)
    all_all = repo.list_by_user(user_factory.id, active_only=False)
    assert len(all_all) >= 2


def test_update_reserva(db_session, user_factory, reserva_data):
    repo = ReservaRepository(db_session)
    reserva = repo.create(user_factory, reserva_data)
    updated = repo.update(user_factory, reserva, {'room': 'B2'})
    assert updated.room == 'B2'

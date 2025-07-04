import os
import pytest
import uuid
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.user import UserFactory, TipoUsuario, User
from src.models.reserva import Base, ReservaProxy

DB_FILE = "test_user.db"

@pytest.fixture(scope="session")
def engine():
    # 1) Antes de tudo, apaga o arquivo velho (se existir):
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    eng = create_engine(f"sqlite:///{DB_FILE}", echo=False)

    # 2) Cria todas as tabelas uma vez só:
    Base.metadata.create_all(eng)

    yield eng

    # 3) No fim da sessão, libera conexões e mantém o arquivo para inspeção:
    eng.dispose()

@pytest.fixture(scope="session")
def session(engine):
    # vincula a mesma sessão a todos os testes
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()

def test_criacao_user_comum(session):
    proxy = ReservaProxy([])
    user = UserFactory.criar_usuario(
        TipoUsuario.COMUM,
        nome="UserX",
        email="userx@example.com",
        senha="minhaSenha",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(user)

    session.add(user)
    session.commit()

    carregado = session.query(User).filter_by(id=user.id).one()
    assert carregado.nome == "UserX"
    assert carregado.email == "userx@example.com"
    assert carregado.tipo == TipoUsuario.COMUM

def test_criacao_user_admin(session):
    proxy = ReservaProxy([])
    admin = UserFactory.criar_usuario(
        TipoUsuario.ADMIN,
        nome="AdminY",
        email="adminy@example.com",
        senha="senhaAdmin",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(admin)

    session.add(admin)
    session.commit()

    carregado = session.query(User).filter_by(id=admin.id).one()
    assert carregado.nome == "AdminY"
    assert carregado.email == "adminy@example.com"
    assert carregado.tipo == TipoUsuario.ADMIN

def test_user_comum_modifica_seu_nome(session):
    proxy = ReservaProxy([])
    user = UserFactory.criar_usuario(
        TipoUsuario.COMUM,
        nome="OrigUser",
        email="orig@example.com",
        senha="senha",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(user)
    session.add(user)
    session.commit()

    # modifica nome
    user.atualizar_perfil(nome="UserNovo")
    session.commit()

    rec = session.query(User).filter_by(id=user.id).one()
    assert rec.nome == "UserNovo"

def test_admin_modifica_seu_nome(session):
    proxy = ReservaProxy([])
    admin = UserFactory.criar_usuario(
        TipoUsuario.ADMIN,
        nome="OrigAdmin",
        email="origadmin@example.com",
        senha="senha",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(admin)
    session.add(admin)
    session.commit()

    # modifica nome
    admin.atualizar_perfil(nome="AdminNovo")
    session.commit()

    rec = session.query(User).filter_by(id=admin.id).one()
    assert rec.nome == "AdminNovo"

def test_user_comum_modifica_email_e_senha(session):
    proxy = ReservaProxy([])
    user = UserFactory.criar_usuario(
        TipoUsuario.COMUM,
        nome="UserE",
        email="usere@example.com",
        senha="senhaOld",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(user)
    session.add(user)
    session.commit()

    # modifica email e senha
    nova_senha = "senhaNew"
    user.atualizar_perfil(email="userN@example.com", senha=nova_senha)
    session.commit()

    rec = session.query(User).filter_by(id=user.id).one()
    assert rec.email == "userN@example.com"
    # verifica que a senha foi re-hashada
    assert rec.senha == hashlib.sha256(nova_senha.encode()).hexdigest()

def test_admin_modifica_email_e_senha(session):
    proxy = ReservaProxy([])
    admin = UserFactory.criar_usuario(
        TipoUsuario.ADMIN,
        nome="AdminE",
        email="admine@example.com",
        senha="senhaOld",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(admin)
    session.add(admin)
    session.commit()

    # modifica email e senha
    nova_senha = "senhaNewAdm"
    admin.atualizar_perfil(email="adminN@example.com", senha=nova_senha)
    session.commit()

    rec = session.query(User).filter_by(id=admin.id).one()
    assert rec.email == "adminN@example.com"
    assert rec.senha == hashlib.sha256(nova_senha.encode()).hexdigest()

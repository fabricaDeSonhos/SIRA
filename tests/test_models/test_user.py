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
        nome="UserComum1",
        email="userx@example.com",
        senha="minhaSenha",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(user)

    session.add(user)
    session.commit()

    carregado = session.query(User).filter_by(id=user.id).one()
    assert carregado.nome == "UserComum1"
    assert carregado.email == "userx@example.com"
    assert carregado.tipo == TipoUsuario.COMUM

def test_criacao_user_admin(session):
    proxy = ReservaProxy([])
    admin = UserFactory.criar_usuario(
        TipoUsuario.ADMIN,
        nome="UserAdmin1",
        email="adminy@example.com",
        senha="senhaAdmin",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(admin)

    session.add(admin)
    session.commit()

    carregado = session.query(User).filter_by(id=admin.id).one()
    assert carregado.nome == "UserAdmin1"
    assert carregado.email == "adminy@example.com"
    assert carregado.tipo == TipoUsuario.ADMIN

def test_user_comum_modifica_seu_nome(session):
    proxy = ReservaProxy([])
    user = UserFactory.criar_usuario(
        TipoUsuario.COMUM,
        nome="UserComum2",
        email="orig@example.com",
        senha="senha",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(user)
    session.add(user)
    session.commit()

    # modifica nome
    user.atualizar_perfil(nome="UserNovo2")
    session.commit()

    rec = session.query(User).filter_by(id=user.id).one()
    assert rec.nome == "UserNovo2"

def test_admin_modifica_seu_nome(session):
    proxy = ReservaProxy([])
    admin = UserFactory.criar_usuario(
        TipoUsuario.ADMIN,
        nome="UserAdmin2",
        email="origadmin@example.com",
        senha="senha",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(admin)
    session.add(admin)
    session.commit()

    # modifica nome
    admin.atualizar_perfil(nome="AdminNovo2")
    session.commit()

    rec = session.query(User).filter_by(id=admin.id).one()
    assert rec.nome == "AdminNovo2"

def test_user_comum_modifica_email_e_senha(session):
    proxy = ReservaProxy([])
    user = UserFactory.criar_usuario(
        TipoUsuario.COMUM,
        nome="UserComum3",
        email="usere@example.com",
        senha="senhaOld",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(user)
    session.add(user)
    session.commit()

    # modifica email e senha
    nova_senha = "senhaNew"
    user.atualizar_perfil(email="novoEmailCOMUM@example.com", senha=nova_senha)
    session.commit()

    rec = session.query(User).filter_by(id=user.id).one()
    assert rec.email == "novoEmailCOMUM@example.com"
    # verifica que a senha foi re-hashada
    assert rec.senha == hashlib.sha256(nova_senha.encode()).hexdigest()

def test_admin_modifica_email_e_senha(session):
    proxy = ReservaProxy([])
    admin = UserFactory.criar_usuario(
        TipoUsuario.ADMIN,
        nome="UserAdmin3",
        email="admine@example.com",
        senha="senhaOld",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(admin)
    session.add(admin)
    session.commit()

    # modifica email e senha
    nova_senha = "senhaNewAdm"
    admin.atualizar_perfil(email="novoEmailADM@example.com", senha=nova_senha)
    session.commit()

    rec = session.query(User).filter_by(id=admin.id).one()
    assert rec.email == "novoEmailADM@example.com"
    assert rec.senha == hashlib.sha256(nova_senha.encode()).hexdigest()

import pytest
from datetime import date, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from src.models.reserva import Base, Sala, Reserva, ReservaProxy
from src.models.user import User, UserFactory, TipoUsuario
from src.models.user import User  


# ---------- Setup da Sessão de Teste ----------

@pytest.fixture(scope="function")
def session():
    # Cria engine em memória e inicializa schema
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# ---------- Objetos de Teste ----------

@pytest.fixture
def sala_teste():
    return Sala("Lab01")

@pytest.fixture
def proxy_teste():
    return ReservaProxy([])  # inicializa sem usuários

@pytest.fixture
def usuario_teste(proxy_teste):
    usuario = UserFactory.criar_usuario(
        tipo=TipoUsuario.COMUM,
        nome="Gabriel",
        email="gabriel@example.com",
        senha="123456",
        proxy=proxy_teste
    )
    proxy_teste.usuarios_cadastrados.append(usuario)
    return usuario

# ---------- Testes ----------

def test_criar_reserva_com_persistencia(session, usuario_teste, sala_teste):
    # Dados da reserva
    data = date(2025, 7, 1)
    hora_ini = time(9, 0)
    hora_fim = time(11, 0)
    nome_materia = "Matemática"

    # Persistindo sala e usuário
    session.add(sala_teste)
    session.add(usuario_teste)
    session.commit()

    # Criando reserva com proxy
    reserva = usuario_teste.fazer_reserva(
        sala=sala_teste,
        data=data,
        hora_inicial=hora_ini,
        hora_final=hora_fim,
        nome_materia=nome_materia
    )

    session.add(reserva)
    session.commit()

    # Consulta para confirmar persistência
    reservas = session.query(Reserva).all()
    assert len(reservas) == 1
    assert reservas[0].nome_materia == "Matemática"
    assert reservas[0].sala.nome == "Lab01"
    assert reservas[0].usuario.nome == "Gabriel"

def test_reserva_conflitante_lanca_excecao(session, usuario_teste, sala_teste):
    data = date(2025, 7, 1)
    hora_ini = time(9, 0)
    hora_fim = time(11, 0)

    session.add(sala_teste)
    session.add(usuario_teste)
    session.commit()

    reserva1 = usuario_teste.fazer_reserva(sala_teste, data, hora_ini, hora_fim, "POO")
    session.add(reserva1)
    session.commit()

    with pytest.raises(ValueError, match="Conflito"):
        usuario_teste.fazer_reserva(sala_teste, data, time(10, 0), time(12, 0), "IA")

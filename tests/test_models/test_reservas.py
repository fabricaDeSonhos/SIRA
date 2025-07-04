import os
import pytest
import uuid
from datetime import date, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.user import UserFactory, TipoUsuario
from src.models.reserva import Base, Sala, ReservaProxy, Reserva

DB_FILE = "test_reserva.db"

@pytest.fixture(scope="session")
def engine():
    # Remove o arquivo antigo apenas uma vez, antes de tudo
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    eng = create_engine(f"sqlite:///{DB_FILE}", echo=False)
    # Cria todas as tabelas uma única vez
    Base.metadata.create_all(eng)
    yield eng
    # Teardown: libera conexões (o arquivo permanece para inspeção)
    eng.dispose()

@pytest.fixture(scope="session")
def session(engine):
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()

def test_usuario_faz_duas_reservas_sem_conflito(session):
    # cria proxy e user
    proxy = ReservaProxy([])
    user = UserFactory.criar_usuario(
        TipoUsuario.COMUM,
        nome="TesteUser",
        email="teste@example.com",
        senha="senha",
        proxy=proxy
    )
    proxy.usuarios_cadastrados.append(user)
    # persiste usuário
    session.add(user)

    # cria sala e persiste
    sala = Sala("SalaA")
    session.add(sala)
    session.commit()

    # faz duas reservas em horários distintos
    r1 = user.fazer_reserva(
        sala=sala,
        data=date(2025, 7, 10),
        hora_inicial=time( 8, 0),
        hora_final=   time(10, 0),
        nome_materia="Matemática"
    )
    session.add(r1)
    session.commit()

    r2 = user.fazer_reserva(
        sala=sala,
        data=date(2025, 7, 10),
        hora_inicial=time(10, 0),
        hora_final=   time(12, 0),
        nome_materia="Física"
    )
    session.add(r2)
    session.commit()

    # Verifica que ambas as reservas existem e pertencem ao mesmo usuário
    todas = session.query(Reserva).filter_by(usuario_id=user.id).order_by(Reserva.hora_inicial).all()
    assert len(todas) == 2
    assert todas[0].nome_materia == "Matemática"
    assert todas[1].nome_materia == "Física"

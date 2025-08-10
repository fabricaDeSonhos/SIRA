import os
import pytest
import uuid
from datetime import date, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.user import UserFactory, TipoUsuario
from src.reserva import Base, Sala, ReservaProxy, Reserva

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

    r3 = user.fazer_reserva(
        sala=sala,
        data=date(2025, 7, 10),
        hora_inicial=time(14, 0),  # 14:00 (2PM)
        hora_final=time(16, 0),    # 16:00 (4PM)
        nome_materia="Geografia"
    )
    session.add(r3)
    session.commit()

    # Reserva 4 - Noite (História)
    r4 = user.fazer_reserva(
        sala=sala,
        data=date(2025, 7, 10),
        hora_inicial=time(18, 30),  # 18:30 (6:30PM)
        hora_final=time(20, 30),    # 20:30 (8:30PM)
        nome_materia="História"
    )
    session.add(r4)
    session.commit()



    # Verifica que ambas as reservas existem e pertencem ao mesmo usuário
    todas = session.query(Reserva).filter_by(usuario_id=user.id).order_by(Reserva.hora_inicial).all()
    assert len(todas) == 4
    assert todas[0].nome_materia == "Matemática"
    assert todas[1].nome_materia == "Física"
    assert todas[2].nome_materia == "Geografia"
    assert todas[3].nome_materia == "História"

from datetime import date, time, datetime
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.database import Base
from src.models.sala_models import Sala
from src.models.user_models import User, TipoUsuario
from src.models.reserva_models import Reserva, ReservationStatus

# 1) Configure engine / sessão (aqui SQLite em memória só para teste rápido)
engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

with Session() as session:
    # 2) Cria uma sala
    sala = Sala(nome="Sala 101")
    session.add(sala)
    
    # 3) Cria um usuário comum
    user = User(
        id=uuid.uuid4(),
        name="Fulano de Tal",
        email="fulano@exemplo.com",
        hashed_password="hash_exemplo",
        salt="salt_exemplo",
        type=TipoUsuario.COMUM.value
    )
    session.add(user)
    
    # 4) Commit para gerar os IDs
    session.commit()
    print(f"  → Sala criada:    id={sala.id}, nome={sala.nome}")
    print(f"  → Usuário criado: id={user.id}, email={user.email}")
    
    # 5) Cria uma reserva ligando sala e usuário
    reserva = Reserva(
        id=str(uuid.uuid4()),            # seu modelo usa string de 36 chars
        user_id=user.id,
        room_id=sala.id,
        reservation_date=date.today(),
        start_time=time(hour=14, minute=0),
        end_time=time(hour=15, minute=0),
        subject_name="Cálculo I",
        status=ReservationStatus.ACTIVE,
        details="Reserva para aula de revisão"
    )
    session.add(reserva)
    session.commit()
    print(f"  → Reserva criada: id={reserva.id}, sala={reserva.room_id}, user={reserva.user_id}")
    
    # 6) Consulta de volta
    r = session.query(Reserva).filter_by(id=reserva.id).one()
    print("Reserva encontrada:")
    print(f"    data: {r.reservation_date}, hora: {r.start_time}–{r.end_time}")
    print(f"    sala: {r.room_id} ({r.sala.nome}), usuário: {r.user_id} ({r.user.name})")

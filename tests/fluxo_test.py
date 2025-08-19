# test para ver o fluxo do banco de dados

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

# Define o nome do arquivo do banco de dados para que possamos inspecioná-lo depois
DB_FILE = "tests/tests_outputs/fluxo_test.db"

@pytest.fixture(scope="session")
def engine():
    """
    Fixture que cria o motor do banco de dados uma vez por sessão de teste.
    Garante um banco de dados limpo a cada execução.
    """

    # Garante que o diretório de saída para o banco de dados de teste exista.
    db_dir = os.path.dirname(DB_FILE)
    os.makedirs(db_dir, exist_ok=True)

    # 1) Antes de tudo, apaga o arquivo velho (se existir) para garantir um teste limpo
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print(f"\nArquivo de banco de dados '{DB_FILE}' antigo removido (se existiu).")

    # Usa um banco de dados SQLite físico para que possamos verificar os dados após o teste
    eng = create_engine(f"sqlite:///{DB_FILE}", echo=False)

    # 2) Cria todas as tabelas (users, rooms, reservas) no banco de dados
    Base.metadata.create_all(eng)
    print("Todas as tabelas foram criadas.")

    yield eng

    # 3) No fim da sessão, o motor é descartado, mas o arquivo .db é mantido.
    print(f"\nSessão de testes finalizada. O arquivo '{DB_FILE}' foi mantido para inspeção.")
    eng.dispose()

@pytest.fixture(scope="session")
def session(engine):
    """
    Fixture que cria uma única sessão do SQLAlchemy para ser usada
    em toda a sessão de teste, garantindo consistência.
    """
    # Vincula a fábrica de sessões ao nosso motor
    Session = sessionmaker(bind=engine)
    sess = Session()
    print("Sessão do banco de dados criada para os testes.")

    yield sess

    # Fecha a sessão no final de tudo
    sess.close()
    print("Sessão do banco de dados fechada.")


# --- Teste de Integração ---

def test_fluxo_completo_de_reserva(session: Session):
    """
    Um único teste que simula um fluxo completo de ponta a ponta:
    1. Cria usuários (comum e admin).
    2. Cria uma sala (ação de admin).
    3. Cria reservas para cada usuário.
    4. Verifica o estado final do banco.
    """
    print("\n--- INICIANDO TESTE DE FLUXO COMPLETO ---")

    # --- Passo 1 e 2: Criação de um usuário comum e um admin ---
    print("\n[Passo 1 e 2: Criando usuários...]")
    user_repo = UserRepository(session)
    
    admin_user = user_repo.create_user(
        name="Super Admin",
        email="admin@example.com",
        password="AdminPassword@123",
        user_type=TipoUsuario.ADMIN
    )
    common_user = user_repo.create_user(
        name="Joana Comum",
        email="joana.comum@example.com",
        password="UserPassword@123"
    )
    
    assert admin_user is not None
    assert isinstance(admin_user, Admin)
    assert common_user is not None
    assert isinstance(common_user, User) and not isinstance(common_user, Admin)
    print("✔ Usuário comum e admin criados com sucesso.")

    # --- Passo 3: Consulta intermediária no banco ---
    print("\n[Passo 3: Verificando usuários no banco...]")
    users_no_banco = session.query(User).all()
    assert len(users_no_banco) == 2
    print(f"✔ Encontrados {len(users_no_banco)} usuários no banco, como esperado.")

    # --- Passo 4: Criação de uma sala (ação de admin) ---
    print("\n[Passo 4: Admin criando uma sala...]")
    room_repo = RoomRepository(session)
    sala_criada = room_repo.create(
        acting_user=admin_user,
        room_data={
            "name": "d101",
            "description": "Sala de Reunião Principal",
            "capacity": 10
        }
    )
    assert sala_criada is not None
    assert sala_criada.name == "d101"
    print(f"✔ Sala '{sala_criada.name}' criada com sucesso.")

    # --- Passo 5 e 6: Criação de duas reservas ---
    print("\n[Passo 5 e 6: Criando reservas para cada usuário...]")
    reserva_repo = ReservaRepository(session)
    
    # Reserva do usuário comum
    reserva_comum = reserva_repo.create(
        acting_user=common_user,
        reserva_data={
            "reservation_date": date(2025, 7, 21),   # ano, mês, dia
            "start_time": time(9, 0),
            "end_time": time(10, 0),
            "subject_name": "Reunião Alpha",
            "details": "Reunião da Equipe Alpha",
            "room_id": sala_criada.id
        }
    )
    # Reserva do usuário admin
    reserva_admin = reserva_repo.create(
        acting_user=admin_user,
        reserva_data={
            "reservation_date": date.today(),
            "start_time": time(11, 0),
            "end_time": time(15, 0),
            "subject_name": "Reunião Alphau",
            "details": "Reunião de Diretoria",
            "room_id": sala_criada.id
        }
    )
    
    assert reserva_comum is not None
    assert reserva_comum.user_id == common_user.id
    assert reserva_admin is not None
    assert reserva_admin.user_id == admin_user.id
    print("✔ Reservas para usuário comum e admin criadas com sucesso.")

    # --- Passo 7: Consulta final no banco ---
    print("\n[Passo 7: Verificação final do estado do banco...]")
    
    # Verifica o total de reservas
    total_reservas = session.query(Reserva).count()
    assert total_reservas == 2
    print(f"✔ Total de reservas no banco: {total_reservas}.")
    
    # Verifica se cada reserva está associada ao usuário e sala corretos
    reserva_joana_db = session.query(Reserva).filter(Reserva.user_id == common_user.id).one()
    assert reserva_joana_db.details == "Reunião da Equipe Alpha"
    assert reserva_joana_db.room.name == "d101"
    print(f"✔ Reserva de '{common_user.name}' verificada.")

    reserva_admin_db = session.query(Reserva).filter(Reserva.user_id == admin_user.id).one()
    assert reserva_admin_db.details == "Reunião de Diretoria"
    assert reserva_admin_db.room.id == sala_criada.id
    print(f"✔ Reserva de '{admin_user.name}' verificada.")

    print("\n--- TESTE DE FLUXO COMPLETO FINALIZADO COM SUCESSO ---")
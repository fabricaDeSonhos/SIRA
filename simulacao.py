# simulacao.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Importando todas as peças da nossa arquitetura
# Em um projeto real, os imports seriam 'from models.database import ...' etc.
# Aqui, vamos supor que eles estão acessíveis para a simulação.

# --- Supondo que estes arquivos existam e são importáveis ---
from src.models.database import Base
from src.models.user_models import User, Admin, TipoUsuario
from src.models.reserva_models import Reserva
from src.models.sala_models import Room

from src.repositories.user_repository import UserRepository
from src.services.reserva_service import ReservaService
from src.services.room_service import RoomService

from src.utils.seeding import seed_initial_rooms
from src.utils import hashing_sennha, email_verifications
# -----------------------------------------------------------

# --- Passo 1: Configuração Inicial ---
# Usaremos um banco de dados SQLite em memória para esta simulação.
# É limpo, rápido e não deixa arquivos para trás.
engine = create_engine("sqlite:///:memory:")
print("Banco de dados em memória configurado.")

# --- Passo 2: Criar Tabelas e Semear Dados Iniciais ---
print("\n--- INICIALIZAÇÃO DO BANCO DE DADOS ---")
# Cria todas as tabelas (users, reservas, rooms)
Base.metadata.create_all(engine)
print("Tabelas criadas com sucesso.")

# Abre uma sessão para semear os dados
with Session(engine) as session:
    seed_initial_rooms(session) # Cria as 5 salas iniciais
    session.commit()
print("--------------------------------------")


# --- O FLUXO DO USUÁRIO COMEÇA AQUI ---

# Inicia uma nova sessão para a simulação da interação do usuário
with Session(engine) as session:

    # --- Passo 3: Criar um Usuário Comum ---
    # Em um app real, isso viria de um endpoint de registro /signup.
    # Usamos o UserRepository diretamente para criar o usuário.
    print("\n--- PASSO 1: REGISTRO DO USUÁRIO ---")
    user_repo = UserRepository(session)
    
    try:
        joao = user_repo.create_user(
            name="João da Silva",
            email="joao.silva@example.com",
            password="Password@123",
            user_type=TipoUsuario.COMUM
        )
        print(f"Usuário comum criado: {joao.name} (ID: {joao.id})")
    except ValueError as e:
        print(f"Erro ao criar usuário: {e}")
        # Se o usuário já existir de uma execução anterior (não acontece em memória), ignora.
        joao = user_repo.get_by_email("joao.silva@example.com")
        print(f"Usuário já existia, carregando: {joao.name}")


    # --- Passo 4: Simular o "Login" do Usuário ---
    # Após o login, a aplicação teria o objeto do usuário que está logado.
    # Aqui, já temos o objeto `joao`. Vamos chamá-lo de `acting_user`.
    print("\n--- PASSO 2: LOGIN ---")
    acting_user = joao
    print(f"'{acting_user.name}' está agora logado no sistema.")

    
    # --- Passo 5: Usuário Interage com o Sistema ---
    # Com o usuário logado, instanciamos os serviços que ele pode usar.
    # Os serviços recebem o `acting_user` para saber quem está realizando as ações.
    print("\n--- PASSO 3: INTERAÇÃO ---")
    reserva_service_joao = ReservaService(acting_user, session)
    room_service_joao = RoomService(acting_user, session)

    # Ação 1: João quer ver as salas disponíveis
    print("\n[Ação 1: Listar salas disponíveis]")
    salas_disponiveis = room_service_joao.list_available_rooms()
    print("Salas encontradas:")
    for sala in salas_disponiveis:
        print(f"- {sala.name}: {sala.description} (Capacidade: {sala.capacity})")

    # Ação 2: João decide reservar a sala "d02"
    print("\n[Ação 2: Fazer uma reserva para a sala 'd02']")
    sala_escolhida = salas_disponiveis[1] # Pegando a d02

    try:
        nova_reserva = reserva_service_joao.create_reserva(
            details=f"Reunião de Alinhamento - Projeto Phoenix",
            room_id=sala_escolhida.id
        )
        print("SUCESSO! Reserva criada:")
        print(f"  ID da Reserva: {nova_reserva.id}")
        print(f"  Para a sala: {nova_reserva.room.name}")
        print(f"  Status: {'Ativa' if nova_reserva.is_active else 'Inativa'}")

    except (ValueError, PermissionError) as e:
        print(f"FALHA! Não foi possível criar a reserva: {e}")

    # Ação 3: João verifica sua lista de reservas
    print("\n[Ação 3: Listar 'Minhas Reservas']")
    minhas_reservas = reserva_service_joao.listar_minhas_reservas()
    print(f"'{acting_user.name}' tem {len(minhas_reservas)} reserva(s) ativa(s):")
    for reserva in minhas_reservas:
        print(f"- ID {reserva.id} para a sala '{reserva.room.name}' com detalhes: '{reserva.details}'")

    # Ação 4: João (usuário comum) tenta fazer algo que não pode
    print("\n[Ação 4: Tentar criar uma reserva 'fixa' (privilégio de Admin)]")
    try:
         reserva_service_joao.create_reserva(
            details="Reserva de Diretoria",
            room_id=sala_escolhida.id,
            is_fixed=True # Usuário comum não pode fazer isso
        )
    except PermissionError as e:
        print(f"SUCESSO NO BLOQUEIO! A política de segurança funcionou: {e}")
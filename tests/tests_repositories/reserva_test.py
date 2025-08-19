# tests/tests_repositories/reservas_test.py
import pytest
from datetime import date, time
import uuid

# Importações dos Modelos e Tipos
from src.models.user_models import User, Admin, TipoUsuario
from src.models.room_models import Room
from src.models.reserva_models import ReservationStatus

# Importações dos Repositórios e Serviços
from src.repositories.user_repository import UserRepository
from src.repositories.room_repositories import RoomRepository
from src.repositories.reserva_repositories import ReservaRepository
from src.services.reserva_service import ReservaService # Importante para testar a lógica de negócio

# --- Fixtures Específicas para este Módulo de Teste ---
# Manter as fixtures aqui torna o arquivo de teste autocontido e fácil de entender.

@pytest.fixture
def common_user(user_repo: UserRepository) -> User:
    """Cria e retorna um usuário Comum padrão para os testes."""
    return user_repo.create_user(
        name="Ana Comum", email="ana.comum@example.com", password="Password@123"
    )

@pytest.fixture
def another_common_user(user_repo: UserRepository) -> User:
    """Cria e retorna um segundo usuário Comum para testar interações."""
    return user_repo.create_user(
        name="Beto Comum", email="beto.comum@example.com", password="Password@123"
    )

@pytest.fixture
def admin_user(user_repo: UserRepository) -> Admin:
    """Cria e retorna um usuário Admin padrão para os testes."""
    return user_repo.create_user(
        name="Carlos Admin", email="carlos.admin@example.com",
        password="Password@123", user_type=TipoUsuario.ADMIN
    )
    
@pytest.fixture
def another_admin_user(user_repo: UserRepository) -> Admin:
    """Cria e retorna um segundo usuário Admin para testar interações."""
    return user_repo.create_user(
        name="Diana Admin", email="diana.admin@example.com",
        password="Password@123", user_type=TipoUsuario.ADMIN
    )

@pytest.fixture
def default_room(admin_user: Admin, room_repo: RoomRepository) -> Room:
    """Cria uma sala padrão, usando o admin_user, para ser usada nos testes de reserva."""
    return room_repo.create(
        acting_user=admin_user,
        room_data={"name": "Sala Padrão", "description": "Sala para testes", "capacity": 5}
    )

# --- Suíte de Testes para Reserva ---

class TestReserva:
    """
    Documentação Viva: Testa o comportamento da criação e consulta de reservas,
    validando as regras de negócio e permissões nas camadas de Serviço e Repositório.
    """

    # A) Testes de Criação (Create)
    # =================================

    def test_A1_common_user_creates_reserva_for_self(self, session, common_user: User, default_room: Room):
        """
        Cenário (A1): Um usuário comum, recém-criado, cria uma reserva para si mesmo.
        Verifica: A criação bem-sucedida através da camada de Serviço.
        """
        print("\n--- Teste (A1): Usuário comum cria reserva para si ---")
        service = ReservaService(acting_user=common_user, db_session=session)
        reserva_data = {
            "room_id": default_room.id, "subject_name": "Reunião de Equipe",
            "reservation_date": date(2025, 8, 18), "start_time": time(14, 0), "end_time": time(15, 0)
        }

        created_reserva = service.create_reserva(reserva_data)

        assert created_reserva is not None
        assert created_reserva.user_id == common_user.id
        print(f"✔ Reserva criada com sucesso para o usuário '{common_user.name}'.")

    def test_A2_admin_user_creates_reserva_for_self(self, session, admin_user: Admin, default_room: Room):
        """
        Cenário (A2): Um admin, recém-criado, cria uma reserva para si mesmo.
        Verifica: Se o método padrão de criação também funciona para administradores.
        """
        print("\n--- Teste (A2): Admin cria reserva para si ---")
        service = ReservaService(acting_user=admin_user, db_session=session)
        reserva_data = {
            "room_id": default_room.id, "subject_name": "Planejamento Admin",
            "reservation_date": date(2025, 8, 19), "start_time": time(10, 0), "end_time": time(11, 0)
        }

        created_reserva = service.create_reserva(reserva_data)

        assert created_reserva is not None
        assert created_reserva.user_id == admin_user.id
        print(f"✔ Reserva de admin criada com sucesso.")

    def test_A3_unauthenticated_user_fails_to_create(self, session):
        """
        Cenário (A3): Uma tentativa de criar uma reserva sem um usuário autenticado (None).
        Verifica: Se o sistema levanta um erro ao inicializar o serviço, protegendo contra ações não autenticadas.
        """
        print("\n--- Teste (A3): Usuário não autenticado falha ao criar reserva ---")
        with pytest.raises(ValueError, match="Um usuário ativo é necessário para inicializar o serviço."):
            ReservaService(acting_user=None, db_session=session)
        print(f"✔ Tentativa de criação por usuário 'None' falhou como esperado.")

    def test_A4_common_user_fails_to_create_fixed_reserva(self, reserva_repo: ReservaRepository, common_user: User, default_room: Room):
        """
        Cenário (A4): Um usuário comum tenta criar uma reserva 'fixa'.
        Verifica: Se a ReservaPolicy (chamada pelo repositório) bloqueia a ação e levanta PermissionError.
        """
        print("\n--- Teste (A4): Usuário comum falha ao tentar criar reserva fixa ---")
        reserva_data = {
            "room_id": default_room.id, "subject_name": "Reserva Fixa Ilegal",
            "status": ReservationStatus.FIXED,
            "reservation_date": date(2025, 1, 1), "start_time": time(9,0), "end_time": time(10,0),
            "user_id": common_user.id
        }
        with pytest.raises(PermissionError, match="Apenas administradores podem criar reservas fixas"):
            reserva_repo.create(acting_user=common_user, reserva_data=reserva_data)
        print("✔ Tentativa de criar reserva fixa foi bloqueada pela política de segurança.")

    # B) Testes de Verificação de Propriedade
    # ========================================

    def test_B1_reserva_is_correctly_linked_to_creator(self, reserva_repo: ReservaRepository, common_user: User, admin_user: Admin, default_room: Room):
        """
        Cenário (B1): Reservas são criadas por usuários diferentes.
        Verifica: Se cada reserva está inequivocamente ligada ao seu criador.
        """
        print("\n--- Teste (B1): Verifica se a reserva pertence ao criador correto ---")
        reserva_comum = reserva_repo.create(common_user, {"room_id": default_room.id, "subject_name": "Reserva de Ana", "user_id": common_user.id, "reservation_date": date(2025, 1, 1), "start_time": time(9,0), "end_time": time(10,0)})
        reserva_admin = reserva_repo.create(admin_user, {"room_id": default_room.id, "subject_name": "Reserva de Carlos", "user_id": admin_user.id, "reservation_date": date(2025, 1, 2), "start_time": time(9,0), "end_time": time(10,0)})
        
        assert reserva_repo.get_by_id(reserva_comum.id).user_id == common_user.id
        assert reserva_repo.get_by_id(reserva_admin.id).user_id == admin_user.id
        print("✔ As reservas foram corretamente associadas aos seus respectivos criadores.")

    # C) Testes de Criação por Terceiros (Privilégios de Admin)
    # ==========================================================

    def test_C1_admin_creates_reserva_for_common_user(self, session, admin_user: Admin, common_user: User, default_room: Room):
        """
        Cenário (C1): Um admin cria uma reserva para um usuário comum.
        Verifica: Se a reserva é criada e pertence ao usuário alvo, não ao admin.
        """
        print("\n--- Teste (C1): Admin cria reserva para outro usuário ---")
        service = ReservaService(acting_user=admin_user, db_session=session)
        reserva_data = {"room_id": default_room.id, "subject_name": "Reserva Delegada", "reservation_date": date(2025, 9, 1), "start_time": time(10, 0), "end_time": time(11, 0)}

        created_reserva = service.create_reserva_for_user(target_user_id=common_user.id, reserva_data=reserva_data)

        assert created_reserva.user_id == common_user.id
        print(f"✔ Sucesso! Admin '{admin_user.name}' criou uma reserva para '{common_user.name}'.")

    def test_C2_common_user_fails_to_create_for_another(self, session, common_user: User, another_common_user: User, default_room: Room):
        """
        Cenário (C2): Um usuário comum tenta criar uma reserva para outro.
        Verifica: Se o serviço levanta um PermissionError, protegendo a funcionalidade.
        """
        print("\n--- Teste (C2): Usuário comum é bloqueado ao tentar criar para outro ---")
        service = ReservaService(acting_user=common_user, db_session=session)
        with pytest.raises(PermissionError, match="Apenas administradores podem criar reservas para outros usuários"):
            service.create_reserva_for_user(target_user_id=another_common_user.id, reserva_data={})
        print(f"✔ Acesso negado para usuário comum, como esperado.")

    def test_C3_admin_creates_reserva_for_another_admin(self, session, admin_user: Admin, another_admin_user: Admin, default_room: Room):
        """
        Cenário (C3): Um admin cria uma reserva para outro admin.
        Verifica: Se a funcionalidade se aplica também entre administradores.
        """
        print("\n--- Teste (C3): Admin cria reserva para outro admin ---")
        service = ReservaService(acting_user=admin_user, db_session=session)
        reserva_data = {"room_id": default_room.id, "subject_name": "Reserva de Admin para Admin", "reservation_date": date(2025, 9, 3), "start_time": time(14,0), "end_time": time(15,0)}
        
        created_reserva = service.create_reserva_for_user(target_user_id=another_admin_user.id, reserva_data=reserva_data)

        assert created_reserva.user_id == another_admin_user.id
        print(f"✔ Sucesso! Admin '{admin_user.name}' criou uma reserva para o admin '{another_admin_user.name}'.")

    def test_C4_admin_creates_fixed_reserva_for_another(self, session, admin_user: Admin, common_user: User, default_room: Room):
        """
        Cenário (C4): Um admin cria uma reserva FIXA para outro usuário.
        Verifica: Se a permissão de criar reserva fixa é validada corretamente mesmo ao criar para terceiros.
        """
        print("\n--- Teste (C4): Admin cria reserva FIXA para outro ---")
        service = ReservaService(acting_user=admin_user, db_session=session)
        reserva_data = {
            "room_id": default_room.id, "subject_name": "Alocação Fixa para Ana",
            "status": ReservationStatus.FIXED,
            "reservation_date": date(2025, 9, 4), "start_time": time(9,0), "end_time": time(17,0)
        }

        created_reserva = service.create_reserva_for_user(target_user_id=common_user.id, reserva_data=reserva_data)

        assert created_reserva.user_id == common_user.id
        assert created_reserva.status == ReservationStatus.FIXED
        print(f"✔ Sucesso! Admin criou uma reserva fixa para '{common_user.name}'.")

    # D) Testes de Busca (Query)
    # ===========================

    def test_D1_list_by_user_and_check_active_filter(self, reserva_repo: ReservaRepository, common_user: User, default_room: Room):
        """
        Cenário (D1): Um usuário tem reservas com status diferentes.
        Verifica: Se a listagem de reservas do repositório respeita o filtro 'active_only'.
        """
        print("\n--- Teste (D1): Verifica a listagem e o filtro de reservas ativas ---")
        # Arrange
        reserva_repo.create(common_user, {"room_id": default_room.id, "subject_name": "Ativa", "user_id": common_user.id, "status": ReservationStatus.ACTIVE, "reservation_date": date(2025, 1, 1), "start_time": time(9,0), "end_time": time(10,0)})
        reserva_repo.create(common_user, {"room_id": default_room.id, "subject_name": "Cancelada", "user_id": common_user.id, "status": ReservationStatus.CANCELLED, "reservation_date": date(2025, 1, 2), "start_time": time(9,0), "end_time": time(10,0)})

        # Act
        reservas_ativas = reserva_repo.list_by_user(user_id=common_user.id, active_only=True)
        todas_as_reservas = reserva_repo.list_by_user(user_id=common_user.id, active_only=False)

        # Assert
        assert len(reservas_ativas) == 1
        assert reservas_ativas[0].subject_name == "Ativa"
        assert len(todas_as_reservas) == 2
        print("✔ Filtro 'active_only' da listagem funcionou como esperado.")

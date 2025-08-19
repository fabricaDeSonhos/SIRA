# tests/tests_repositories/test_room_repository.py
import pytest
from src.models.user_models import User, Admin, TipoUsuario
from src.repositories.user_repository import UserRepository
from src.repositories.room_repositories import RoomRepository
from src.utils.exceptions import DuplicateRoomError
from sqlalchemy.exc import IntegrityError

# --- Fixtures de Usuários ---
# Estas fixtures criam usuários que podem ser reutilizados pelos testes
# Evita a repetição de código e foca o teste na lógica de 'Room'.

# Mock para evitar dependências externas
@pytest.fixture(autouse=True)
def patch_utils(monkeypatch):
    # Desliga a verificação de e-mail para que a criação de usuários nas fixtures não falhe
    monkeypatch.setattr('src.utils.email_verification.verificar_email_para_cadastro', lambda email, db: None)
    # Padroniza o hashing de senha
    monkeypatch.setattr('src.utils.hashing_senha.hash_and_validate', lambda pw: ("salt123", "hash123"))


@pytest.fixture
def admin_user(user_repo: UserRepository) -> Admin:
    """Fixture que cria e retorna um usuário Admin padrão."""
    return user_repo.create_user(
        name="Admin de Teste",
        email="admin.teste@example.com",
        password="Password@123",
        user_type=TipoUsuario.ADMIN
    )

@pytest.fixture
def common_user(user_repo: UserRepository) -> User:
    """Fixture que cria e retorna um usuário Comum padrão."""
    return user_repo.create_user(
        name="Usuário Comum de Teste",
        email="comum.teste@example.com",
        password="Password@123"
    )

# --- Suíte de Testes para RoomRepository ---

class TestRoomRepository:
    """
    Agrupa todos os testes para o RoomRepository.
    """

    def test_create_room_success_with_admin_user(self, room_repo: RoomRepository, admin_user: Admin):
        """
        Cenário: Um usuário Admin cria uma sala com dados válidos.
        Verifica se a sala é criada corretamente e persistida no banco.
        """
        print("\n--- Teste: Admin criando sala com sucesso ---")
        # Arrange
        room_data = {
            "name": "Sala de Reunião Alpha",
            "description": "Sala para reuniões da equipe Alpha.",
            "capacity": 10
        }

        # Act
        created_room = room_repo.create(acting_user=admin_user, room_data=room_data)

        # Assert
        assert created_room is not None
        assert created_room.id is not None
        assert created_room.name == "Sala de Reunião Alpha"
        assert created_room.capacity == 10
        print(f"✔ Sala '{created_room.name}' criada com sucesso pelo admin '{admin_user.name}'.")

    def test_create_room_fails_with_common_user(self, room_repo: RoomRepository, common_user: User):
        """
        Cenário: Um usuário Comum tenta criar uma sala.
        Verifica se uma exceção de permissão (PermissionError) é levantada,
        conforme definido na RoomPolicy.
        """
        print("\n--- Teste: Usuário comum falha ao tentar criar sala ---")
        # Arrange
        room_data = {"name": "Sala Secreta", "capacity": 5}

        # Act & Assert
        with pytest.raises(PermissionError) as excinfo:
            room_repo.create(acting_user=common_user, room_data=room_data)
        
        assert "Apenas administradores podem gerenciar salas" in str(excinfo.value)
        print(f"✔ Tentativa de criação de sala pelo usuário '{common_user.name}' foi bloqueada corretamente.")

    def test_create_room_with_duplicate_name_raises_error(self, room_repo: RoomRepository, admin_user: Admin):
        """
        Cenário: Um admin tenta criar uma sala com um nome que já existe.
        Verifica se a exceção customizada 'DuplicateRoomError' é levantada.
        """
        print("\n--- Teste: Erro ao criar sala com nome duplicado ---")
        # Arrange
        room_data = {"name": "Sala Única", "capacity": 3}
        room_repo.create(acting_user=admin_user, room_data=room_data) # Cria a primeira sala
        print(f"✔ Primeira sala '{room_data['name']}' criada.")

        # Act & Assert
        print("... Tentando criar a segunda sala com o mesmo nome...")
        with pytest.raises(DuplicateRoomError) as excinfo:
            room_repo.create(acting_user=admin_user, room_data=room_data) # Tenta criar a segunda
        
        assert f"A sala com o nome '{room_data['name']}' já existe" in str(excinfo.value)
        print("✔ Exceção de nome duplicado levantada corretamente.")

    def test_get_and_list_rooms(self, room_repo: RoomRepository, admin_user: Admin):
        """
        Cenário: Cria múltiplas salas e depois as busca.
        Verifica se os métodos get_by_id, get_by_name e list_all funcionam.
        """
        print("\n--- Teste: Listar e buscar salas ---")
        # Arrange
        sala1 = room_repo.create(admin_user, {"name": "Sala-A", "capacity": 1})
        sala2 = room_repo.create(admin_user, {"name": "Sala-B", "capacity": 2})

        # Act
        all_rooms = room_repo.list_all()
        found_by_id = room_repo.get_by_id(sala2.id)
        found_by_name = room_repo.get_by_name("Sala-A")

        # Assert
        assert len(all_rooms) == 2
        assert all_rooms[0].name == "Sala-A"
        assert all_rooms[1].name == "Sala-B"
        print(f"✔ list_all retornou {len(all_rooms)} salas.")

        assert found_by_id is not None
        assert found_by_id.name == "Sala-B"
        print(f"✔ get_by_id encontrou a sala '{found_by_id.name}'.")

        assert found_by_name is not None
        assert found_by_name.name == "Sala-A"
        print(f"✔ get_by_name encontrou a sala '{found_by_name.name}'.")

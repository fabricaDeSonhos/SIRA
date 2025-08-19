# tests/tests_repositories/users_tests.py
import pytest
from src.models.user_models import User, Admin, TipoUsuario
from src.repositories.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError

# Mock APENAS para a função de hashing, para manter os testes rápidos e previsíveis.
# A verificação de e-mail agora será testada de verdade.
@pytest.fixture(autouse=True)
def patch_hashing(monkeypatch):
    monkeypatch.setattr(
        'src.utils.hashing_senha.hash_and_validate',
        lambda pw: ("salt123", "hash123")
    )

class TestUserRepository:
    """
    Agrupa todos os testes para o UserRepository.
    """

    def test_create_common_user_success(self, user_repo: UserRepository):
        """
        Cenário: Criação de um usuário comum com dados válidos.
        """
        print("\n--- Teste: Criar usuário comum com sucesso ---")
        user_data = {
            "name": "João Comum",
            "email": "joao.comum@example.com",
            "password": "Password@123"
        }
        created_user = user_repo.create_user(**user_data)

        assert created_user is not None
        assert created_user.name == user_data["name"]
        assert created_user.type == TipoUsuario.COMUM.value
        print(f"✔ Usuário '{created_user.name}' criado com sucesso.")

    def test_create_admin_user_success(self, user_repo: UserRepository):
        """
        Cenário: Criação de um usuário administrador.
        """
        print("\n--- Teste: Criar usuário admin com sucesso ---")
        admin_data = {
            "name": "Maria Admin",
            "email": "maria.admin@example.com",
            "password": "Password@123",
            "user_type": TipoUsuario.ADMIN
        }
        created_admin = user_repo.create_user(**admin_data)

        assert created_admin is not None
        assert isinstance(created_admin, Admin)
        assert created_admin.type == TipoUsuario.ADMIN.value
        print(f"✔ Administrador '{created_admin.name}' criado com sucesso.")

    def test_create_user_with_duplicate_email_raises_value_error(self, user_repo: UserRepository):
        """
        Cenário: Tentativa de criar um segundo usuário com um e-mail que já existe.
        Verifica se a validação preventiva em 'verificar_email_para_cadastro' levanta um ValueError.
        """
        print("\n--- Teste: Erro ao criar usuário com e-mail duplicado ---")
        email = "email.duplicado@example.com"
        
        primeiro_usuario = user_repo.create_user(
            name="Primeiro Usuário", 
            email=email, 
            password="Password@123"
        )
        print(f"✔ Usuário inicial criado com sucesso: ID={primeiro_usuario.id}, Email='{primeiro_usuario.email}'")

        print("... Tentando criar um segundo usuário com o mesmo e-mail...")
        # --- CORREÇÃO APLICADA AQUI ---
        # Agora esperamos um ValueError, que é o comportamento programado da sua função de verificação.
        with pytest.raises(ValueError) as excinfo:
            user_repo.create_user(name="Segundo Usuário", email=email, password="Password@456")
        
        # Verificamos se a mensagem de erro é a que esperamos da nossa lógica de negócio.
        assert "E-mail já cadastrado. Use outro." in str(excinfo.value)
        print(f"✔ Exceção de negócio (ValueError) levantada corretamente.")

    def test_get_user_by_id_and_email(self, user_repo: UserRepository):
        """
        Cenário: Recuperar um usuário existente por seu ID e por seu e-mail.
        """
        print("\n--- Teste: Buscar usuário por ID e E-mail ---")
        user = user_repo.create_user(name="Carlos", email="carlos@example.com", password="Password@123")

        found_by_id = user_repo.get_by_id(user.id)
        found_by_email = user_repo.get_by_email(user.email)

        assert found_by_id.id == user.id
        print(f"✔ Usuário encontrado por ID: {found_by_id.id}")
        
        assert found_by_email.email == user.email
        print(f"✔ Usuário encontrado por E-mail: {found_by_email.email}")

    def test_update_user_data(self, user_repo: UserRepository):
        """
        Cenário: Atualizar os dados de um usuário existente.
        """
        print("\n--- Teste: Atualizar dados de um usuário ---")
        user = user_repo.create_user(name="Ana Original", email="ana@example.com", password="Password@123")
        
        update_data = {"name": "Ana Atualizada", "is_active": False}
        updated_user = user_repo.update_user(user, update_data)

        assert updated_user.name == "Ana Atualizada"
        assert updated_user.is_active is False
        print(f"✔ Dados do usuário '{updated_user.name}' atualizados com sucesso.")

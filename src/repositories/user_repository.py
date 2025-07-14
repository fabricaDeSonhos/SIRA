from typing import Optional, Type
import uuid

from sqlalchemy.orm import Session

# Importe seus módulos e os modelos
from src.models.user_models import User, Admin, TipoUsuario
from src.utils import hashing_sennha, email_verifications # Supondo que estejam em core/

class UserRepository:
    def __init__(self, db_session: Session):
        """
        Inicializa o repositório com uma sessão de banco de dados.
        :param db_session: A sessão do SQLAlchemy.
        """
        self.db = db_session

    def create_user(
        self, 
        name: str, 
        email: str, 
        password: str, 
        user_type: TipoUsuario = TipoUsuario.COMUM
    ) -> User:
        """
        Cria um novo usuário, validando os dados e fazendo o hash da senha.
        Este método é o "ponto de entrada" para novos usuários no sistema.
        """
        # 1. Validar o email (formato e se já existe)
        email_verifications.verificar_email_para_cadastro(email, self.db)
        
        # 2. Validar a força da senha e gerar o hash e o salt
        try:
            salt_hex, hash_hex = hashing_sennha.hash_and_validate(password)
        except ValueError as e:
            # Propaga o erro de senha fraca
            raise e

        # 3. Escolher a classe correta (User ou Admin) com base no tipo
        user_class: Type[User] = Admin if user_type == TipoUsuario.ADMIN else User
        
        # 4. Cria a instância do modelo com os dados seguros
        new_user = user_class(
            name=name,
            email=email,
            hashed_password=hash_hex,
            salt=salt_hex,
            # O campo 'type' será preenchido automaticamente pelo SQLAlchemy
        )

        # 5. Adicionar à sessão e fazer o commit
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        return new_user

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Busca um usuário pelo seu UUID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Busca um usuário pelo seu email."""
        return self.db.query(User).filter(User.email == email).first()

    def update_user(self, user: User, update_data: dict) -> User:
        """
        Atualiza os dados de um usuário.
        O objeto 'user' deve ser uma instância gerenciada pelo SQLAlchemy.
        """
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def set_active_status(self, user: User, is_active: bool) -> User:
        """Ativa ou desativa um usuário."""
        user.is_active = is_active
        self.db.commit()
        self.db.refresh(user)
        return user
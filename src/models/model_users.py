import enum
import uuid
from typing import List

from sqlalchemy import (
    Boolean,
    String,
    Enum as EnumDB,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

# --- Base Declarativa e Enum ---

from .base import Base

class UserType(enum.Enum):
    """Define os tipos de usuário no sistema."""
    COMMON = "comum"
    ADMIN = "admin"

# --- Modelo User (Classe Pai) ---

class User(Base):
    """
    Modelo base para todos os usuários do sistema.
    Utiliza uma estratégia de herança de tabela única, onde o campo 'type'
    atua como o discriminador para determinar se a instância é um User ou Admin.
    """
    __tablename__ = "users"

    # --- Colunas da Tabela ---

    # SUGESTÃO 1: ID como UUID. Excelente para segurança e escalabilidade.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # SUGESTÃO 2: Email único e indexado para performance.
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    # SUGESTÃO 3: Armazenar a senha como hash, nunca em texto plano.
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # --- Configuração da Herança de Tabela Única ---
    
    # Esta é a coluna "discriminadora". Ela diz ao SQLAlchemy qual classe carregar.
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "comum", # Valor para esta classe base (User)
        "polymorphic_on": "type",        # Coluna usada para discriminar
    }
    
    # --- Relacionamentos ---
    # Adicionando o relacionamento inverso para as reservas.
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation", 
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, email='{self.email}', type='{self.type}')>"


# --- Modelo Admin (Classe Filha) ---
class Admin(User):
    """
    Modelo para um usuário Administrador. Herda todos os campos de User
    e reside na mesma tabela 'users'. Não possui colunas próprias.
    """
    __mapper_args__ = {
        "polymorphic_identity": "admin", # Valor discriminador para esta classe
    }

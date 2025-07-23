import enum
import uuid
from typing import List

# Base declarativa do SQLAlchemy
from .database import Base

from sqlalchemy import (
    Boolean,
    String,
    Enum as EnumDB,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    relationship
)

# Enum para os tipos de usuário, alinhado com user_service.py
class TipoUsuario(enum.Enum):
    """Define os tipos de usuário no sistema."""
    COMUM = "comum"
    ADMIN = "admin"

# --- Modelo User (Classe Pai) ---
class User(Base):
    """
    Modelo base para todos os usuários. Utiliza herança de tabela única,
    com a coluna 'type' atuando como discriminador.
    """
    __tablename__ = "users"

    # --- Colunas da Tabela ---
    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    # Armazena o hash da senha gerado pelo Argon2id
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Armazena o salt usado para gerar o hash, essencial para verificação
    salt: Mapped[str] = mapped_column(String(32), nullable=False) # 32 chars para 16 bytes em hex
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # --- Configuração da Herança ---
    # Coluna "discriminadora" que define o tipo de objeto (User ou Admin)
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": TipoUsuario.COMUM.value, # Valor para a classe User
        "polymorphic_on": "type",                      # Coluna usada para discriminar
    }
    
    # --- Relacionamentos ---
    reservas: Mapped[List["Reserva"]] = relationship(
        "Reserva", 
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', type='{self.type}')>"

# --- Modelo Admin (Classe Filha) ---
class Admin(User):
    """
    Modelo para um usuário Administrador. Herda de User e reside na mesma tabela.
    """
    __mapper_args__ = {
        "polymorphic_identity": TipoUsuario.ADMIN.value, # Valor discriminador para Admin
    }

    def __repr__(self):
        return f"<Admin(id={self.id}, email='{self.email}', type='{self.type}')>"
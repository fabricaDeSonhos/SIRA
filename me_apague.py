# /models/reserva_models.py
import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    String,
    ForeignKey,
    DateTime,
    Enum as EnumDB,
    func
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

# Importe a Base declarativa do seu arquivo de configuração do banco
from .database import Base

# Importe User para o type hint do relacionamento
from .user_models import User  

# --- Enum atualizado com o status "FIXA" ---
class ReservationStatus(enum.Enum):
    """Define os possíveis status de uma reserva."""
    ACTIVE = "ativa"
    CANCELLED = "cancelada"
    COMPLETED = "concluída"
    FIXED = "fixa"  # Nova opção para reservas recorrentes/permanentes

class Reserva(Base):
    """
    Modelo SQLAlchemy para uma Reserva.
    """
    __tablename__ = "reservas"

    # --- Colunas da Tabela ---

    id: Mapped[int] = mapped_column(primary_key=True)
    
    details: Mapped[str] = mapped_column(
        String(300), 
        nullable=False,
        comment="Detalhes específicos da reserva."
    )
    
    status: Mapped[ReservationStatus] = mapped_column(
        EnumDB(ReservationStatus), 
        default=ReservationStatus.ACTIVE, 
        nullable=False
    )
    
    is_fixed: Mapped[bool] = mapped_column(
        Boolean, 
        default=False, 
        nullable=False,
        comment="Indica se é uma reserva fixa (privilégio de Admin)."
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        comment="Data e hora de criação da reserva."
    )

    # --- Chave Estrangeira e Relacionamento ---
    
    # Define a coluna que armazena o ID do usuário dono da reserva
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        ForeignKey("users.id"),
        nullable=False
    )
    
    # Cria o relacionamento com o objeto User, permitindo acessar
    # os dados do usuário a partir de uma reserva (ex: reserva.user.name)
    user: Mapped["User"] = relationship(
        "User", 
        back_populates="reservas" # Deve corresponder ao nome do relacionamento em user_models.py
    )

    def __repr__(self):
        return f"<Reserva(id={self.id}, user_id='{self.user_id}', is_active={self.is_active})>"
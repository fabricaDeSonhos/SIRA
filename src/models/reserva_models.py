import enum
from datetime import date, time, datetime
from typing import List # Necessário para os relacionamentos com type hints

from sqlalchemy import (
    String,
    ForeignKey,
    Enum as EnumDB, # Renomeando para evitar conflito com o enum do Python
    func # Para usar funções do SQL como NOW()
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)

# --- Base Declarativa para o SQLAlchemy 2.0 ---
from .database import Base

from .user_models import User  


# --- Enum atualizado com o status "FIXA" ---
class ReservationStatus(enum.Enum):
    """Define os possíveis status de uma reserva."""
    ACTIVE = "ativa"
    CANCELLED = "cancelada"
    COMPLETED = "concluída"
    FIXED = "fixa"  # Nova opção para reservas recorrentes/permanentes

# --- Modelo Reserva com a nova sintaxe ---
class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)   
   
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    
    reservation_date: Mapped[date] = mapped_column(comment="Data da reserva")
    start_time: Mapped[time] = mapped_column(comment="Horário de início da reserva")
    end_time: Mapped[time] = mapped_column(comment="Horário de término da reserva")
    
    # Para Strings, ainda é necessário especificar o comprimento
    subject_name: Mapped[str] = mapped_column(String(100), comment="Nome da matéria", nullable=False)

    # Usando o Enum atualizado, com um valor padrão
    status: Mapped[ReservationStatus] = mapped_column(
        EnumDB(ReservationStatus), 
        default=ReservationStatus.ACTIVE, 
        nullable=False
    )

    details: Mapped[str] = mapped_column(
        String(300), 
        nullable=False,
        comment="Detalhes específicos da reserva."
    )
    
    # Timestamps usando funções do servidor de banco de dados (mais robusto)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    # --- Relacionamentos com Type Hinting moderno ---
    # O nome da classe entre aspas ("User") evita problemas de importação circular
    user: Mapped["User"] = relationship("User", back_populates="reservas") # Deve corresponder ao nome do relacionamento em user_models.py
    #room: Mapped["Room"] = relationship(back_populates="reservas")

    def __repr__(self):
        return f"<Reserva(id={self.id}, user_id='{self.user_id}', is_active={self.is_active})>"

        #return (
        #    f"<Reserva(id={self.id}, room_id={self.room_id}, "
        #    f"date='{self.reservation_date}', status='{self.status.value}')>"
        #)
    




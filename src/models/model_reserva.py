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
from .base import Base
# --- Enum atualizado com o status "FIXA" ---
class ReservationStatus(enum.Enum):
    """Define os possíveis status de uma reserva."""
    ACTIVE = "ativa"
    CANCELLED = "cancelada"
    COMPLETED = "concluída"
    FIXED = "fixa"  # Nova opção para reservas recorrentes/permanentes

# --- Modelo Reservation com a nova sintaxe ---
class Reservation(Base):
    """
    Modelo SQLAlchemy para a tabela 'reservations' utilizando a sintaxe moderna (2.0).
    """
    __tablename__ = "reservations"

    # A sintaxe `Mapped[tipo_python]` oferece type hinting integrado
    # O que está dentro de `mapped_column()` são as configurações do banco de dados
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)   
    # nullable=False é inferido a partir do tipo não-opcional (ex: Mapped[int] vs Mapped[Optional[int]])
    # mas é bom ser explícito para ForeignKeys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    
    reservation_date: Mapped[date] = mapped_column(comment="Data da reserva")
    start_time: Mapped[time] = mapped_column(comment="Horário de início da reserva")
    end_time: Mapped[time] = mapped_column(comment="Horário de término da reserva")
    
    # Para Strings, ainda é necessário especificar o comprimento
    subject_name: Mapped[str] = mapped_column(String(100), comment="Nome da matéria ou finalidade")

    # Usando o Enum atualizado, com um valor padrão
    status: Mapped[ReservationStatus] = mapped_column(
        EnumDB(ReservationStatus), 
        default=ReservationStatus.ACTIVE, 
        nullable=False
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
    user: Mapped["User"] = relationship(back_populates="reservations")
    room: Mapped["Room"] = relationship(back_populates="reservations")

    def __repr__(self):
        return (
            f"<Reservation(id={self.id}, room_id={self.room_id}, "
            f"date='{self.reservation_date}', status='{self.status.value}')>"
        )

# --- Modelos User e Room atualizados para demonstrar o relacionamento ---

# class User(Base):
#     __tablename__ = "users"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     # ... outros campos do usuário
#     reservations: Mapped[List["Reservation"]] = relationship(back_populates="user")

# class Room(Base):
#     __tablename__ = "rooms"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     # ... outros campos da sala
#     reservations: Mapped[List["Reservation"]] = relationship(back_populates="room")
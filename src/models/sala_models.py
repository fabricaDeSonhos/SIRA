# /models/room_models.py (Novo arquivo)

from typing import List
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base
# from .reserva_models import Reserva # Import para o type hint


class Room(Base):
    """
    Modelo SQLAlchemy para uma Sala de Reunião/Evento.
    """
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="Nome/código único da sala (ex: d01, d02)."
    )
    
    description: Mapped[str] = mapped_column(
        String(255), 
        nullable=True,
        comment="Descrição amigável da sala."
    )
    
    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
        comment="Capacidade máxima de pessoas na sala."
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Se a sala está disponível para novas reservas."
    )
    
    # Relacionamento inverso: a partir de uma sala, podemos ver todas as suas reservas
    reservas: Mapped[List["Reserva"]] = relationship(
        "Reserva", 
        back_populates="room",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}')>"
# /models/room_models.py (Nome de arquivo corrigido)

from typing import List
from sqlalchemy import String, Integer, Boolean, CheckConstraint # <-- Importar CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Room(Base):
    """
    Modelo SQLAlchemy para uma Sala de Reunião/Evento.
    """
    __tablename__ = "rooms"
    
    # Adicionando um comentário de tabela para documentação
    __table_args__ = (
        CheckConstraint('capacity > 0', name='cc_room_capacity_positive'),
    )

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
    
    # MELHORIA: A CheckConstraint acima garante que este valor será sempre > 0 no banco.
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
    
    reservas: Mapped[List["Reserva"]] = relationship(
        "Reserva", 
        back_populates="room",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Room(id={self.id}, name='{self.name}')>"
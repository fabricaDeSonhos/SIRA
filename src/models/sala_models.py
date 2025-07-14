from sqlalchemy import (
    Boolean,
    String,
    Enum as EnumDB,
    Integer,
    List
)
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from .database import Base
from .reserva_models import Reserva


class Sala(Base):
    __tablename__ = "salas"

    id: Mapped[int]   = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    #migration 

    reservas: Mapped[List["Reserva"]] = relationship("Reserva", back_populates="sala")

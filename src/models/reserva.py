from .estado_reserva import ReservaAtiva, ReservaCancelada, ReservaConcluida

import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Time, Date, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from datetime import time, date
from typing import TYPE_CHECKING, List
from sqlalchemy.ext.declarative import declarative_base
from .base import Base

if TYPE_CHECKING:
    from .user import User

# Observer
class Observer:
    def atualizar(self, reserva):
        raise NotImplementedError()

class EmailNotificador(Observer):
    def atualizar(self, reserva):
        print(f"[Email] Notificação: A reserva foi {reserva.estado.__class__.__name__}.")

class LogReserva(Observer):
    def atualizar(self, reserva):
        print(f"[Log] Estado da reserva alterado para: {reserva.estado.__class__.__name__}")

# Sala
class Sala(Base):
    __tablename__ = "salas"

    id: Mapped[int]   = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    #migration 
   
    reservas: Mapped[List["Reserva"]] = relationship("Reserva", back_populates="sala")

    def __init__(self, nome: str):
        self.nome = nome

    def verifica_conflito(self, nova_reserva: "Reserva") -> bool:
        for r in self.reservas:
            if r.data == nova_reserva.data and (
                nova_reserva.hora_inicial < r.hora_final and
                nova_reserva.hora_final > r.hora_inicial
            ):
                return True
        return False

    def adicionar_reserva(self, nova_reserva: "Reserva"):
        if self.verifica_conflito(nova_reserva):
            raise ValueError(f"Conflito: Sala '{self.nome}' já possui reserva nesse horário.")
        self.reservas.append(nova_reserva)

    def remover_reserva(self, reserva: "Reserva"):
        if reserva in self.reservas:
            self.reservas.remove(reserva)

    def __repr__(self):
        return f"Sala({self.nome})"

# Reserva
class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["User"] = relationship("User", back_populates="reservas")

    sala_id:    Mapped[int] = mapped_column(ForeignKey("salas.id"))
    sala:       Mapped[Sala] = relationship("Sala", back_populates="reservas")

    data: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicial: Mapped[time] = mapped_column(Time, nullable=False)
    hora_final: Mapped[time] = mapped_column(Time, nullable=False)
    nome_materia: Mapped[str] = mapped_column(String, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
   #campo de descrição
   
   
    # atributos extras
    def __post_init__(self):
        self.estado = ReservaAtiva()
        self.observadores = []

    @classmethod
    def criar(cls, usuario: "User", sala: Sala, data: date, hora_inicial: time, hora_final: time, nome_materia: str) -> "Reserva":
        reserva = cls(
            id=str(uuid.uuid4()),
            usuario=usuario,
            sala=sala,
            data=data,
            hora_inicial=hora_inicial,
            hora_final=hora_final,
            nome_materia=nome_materia,
            ativo=True
        )
        reserva.estado = ReservaAtiva()
        reserva.observadores = []
        sala.adicionar_reserva(reserva)
        return reserva

    def adicionar_observador(self, obs: Observer):
        self.observadores.append(obs)

    def notificar_observadores(self):
        for obs in self.observadores:
            obs.atualizar(self)

    def cancelar(self):
        self.estado.cancelar(self)
        self.notificar_observadores()

    def concluir(self):
        self.estado.concluir(self)
        self.notificar_observadores()

    def modificar(self, data: date, hora_inicial: time, hora_final: time, nome_materia: str):
        self.sala.remover_reserva(self)

        original = (self.data, self.hora_inicial, self.hora_final, self.nome_materia)

        self.data = data
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.nome_materia = nome_materia

        try:
            self.sala.adicionar_reserva(self)
        except ValueError:
            self.data, self.hora_inicial, self.hora_final, self.nome_materia = original
            self.sala.adicionar_reserva(self)
            raise

        self.notificar_observadores()

    def to_dict(self) -> dict:
        return {
            "usuario": self.usuario.nome,
            "email": self.usuario.email,
            "sala": self.sala.nome,
            "data": self.data.isoformat(),
            "hora_inicial": self.hora_inicial.isoformat(),
            "hora_final": self.hora_final.isoformat(),
            "nome_materia": self.nome_materia,
            "estado": self.estado.__class__.__name__,
            "ativo": self.ativo,
        }

# Proxy Singleton
class ReservaProxy:
    _instancia = None

    def __new__(cls, usuarios_cadastrados: List["User"]):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.usuarios_cadastrados = usuarios_cadastrados
        return cls._instancia

    def fazer_reserva(self, usuario: "User", sala: Sala, data: date, hora_inicial: time, hora_final: time, nome_materia: str) -> Reserva:
        if usuario not in self.usuarios_cadastrados:
            raise PermissionError("Usuário não cadastrado. Reserva negada.")
        return Reserva.criar(usuario, sala, data, hora_inicial, hora_final, nome_materia)

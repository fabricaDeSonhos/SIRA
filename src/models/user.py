import re
import uuid
import hashlib
from abc import ABC, abstractmethod
from typing import Optional, List
from .reserva import ReservaProxy, Reserva, Sala

from enum import Enum as PyEnum
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Time, Date
from datetime import datetime, time, date
from .base import Base
# Enum para tipos de usuário
class TipoUsuario(PyEnum):
    COMUM = "comum"
    ADMIN = "admin"

tipo: Mapped[TipoUsuario] = mapped_column(SqlEnum(TipoUsuario), nullable=False)


# Validação de email
def validar_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Hash de senha
def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# Classe principal do usuário
class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(CHAR(36),primary_key=True,default=lambda: str(uuid.uuid4()),unique=True,nullable=False)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    senha: Mapped[str] = mapped_column(String, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    tipo: Mapped[TipoUsuario] = mapped_column(SqlEnum(TipoUsuario), nullable=False)

    
    reservas: Mapped[List["Reserva"]] = relationship(
        "Reserva",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    #    #configuração da tabela STI, existe apenas tabela usuarios, e nela a coluna tipo que define se é admin ou comum
    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": TipoUsuario.COMUM,
    }


    def __init__(self, nome: str, email: str, senha: str, proxy: ReservaProxy):
        if not validar_email(email):
            raise ValueError("Email inválido")
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.senha = gerar_hash_senha(senha)
        self.ativo = True
        self.tipo = TipoUsuario.COMUM
        self.proxy = proxy

    def fazer_reserva(self, sala: Sala, data: date, hora_inicial: time, hora_final: time, nome_materia: str) -> Reserva:
        return self.proxy.fazer_reserva(self, sala, data, hora_inicial, hora_final, nome_materia)

    def cancelar_reserva(self, reserva: Reserva) -> None:
        if reserva in self.reservas:
            reserva.cancelar()
            reserva.sala.remover_reserva(reserva)
        else:
            raise ValueError("Reserva não pertence a este usuário.")

    def modificar_reserva(self, reserva: Reserva, data: date, hora_inicial: time, hora_final: time, nome_materia: str) -> None:
        if reserva in self.reservas:
            reserva.modificar(data, hora_inicial, hora_final, nome_materia)
        else:
            raise ValueError("Reserva não pertence a este usuário.")


    #ser menos generalizada com, modificiar nome, modificar email e modificar senha
    def atualizar_perfil(self, nome: Optional[str] = None, email: Optional[str] = None, senha: Optional[str] = None) -> None:
        if nome:
            self.nome = nome
        if email:
            if not validar_email(email):
                raise ValueError("Email inválido")
            self.email = email
        if senha:
            self.senha = gerar_hash_senha(senha)



# Admin especializado
class Admin(User):
    #tag para banco para "isso é um admin"
    __mapper_args__ = {
        "polymorphic_identity": TipoUsuario.ADMIN,
    }
     
    def __init__(self, nome: str, email: str, senha: str, proxy: ReservaProxy):
        super().__init__(nome, email, senha, proxy)
        self.tipo = TipoUsuario.ADMIN

    def criar_reserva_fixa(self, sala: Sala, data: date, hora_inicial: time, hora_final: time, nome_materia: str) -> Reserva:
        reserva = Reserva.criar(self, sala, data, hora_inicial, hora_final, f"[FIXA] {nome_materia}")
        return reserva

    def remover_reserva_de_outro(self, usuario: "User", reserva: Reserva) -> None:
        if reserva in usuario.reservas:
            # 1) cancela o estado
            reserva.cancelar()
            # 2) remove da sala
            reserva.sala.remover_reserva(reserva)
            # 3) remove da lista de reservas do usuário
            usuario.reservas.remove(reserva)
        else:
            raise ValueError("Reserva não encontrada no usuário alvo.")
        
    def modificar_outro(self, usuario: "User", reserva: Reserva, data: date, hora_inicial: time, hora_final: time, nome_materia: str) -> None:
        if reserva in usuario.reservas:
            reserva.modificar(data, hora_inicial, hora_final, nome_materia)
        else:
            raise ValueError("Sem permissão ou reserva inválida.")

# Fábrica de usuários
class UserFactory:
    @staticmethod
    def criar_usuario(tipo: TipoUsuario, nome: str, email: str, senha: str, proxy: ReservaProxy):
        if tipo == TipoUsuario.ADMIN:
            return Admin(nome, email, senha, proxy)
        elif tipo == TipoUsuario.COMUM:
            return User(nome, email, senha, proxy)
        else:
            raise ValueError("Tipo de usuário inválido")

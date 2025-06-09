import re
import uuid
import hashlib
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List

# Import relativo dentro do pacote models
from .reserva import ReservaProxy, Reserva, Sala

# Enum de tipos de usuário
class TipoUsuario(Enum):
    COMUM = "comum"
    ADMIN = "admin"

# Validação e hash de senha (Experts)
def validar_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# Interface de Usuário (contrato de ações)
class IUser(ABC):
    @abstractmethod
    def fazer_reserva(self, sala: Sala, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> Reserva:
        pass

    @abstractmethod
    def cancelar_reserva(self, reserva: Reserva) -> None:
        pass

    @abstractmethod
    def modificar_reserva(self, reserva: Reserva, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> None:
        pass

    @abstractmethod
    def atualizar_perfil(self, nome: Optional[str] = None, email: Optional[str] = None, senha: Optional[str] = None) -> None:
        pass

# Classe base User
class User(IUser):
    def __init__(self, nome: str, email: str, senha: str, proxy: ReservaProxy):
        if not validar_email(email):
            raise ValueError("Email inválido")
        self.id = str(uuid.uuid4())
        self._nome = nome
        self._email = email
        self._senha = gerar_hash_senha(senha)
        self._status = True
        self.tipo = TipoUsuario.COMUM
        self._reservas: List[Reserva] = []
        self._proxy = proxy

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

    @property
    def reservas(self) -> List[Reserva]:
        return list(self._reservas)

    def fazer_reserva(self, sala: Sala, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> Reserva:
        reserva = self._proxy.fazer_reserva(self, sala, data, hora_inicial, hora_final, nome_materia)
        self._reservas.append(reserva)
        return reserva

    def cancelar_reserva(self, reserva: Reserva) -> None:
        if reserva in self._reservas:
            reserva.cancelar()
            reserva.sala.remover_reserva(reserva)
            self._reservas.remove(reserva)
        else:
            raise ValueError("Reserva não pertence a este usuário.")

    def modificar_reserva(self, reserva: Reserva, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> None:
        if reserva in self._reservas:
            reserva.modificar(data, hora_inicial, hora_final, nome_materia)
        else:
            raise ValueError("Reserva não pertence a este usuário.")

    def atualizar_perfil(self, nome: Optional[str] = None, email: Optional[str] = None, senha: Optional[str] = None) -> None:
        if nome:
            self._nome = nome
        if email:
            if not validar_email(email):
                raise ValueError("Email inválido")
            self._email = email
        if senha:
            self._senha = gerar_hash_senha(senha)

# Classe Admin com privilégios extras
class Admin(User):
    def __init__(self, nome: str, email: str, senha: str, proxy: ReservaProxy):
        super().__init__(nome, email, senha, proxy)
        self.tipo = TipoUsuario.ADMIN

    def criar_reserva_fixa(self, sala: Sala, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> Reserva:
        reserva = Reserva(self, sala, data, hora_inicial, hora_final, f"[FIXA] {nome_materia}")
        self._reservas.append(reserva)
        return reserva

    def remover_reserva_de_outro(self, usuario: 'User', reserva: Reserva) -> None:
        if reserva in usuario._reservas:
            usuario._reservas.remove(reserva)
            reserva.cancelar()
            reserva.sala.remover_reserva(reserva)
        else:
            raise ValueError("Reserva não encontrada no usuário alvo.")

    def modificar_outro(self, usuario: 'User', reserva: Reserva, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> None:
        if reserva in usuario._reservas:
            reserva.modificar(data, hora_inicial, hora_final, nome_materia)
        else:
            raise ValueError("Sem permissão ou reserva inválida.")


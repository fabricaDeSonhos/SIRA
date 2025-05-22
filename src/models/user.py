import re
import uuid
import hashlib
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional

# Importa a classe Reserva completa (State, Observer, status, to_dict etc.)
from .reserva import Reserva

# Enum para tipo de usuário\
class TipoUsuario(Enum):
    COMUM = "comum"
    ADMIN = "admin"

# Validação de e-mail (Expert)
def validar_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Geração de hash para senhas (Expert)
def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

# Interface de usuário (Strategy)
class IUser(ABC):
    @abstractmethod
    def fazer_reserva(self, descricao: str) -> None:
        pass

    @abstractmethod
    def cancelar_reserva(self, reserva_id: str) -> None:
        pass

    @abstractmethod
    def atualizar_perfil(self, nome: Optional[str], email: Optional[str], senha: Optional[str]) -> None:
        pass

# Classe base User (High Cohesion)
class User(IUser):
    def __init__(self, nome: str, email: str, senha: str):
        if not validar_email(email):
            raise ValueError("Email inválido")

        self.id = str(uuid.uuid4())
        self._nome = nome
        self._email = email
        self._senha = gerar_hash_senha(senha)
        self._status = True
        self._tipo = TipoUsuario.COMUM
        self._reservas: Dict[str, Reserva] = {}

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email

    @property
    def tipo(self) -> TipoUsuario:
        return self._tipo

    # Information Expert: User conhece suas reservas
    def fazer_reserva(self, descricao: str) -> None:
        reserva_id = str(uuid.uuid4())
        reserva = Reserva(reserva_id, descricao)
        self._reservas[reserva_id] = reserva
        print(f"Reserva criada com ID {reserva_id}")

    def cancelar_reserva(self, reserva_id: str) -> None:
        if reserva_id in self._reservas:
            del self._reservas[reserva_id]
            print(f"Reserva {reserva_id} cancelada.")
        else:
            print("Reserva não encontrada.")

    def atualizar_perfil(self, nome: Optional[str], email: Optional[str], senha: Optional[str]) -> None:
        if nome:
            self._nome = nome
        if email:
            if not validar_email(email):
                raise ValueError("Email inválido")
            self._email = email
        if senha:
            self._senha = gerar_hash_senha(senha)
        print("Perfil atualizado.")

    def to_dict(self) -> dict:
        #Serializa o usuário para persistência em JSON.
        return {
            "id": self.id,
            "nome": self._nome,
            "email": self._email,
            "senha": self._senha,
            "status": self._status,
            "tipo": self._tipo.value
        }

# Classe Admin, herda de User (Polymorphism)
class Admin(User):
    def __init__(self, nome: str, email: str, senha: str):
        super().__init__(nome, email, senha)
        self._tipo = TipoUsuario.ADMIN

    # Responsabilidade estendida de Admin
    def remover_reserva_usuario(self, usuario: User, reserva_id: str) -> None:
        if reserva_id in usuario._reservas:
            del usuario._reservas[reserva_id]
            print(f"Reserva {reserva_id} removida do usuário {usuario.nome}.")
        else:
            print("Reserva não encontrada para este usuário.")

    def criar_reserva_fixa(self, usuario: User, descricao: str) -> None:
        reserva_id = str(uuid.uuid4())
        reserva = Reserva(reserva_id, f"[FIXA] {descricao}")
        usuario._reservas[reserva_id] = reserva
        print(f"Reserva fixa criada com ID {reserva_id} para {usuario.nome}")

    def modificar_usuario(self, usuario: User,
                          nome: Optional[str] = None,
                          email: Optional[str] = None,
                          senha: Optional[str] = None,
                          status: Optional[bool] = None) -> None:
        if nome:
            usuario._nome = nome
        if email:
            if not validar_email(email):
                raise ValueError("Email inválido")
            usuario._email = email
        if senha:
            usuario._senha = gerar_hash_senha(senha)
        if status is not None:
            usuario._status = status
        print(f"Usuário {usuario.id} modificado com sucesso.")

# Factory Method + Singleton Pattern\
class UserFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserFactory, cls).__new__(cls)
        return cls._instance

    def criar_usuario(self, nome: str, email: str, senha: str, tipo: TipoUsuario) -> User:
        if tipo == TipoUsuario.ADMIN:
            return Admin(nome, email, senha)
        return User(nome, email, senha)

# Decorator Pattern: adiciona comportamentos dinâmicos sem alterar User
class UserDecorator(IUser):
    def __init__(self, user: IUser):
        self._user = user

    def fazer_reserva(self, descricao: str) -> None:
        self._user.fazer_reserva(descricao)

    def cancelar_reserva(self, reserva_id: str) -> None:
        self._user.cancelar_reserva(reserva_id)

    def atualizar_perfil(self, nome: Optional[str], email: Optional[str], senha: Optional[str]) -> None:
        self._user.atualizar_perfil(nome, email, senha)

    def to_dict(self) -> dict:
        return getattr(self._user, 'to_dict', lambda: {})()

# Exemplo de Decorator: registra logs antes e depois das ações
class LoggingUserDecorator(UserDecorator):
    def fazer_reserva(self, descricao: str) -> None:
        print(f"[LOG] Usuário {self._user.nome} vai criar reserva: {descricao}")
        super().fazer_reserva(descricao)
        print(f"[LOG] Reserva criada com sucesso.")

    def cancelar_reserva(self, reserva_id: str) -> None:
        print(f"[LOG] Usuário {self._user.nome} vai cancelar reserva: {reserva_id}")
        super().cancelar_reserva(reserva_id)
        print(f"[LOG] Reserva cancelada com sucesso.")

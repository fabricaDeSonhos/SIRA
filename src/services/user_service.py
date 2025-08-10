# services/user_service.py

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

# Importando todas as peças da nossa arquitetura
from models.user_models import User, Admin, Reservation
from repositories.user_repository import UserRepository
from repositories import ReservationRepository # Supondo que exista
from utils import hashing_senha

# A interface Iuser_service é conceitual. A implementação focará nas classes concretas.
# A inicialização original foi refatorada para um design mais limpo (ver __init__ abaixo).
class Iuser_service():
    def __init__(self, id: str, name: str, email: str, hashed_password: str, is_active: bool = True, reservas_usuario: list = None):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.reservas_usuario = list(reservas_usuario) if reservas_usuario is not None else []
    
    
    def atualizar_user(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")

    def get_user(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")
    
    def fazer_reserva(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")

    def cancelar_reserva(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")

    def atualizar_reserva(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")
    
    def listar_minhas_reservas(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")


class UserService:
    """
    Classe base de serviço. Orquestra as ações do usuário,
    delegando a lógica de negócio para repositórios e políticas.
    """
    def __init__(self, acting_user: User, db_session: Session):
        """
        SUGESTÃO: Injeção de Dependência.
        O serviço é inicializado com o usuário que está agindo e a sessão do DB.
        Isso desacopla o serviço dos dados estáticos.

        :param acting_user: O objeto User/Admin que está executando as ações.
        :param db_session: A sessão do SQLAlchemy para interagir com o DB.
        """
        if not acting_user:
            raise ValueError("Um usuário ativo é necessário para inicializar o serviço.")
        
        self.acting_user = acting_user
        self.db = db_session
        
        # O serviço utiliza repositórios para acessar o banco de dados
        self.user_repo = UserRepository(self.db)
        self.reservation_repo = ReservationRepository(self.db) # Supondo que este repo exista

    def get_user(self) -> Dict[str, Any]:
        """Pega/consulta as próprias informações do usuário."""
        return {
            "id": self.acting_user.id,
            "name": self.acting_user.name,
            "email": self.acting_user.email,
            "is_active": self.acting_user.is_active,
            "type": self.acting_user.type,
        }

    def atualizar_user(self, name: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """
        Atualiza o próprio usuário (nome, email ou senha).
        """
        update_data = {}
        if name:
            update_data['name'] = name
        if email:
            # A validação de email duplicado ocorreria no repositório
            update_data['email'] = email
        if password:
            # A validação de força e hashing é delegada para o módulo de hashing
            salt_hex, hash_hex = hashing_senha.hash_and_validate(password)
            update_data['salt'] = salt_hex
            update_data['hashed_password'] = hash_hex

        if not update_data:
            raise ValueError("Nenhum dado fornecido para atualização.")
            
        updated_user = self.user_repo.update_user(self.acting_user, update_data)
        self.acting_user = updated_user # Atualiza o estado do serviço
        return self.get_user()

    def fazer_reserva(self, reservation_data: Dict[str, Any]) -> Reservation:
        """
        Faz uma reserva. A verificação de permissão (política) é delegada
        para a camada de repositório/serviço da reserva.
        """
        # O ReservationRepository cuidará de chamar a ReservationPolicy
        return self.reservation_repo.create_reservation(self.acting_user, reservation_data)

    def cancelar_reserva(self, reservation_id: int) -> None:
        """
        Cancela uma reserva. As verificações (se a reserva pertence ao usuário)
        são feitas pela Política, chamada pelo repositório.
        """
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reserva não encontrada.")
            
        # O método delete do repositório deve chamar a política para garantir a permissão
        self.reservation_repo.delete(self.acting_user, reservation)

    def atualizar_reserva(self, reservation_id: int, update_data: Dict[str, Any]) -> Reservation:
        """
        Atualiza os dados de uma reserva. A permissão é verificada na camada inferior.
        """
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Reserva não encontrada.")
        
        # O método update do repositório deve chamar a política
        return self.reservation_repo.update(self.acting_user, reservation, update_data)

    def listar_minhas_reservas(self) -> List[Reservation]:
        """Lista as reservas ativas do próprio usuário."""
        return self.reservation_repo.list_by_user(user_id=self.acting_user.id, active_only=True)
    
    def __repr__(self) -> str:
        """Representação do objeto de serviço para facilitar a depuração."""
        return f"<{self.__class__.__name__} for user '{self.acting_user.email}'>"

class AdminService(UserService):
    """
    Serviço para administradores. Herda todas as funcionalidades de um usuário comum
    e adiciona métodos com privilégios elevados.
    """
    def __init__(self, acting_user: Admin, db_session: Session):
        if not isinstance(acting_user, Admin):
            raise TypeError("AdminService requer um usuário do tipo Administrador.")
        super().__init__(acting_user, db_session)

    def get_info_outros(self, target_user_id: str) -> Optional[Dict[str, Any]]:
        """Pega dados de outros usuários."""
        target_user = self.user_repo.get_by_id(target_user_id)
        if not target_user:
            return None
        # SUGESTÃO: Poderíamos ter uma UserPolicy para verificar se este admin pode ver aquele usuário
        return {
            "id": target_user.id,
            "name": target_user.name,
            "email": target_user.email,
            "is_active": target_user.is_active,
            "type": target_user.type,
        }

    def altera_info_outros(self, target_user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Muda qualquer informação de outro usuário comum.
        """
        target_user = self.user_repo.get_by_id(target_user_id)
        if not target_user:
            raise ValueError("Usuário alvo não encontrado.")
            
        # A política seria chamada aqui: self.user_policy.can_update(self.acting_user, target_user)
        
        updated_user = self.user_repo.update_user(target_user, update_data)
        return { "id": updated_user.id, "name": updated_user.name, "email": updated_user.email }

    def remover_reserva_outros(self, reservation_id: int) -> None:
        """
        Remove (desativa) a reserva de outro usuário. A política de reserva já
        concede essa permissão a administradores.
        """
        # A lógica é a mesma que cancelar a própria reserva, pois a política
        # dentro do repositório tratará a permissão do admin corretamente.
        self.cancelar_reserva(reservation_id)

    def atualizar_reserva_de_outro(self, reservation_id: int, update_data: Dict[str, Any]) -> Reservation:
        """
        Atualiza a reserva de outro usuário. A política dentro do repositório
        dará ao admin a permissão necessária.
        """
        return self.atualizar_reserva(reservation_id, update_data)

    def listar_reservas_outros(self, target_user_id: str) -> List[Reservation]:
        """
        Lista todas as reservas de outro usuário (ativas e inativas).
        """
        return self.reservation_repo.list_by_user(user_id=target_user_id, active_only=False)
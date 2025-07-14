# /services/reserva_service.py

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from ..models.user_models import User, Admin
from ..models.reserva_models import Reserva
from ..repositories.reserva_repositories import ReservaRepository
from ..policy.Reserva_Policy import ReservaPolicy # Para verificações de visualização

class ReservaService:
    """
    Camada de serviço que orquestra as operações de negócio para Reservas.
    """
    def __init__(self, acting_user: User, db_session: Session):
        self.acting_user = acting_user
        self.db = db_session
        self.repo = ReservaRepository(db_session)
        self.policy = ReservaPolicy()

    def create_reserva(self, details: str, is_fixed: bool = False) -> Reserva:
        """
        Cria uma nova reserva para o usuário logado.
        :param details: Detalhes da reserva.
        :param is_fixed: Se a reserva é fixa (requer permissão de admin).
        """
        reserva_data = {"details": details, "is_fixed": is_fixed}
        # Delega a criação e a verificação de permissão para o repositório
        return self.repo.create(self.acting_user, reserva_data)

    def get_reserva_by_id(self, reserva_id: int) -> Optional[Reserva]:
        """
        Busca uma reserva por ID e verifica se o usuário tem permissão para vê-la.
        """
        reserva = self.repo.get_by_id(reserva_id)
        if not reserva:
            return None
        
        # O serviço verifica a permissão de LEITURA
        self.policy.can_view(self.acting_user, reserva)
        return reserva

    def cancelar_reserva(self, reserva_id: int) -> Reserva:
        """
        Cancela uma reserva, tornando-a inativa.
        """
        reserva = self.get_reserva_by_id(reserva_id) # get_reserva_by_id já checa a permissão de acesso
        if not reserva:
            raise ValueError("Reserva não encontrada ou acesso negado.")

        if not reserva.is_active:
            raise ValueError("Esta reserva já está cancelada.")
            
        # A atualização também é protegida pela política no repositório
        return self.repo.update(self.acting_user, reserva, {"is_active": False})

    def listar_minhas_reservas(self) -> List[Reserva]:
        """Lista as reservas ativas do usuário logado."""
        return self.repo.list_by_user(user_id=self.acting_user.id, active_only=True)

    def listar_reservas_de_usuario(self, target_user_id: uuid.UUID) -> List[Reserva]:
        """
        (Admin-only) Lista todas as reservas (ativas e inativas) de um usuário específico.
        """
        if not isinstance(self.acting_user, Admin):
            raise PermissionError("Apenas administradores podem listar reservas de outros usuários.")
            
        return self.repo.list_by_user(user_id=target_user_id, active_only=False)
# /services/reserva_service.py

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import uuid

from ..models.user_models import User, Admin
from ..models.reserva_models import Reserva
from ..repositories.reserva_repositories import ReservaRepository
from ..policies.reserva_policy import ReservaPolicy # Para verificações de visualização

class ReservaService:
    """
    Camada de serviço que orquestra as operações de negócio para Reservas.
    """
    def __init__(self, acting_user: User, db_session: Session):
        if not acting_user:
            raise ValueError("Um usuário ativo é necessário para inicializar o serviço.")
    
        self.acting_user = acting_user
        self.db = db_session
        self.repo = ReservaRepository(db_session)
        self.policies = ReservaPolicy()

    def create_reserva(self, reserva_data: Dict[str, Any]) -> Reserva:
        """
        Cria uma nova reserva para o usuário que está agindo (acting_user).
        Este é o método padrão para usuários comuns e admins que reservam para si mesmos.
        """
        # Prepara o payload, garantindo que a reserva seja para o usuário logado.
        payload = reserva_data.copy()
        payload['user_id'] = self.acting_user.id
        
        print(f"Usuário '{self.acting_user.name}' está criando uma reserva para si mesmo.")
        
        # Chama o repositório com os dados já processados.
        return self.repo.create(self.acting_user, payload)

    def create_reserva_for_user(self, target_user_id: uuid.UUID, reserva_data: Dict[str, Any]) -> Reserva:
        """
        (Admin-only) Cria uma nova reserva em nome de outro usuário.
        
        :param target_user_id: O ID do usuário para quem a reserva será criada.
        :param reserva_data: Dicionário com os detalhes da reserva.
        """
        # --- LÓGICA DE NEGÓCIO E SEGURANÇA ---
        # 2. Se a política não levantou um erro, o serviço prossegue com a lógica de negócio
        self.policies.can_create_for_another_user(self.acting_user)

        # Prepara o payload, garantindo que a reserva seja para o usuário alvo.
        payload = reserva_data.copy()
        payload['user_id'] = target_user_id

        print(f"Admin '{self.acting_user.name}' está criando uma reserva para o usuário ID: {target_user_id}")

        # Chama o repositório com os dados processados.
        return self.repo.create(self.acting_user, payload)

    def get_reserva_by_id(self, reserva_id: uuid.UUID) -> Optional[Reserva]:
        """
        Busca uma reserva por ID e verifica se o usuário tem permissão para vê-la.
        """
        reserva = self.repo.get_by_id(reserva_id)
        if not reserva:
            return None
        
        # O serviço verifica a permissão de LEITURA
        self.policies.can_view(self.acting_user, reserva)
        return reserva

    def cancelar_reserva(self, reserva_id: uuid.UUID) -> Reserva:
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
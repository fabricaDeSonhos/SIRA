# /services/room_service.py (Versão revisada)

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from ..models.user_models import User, Admin
from ..models.room_models import Room # <-- Correção de typo: 'room_models'
from ..repositories.room_repositories import RoomRepository
from ..utils.exceptions import DuplicateRoomError # Importa a exceção

class RoomService:
    def __init__(self, db_session: Session, acting_user: Optional[User] = None):
        self.acting_user = acting_user
        self.db = db_session
        self.repo = RoomRepository(db_session)

    def list_available_rooms(self) -> List[Room]:
        """Lista todas as salas ativas. Ação pública."""
        return self.repo.list_all(active_only=True)

    def create_room(self, name: str, description: Optional[str], capacity: int) -> Room:
        """Cria uma nova sala. Ação restrita a Admins."""
        if not isinstance(self.acting_user, Admin): # Verificação mais explícita
            raise PermissionError("Apenas administradores podem criar salas.")

        room_data = {"name": name, "description": description, "capacity": capacity}
        return self.repo.create(self.acting_user, room_data)

    def update_room_details(self, room_id: int, description: Optional[str] = None, capacity: Optional[int] = None) -> Room:
        """ (NOVO) Atualiza a capacidade ou descrição de uma sala. """
        if not isinstance(self.acting_user, Admin):
            raise PermissionError("Apenas administradores podem atualizar salas.")

        room = self.repo.get_by_id(room_id)
        if not room:
            raise ValueError(f"Sala com ID {room_id} não encontrada.")

        update_data = {}
        if description is not None:
            update_data['description'] = description
        if capacity is not None:
            update_data['capacity'] = capacity
        
        if not update_data:
            raise ValueError("Nenhum dado válido para atualização foi fornecido.")

        return self.repo.update(self.acting_user, room, update_data)

    def deactivate_room(self, room_id: int) -> Room:
        """ (NOVO) Desativa uma sala, impedindo novas reservas. """
        if not isinstance(self.acting_user, Admin):
            raise PermissionError("Apenas administradores podem desativar salas.")

        room = self.repo.get_by_id(room_id)
        if not room:
            raise ValueError(f"Sala com ID {room_id} não encontrada.")
        
        if not room.is_active:
            raise ValueError("Esta sala já está desativada.")

        # Reutiliza o método de update para a desativação
        return self.repo.update(self.acting_user, room, {"is_active": False})
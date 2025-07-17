# /services/room_service.py (Novo arquivo)

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from ..models.user_models import User
from ..models.sala_models import Room
from ..repositories.room_repositories import RoomRepository

class RoomService:
    def __init__(self, db_session: Session, acting_user: Optional[User] = None):
        """
        Opcionalmente recebe um usuário para ações que exigem permissão.
        """
        self.acting_user = acting_user
        self.db = db_session
        self.repo = RoomRepository(db_session)

    def list_available_rooms(self) -> List[Room]:
        """
        Lista todas as salas ativas. Ação pública.
        """
        return self.repo.list_all(active_only=True)

    def create_room(self, name: str, description: str, capacity: int) -> Room:
        """
        Cria uma nova sala. Ação restrita a Admins.
        """
        if not self.acting_user:
            raise PermissionError("Você deve estar logado como administrador para criar uma sala.")

        room_data = {"name": name, "description": description, "capacity": capacity}
        
        # O repositório chamará a política para garantir que o usuário é um admin
        return self.repo.create(self.acting_user, room_data)
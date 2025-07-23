#
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from ..models.user_models import User
from ..models.room_models import Room
from ..policies.room_policy import RoomPolicy # <-- Correção de typo: 'policies'
from ..utils.exceptions import DuplicateRoomError # <-- MELHORIA: Exceção customizada

class RoomRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.policies = RoomPolicy()

    def get_by_id(self, room_id: int) -> Optional[Room]:
        """ (NOVO) Busca uma sala pelo seu ID. Essencial para updates. """
        return self.db.query(Room).filter(Room.id == room_id).first()

    def get_by_name(self, name: str) -> Optional[Room]:
        """Busca uma sala pelo seu nome único."""
        return self.db.query(Room).filter(Room.name == name).first()

    def list_all(self, active_only: bool = True) -> List[Room]:
        """Lista todas as salas."""
        query = self.db.query(Room)
        if active_only:
            query = query.filter(Room.is_active == True)
        return query.order_by(Room.name).all()

    def create(self, acting_user: User, room_data: Dict[str, Any]) -> Room:
        """Cria uma nova sala."""
        self.policies.can_manage(acting_user)

        if self.get_by_name(room_data['name']):
            # MELHORIA: Lança uma exceção específica em vez de ValueError.
            raise DuplicateRoomError(f"A sala com o nome '{room_data['name']}' já existe.")

        new_room = Room(**room_data)
        self.db.add(new_room)
        self.db.commit()
        self.db.refresh(new_room)
        return new_room

    def update(self, acting_user: User, room: Room, update_data: Dict[str, Any]) -> Room:
        """ (NOVO) Atualiza os dados de uma sala existente. """
        self.policies.can_manage(acting_user)

        for key, value in update_data.items():
            if hasattr(room, key) and key not in ['id', 'name']: # Não permitir mudar ID ou nome
                setattr(room, key, value)
        
        self.db.commit()
        self.db.refresh(room)
        return room
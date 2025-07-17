# /repositories/room_repositories.py (Novo arquivo)

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload

from ..models.user_models import User
from ..models.sala_models import Room
from ..policy.room_policy import RoomPolicy


class RoomRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.policy = RoomPolicy()

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
        # 1. Verifica a permissão
        self.policy.can_manage(acting_user)

        # 2. Verifica se o nome já existe
        if self.get_by_name(room_data['name']):
            raise ValueError(f"A sala com o nome '{room_data['name']}' já existe.")

        # 3. Cria e salva
        new_room = Room(**room_data)
        self.db.add(new_room)
        self.db.commit()
        self.db.refresh(new_room)
        return new_room
# /core/seeding.py (Novo arquivo)

from sqlalchemy.orm import Session
from ..repositories.room_repositories import RoomRepository

def seed_initial_rooms(db: Session):
    """
    Verifica e cria as 5 salas iniciais se elas não existirem.
    """
    print("Verificando e semeando salas iniciais...")
    repo = RoomRepository(db)
    
    initial_rooms = [
        {"name": "d01", "description": "Sala de Reunião Pequena", "capacity": 6},
        {"name": "d02", "description": "Sala de Reunião Média", "capacity": 12},
        {"name": "d03", "description": "Sala de Foco Individual", "capacity": 1},
        {"name": "d04", "description": "Auditório Pequeno", "capacity": 30},
        {"name": "d05", "description": "Sala de Brainstorming com Lousa", "capacity": 8},
    ]

    for room_data in initial_rooms:
        existing_room = repo.get_by_name(room_data["name"])
        if not existing_room:
            # Para criar salas via script, não precisamos de um "acting_user" admin,
            # pois é uma ação de confiança do sistema. Vamos chamar o db diretamente.
            new_room = Room(**room_data)
            db.add(new_room)
            print(f"Sala '{room_data['name']}' criada.")
        else:
            print(f"Sala '{room_data['name']}' já existe.")
            
    db.commit()
    print("Semeadura de salas concluída.")
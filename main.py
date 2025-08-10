# Em main.py ou onde você inicializa o Flask

# em desenvolvimento

from models.database import engine, Base
from utils.seeding import seed_initial_rooms
from sqlalchemy.orm import Session

# ... seu código de criação do app Flask ...

def init_db():
    # Cria todas as tabelas definidas nos seus modelos
    Base.metadata.create_all(bind=engine)
    
    # Abre uma sessão para popular os dados iniciais
    with Session(engine) as session:
        seed_initial_rooms(session)

if __name__ == '__main__':
    print("Inicializando banco de dados...")
    init_db()
    # app.run(...)
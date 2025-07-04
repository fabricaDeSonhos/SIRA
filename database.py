from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cria engine do banco (aqui usando SQLite, mas pode trocar por PostgreSQL etc.)
engine = create_engine("sqlite:///banco.db", echo=True)

# Base para todos os modelos
Base = declarative_base()

# Session (controle das transações)
SessionLocal = sessionmaker(bind=engine)

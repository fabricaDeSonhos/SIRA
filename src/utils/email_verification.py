import re
from sqlalchemy.orm import Session
from src.models.user_models import User  

# Expressão regular simples para validação de e-mail
EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")
"""
Exemplo de e-mails válidos com essa regex
joao@gmail.com
maria.silva@empresa.com.br
teste123@sub.dominio.org
"""

def validar_formato_email(email: str) -> bool:
    """
    Verifica se o formato do e-mail é válido usando expressão regular.
    """
    return EMAIL_RE.fullmatch(email) is not None

def email_ja_cadastrado(email: str, db: Session) -> bool:
    """
    Verifica se o e-mail já está cadastrado no banco de dados.

    :param email: E-mail a verificar
    :param db: Sessão do SQLAlchemy
    :return: True se já existir, False caso contrário
    """
    return db.query(User).filter(User.email == email).first() is not None

def verificar_email_para_cadastro(email: str, db: Session) -> None:
    """
    Valida o e-mail antes do cadastro:
    - Verifica se o formato é válido
    - Verifica se já existe no banco

    Levanta ValueError com mensagens apropriadas.
    """
    if not validar_formato_email(email):
        raise ValueError("Formato de e-mail inválido.")
    if email_ja_cadastrado(email, db):
        raise ValueError("E-mail já cadastrado. Use outro.")

import os
import re
import hmac
from typing import Tuple

from argon2.low_level import (
    hash_secret,
    verify_secret,
    Type as Argon2Type
)

# =====================
# Configurações Argon2id
# =====================
# Número de iterações (maior = mais seguro, porém mais lento)
TIME_COST = 2
# Quantidade de memória em kibibytes (maior = mais seguro contra GPU)
MEMORY_COST = 102_400  # 100 MiB
# Paralelismo (threads internas)
PARALLELISM = 8
# Tamanho do salt em bytes
SALT_SIZE = 16
# Tamanho do hash em bytes
HASH_LENGTH = 32
# Tipo de Argon2: Argon2id
ARGON2_TYPE = Argon2Type.ID

# =====================
# Regex de força de senha:
# =====================
UPPER_RE = re.compile(r'[A-Z]')
LOWER_RE = re.compile(r'[a-z]')
DIGIT_RE = re.compile(r'\d')
SPECIAL_RE = re.compile(r'[!@#$%^&*(),.?":{}|<>]')


def generate_salt(size: int = SALT_SIZE) -> bytes:
    """
    Gera um salt criptograficamente seguro.
    :param size: número de bytes no salt
    :return: salt em bytes
    """
    return os.urandom(size)


def hash_password(password: str, salt: bytes = None) -> Tuple[str, str]:
    """
    Gera hash da senha usando Argon2id com salt.

    :param password: senha em texto plain
    :param salt: salt em bytes; se None, será gerado automaticamente
    :return: tupla (salt_hex, hash_hex)
    """
    if salt is None:
        salt = generate_salt()
    # hash_secret retorna bytes brutos do hash
    hash_bytes = hash_secret(
        password.encode('utf-8'),
        salt,
        time_cost=TIME_COST,
        memory_cost=MEMORY_COST,
        parallelism=PARALLELISM,
        hash_len=HASH_LENGTH,
        type=ARGON2_TYPE
    )
    # converte para hexadecimal para armazenamento
    return salt.hex(), hash_bytes.hex()


def verify_password(password: str, salt_hex: str, hash_hex: str) -> bool:
    """
    Verifica se a senha corresponde ao hash usando o salt fornecido.

    :param password: senha plain a verificar
    :param salt_hex: salt em hexadecimal
    :param hash_hex: hash esperado em hexadecimal
    :return: True se bater, False caso contrário
    """
    salt = bytes.fromhex(salt_hex)
    expected_hash = bytes.fromhex(hash_hex)
    try:
        # recria o hash usando mesmos parâmetros
        new_hash = hash_secret(
            password.encode('utf-8'),
            salt,
            time_cost=TIME_COST,
            memory_cost=MEMORY_COST,
            parallelism=PARALLELISM,
            hash_len=len(expected_hash),
            type=ARGON2_TYPE
        )
        # compara de forma segura para evitar timing attacks
        return hmac.compare_digest(new_hash, expected_hash)
    except Exception:
        return False


def validate_password_strength(
    password: str,
    min_length: int = 8,
    require_upper: bool = True,
    require_lower: bool = True,
    require_digit: bool = True,
    require_special: bool = True
) -> bool:
    """
    Valida a força da senha de acordo com critérios básicos.

    :param password: senha a ser validada
    :param min_length: comprimento mínimo
    :param require_upper: precisa ter letra maiúscula?
    :param require_lower: precisa ter letra minúscula?
    :param require_digit: precisa ter dígito?
    :param require_special: precisa ter caractere especial?
    :return: True se todos os requisitos forem atendidos
    """
    if len(password) < min_length:
        return False
    if require_upper and not UPPER_RE.search(password):
        return False
    if require_lower and not LOWER_RE.search(password):
        return False
    if require_digit and not DIGIT_RE.search(password):
        return False
    if require_special and not SPECIAL_RE.search(password):
        return False
    return True


def hash_and_validate(password: str) -> Tuple[str, str]:
    """
    Valida a força da senha e retorna (salt_hex, hash_hex).
    Levanta ValueError se a senha for fraca.

    :param password: senha plain
    :return: (salt_hex, hash_hex)
    """
    if not validate_password_strength(password):
        raise ValueError("Senha não atende aos requisitos de segurança")
    return hash_password(password)

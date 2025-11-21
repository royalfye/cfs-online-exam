# src/services/security.py

from passlib.context import CryptContext

# Agora usamos argon2 em vez de bcrypt
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Gera o hash seguro da senha em texto puro usando Argon2.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto puro corresponde ao hash armazenado (Argon2).
    """
    return pwd_context.verify(plain_password, hashed_password)
# src/services/user_service.py

from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db.models import User


def create_user(
    db: Session,
    *,
    username: str,
    email: str,
    password_hash: str,
    full_name: str,
    birth_date: date,
    role: str,
    rank: str | None = None,
) -> User:
    """
    Cria um novo usuário no banco.

    Parâmetros:
        db: sessão de banco de dados já aberta.
        username, email, password_hash, full_name, birth_date, role, rank: dados do usuário.

    Levanta:
        ValueError: se username ou email já estiverem cadastrados.
    """
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        birth_date=birth_date,
        role=role,
        rank=rank,
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Violação de UNIQUE (provavelmente username ou email)
        raise ValueError("Username ou email já cadastrados.") from e

    db.refresh(user)  # Atualiza com dados do banco (id, created_at, etc.)
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Busca um usuário pelo username.
    Retorna o User ou None se não existir.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Busca um usuário pelo email.
    Retorna o User ou None se não existir.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Busca um usuário pelo seu ID.
    """
    return db.query(User).filter(User.id == user_id).first()
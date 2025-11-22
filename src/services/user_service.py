# src/services/user_service.py

from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db.models import User
from src.schemas.user import UserUpdate  # ← adiciona isso


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

def update_user(
    db: Session,
    user_id: int,
    user_update: UserUpdate,
) -> User | None:
    """
    Atualiza parcialmente os dados de um usuário.

    Retorna o usuário atualizado ou None se não encontrado.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    # Atualiza apenas campos enviados (não None)
    if user_update.email is not None:
        user.email = user_update.email

    if user_update.username is not None:
        user.username = user_update.username

    if user_update.full_name is not None:
        user.full_name = user_update.full_name

    if user_update.birth_date is not None:
        user.birth_date = user_update.birth_date

    if user_update.rank is not None:
        user.rank = user_update.rank

    # senha será tratada no endpoint, pois precisa de hash
    # (não mexemos aqui na password_hash)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Provavelmente conflito de email/username já existente
        raise ValueError("Email ou username já estão em uso.") from e

    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """
    Deleta um usuário do banco de dados pelo ID.

    Args:
        db: Sessão do banco de dados
        user_id: ID do usuário a ser deletado

    Returns:
        True se o usuário foi deletado, False se não foi encontrado
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return False

    db.delete(user)
    db.commit()
    return True
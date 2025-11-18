from datetime import date

from sqlalchemy.exc import IntegrityError

from src.db.database import SessionLocal
from src.db.models import User


def create_user(username: str,
                email: str,
                password_hash: str,
                full_name: str,
                birth_date: date,
                role: str,
                rank: str | None = None) -> User:
    """
    Cria um novo usuário no banco.
    Levanta exceção se username ou email já existirem.
    """
    db = SessionLocal()
    try:
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
        db.commit()
        db.refresh(user)  # Atualiza o objeto com dados do banco (id, created_at, etc.)
        return user
    except IntegrityError as e:
        db.rollback()
        # Isso acontece se username ou email já existirem (constraint UNIQUE)
        raise ValueError("Username ou email já cadastrados.") from e
    finally:
        db.close()


def get_user_by_username(username: str) -> User | None:
    """
    Busca um usuário pelo username.
    Retorna o User ou None se não existir.
    """
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()
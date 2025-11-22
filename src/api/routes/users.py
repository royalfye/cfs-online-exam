from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services import user_service
from src.services.security import hash_password
from src.schemas.user import UserCreate, UserRead
from src.services.auth import get_current_user, AdminOrInstrutorUser
from src.db.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    if user_in.username and user_in.username.strip():
        username_final = user_in.username.strip()
    else:
        username_final = user_in.email.split("@")[0]

    existing_user_by_username = user_service.get_user_by_username(db, username_final)
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso.",
        )

    existing_user_by_email = user_service.get_user_by_email(db, user_in.email)
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso.",
        )

    password_hashed = hash_password(user_in.password)

    try:
        user = user_service.create_user(
            db,
            username=username_final,
            email=user_in.email,
            password_hash=password_hashed,
            full_name=user_in.full_name,
            birth_date=user_in.birth_date,
            role=user_in.role,
            rank=user_in.rank,
        )
        return user  # ← agora está dentro do try, logo após a criação
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get("/me", response_model=UserRead)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id_endpoint(
    user_id: int,
    current_user: AdminOrInstrutorUser,  # sem default, vem antes
    db: Session = Depends(get_db),       # com default, vem depois
):
    """
    Busca um usuário pelo seu ID.

    - Apenas 'admin' ou 'instrutor' podem acessar.
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )
    return user
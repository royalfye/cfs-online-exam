from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services import user_service
from src.services.security import verify_access_token
from src.schemas.token import TokenData
from src.db.models import User
from src.schemas.roles import UserRole  # ⬅ novo import


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token, credentials_exception)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    token_data = TokenData(username=username)

    user = user_service.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


def require_role(*allowed_roles: UserRole):  # ⬅ tipado com UserRole
    async def role_checker(
        current_user: Annotated[User, Depends(get_current_user)]
    ) -> User:
        # current_user.role é string no modelo, então comparamos com .value
        if current_user.role not in {role.value for role in allowed_roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso.",
            )
        return current_user

    return role_checker


# Aliases de tipos
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]
AdminOrInstrutorUser = Annotated[
    User,
    Depends(require_role(UserRole.ADMIN, UserRole.INSTRUTOR)),
]
# src/api/routes/auth.py

from datetime import timedelta # Importar timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Importar OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.services import user_service
from src.services.security import verify_password, create_access_token # Importar create_access_token
from src.schemas.user import UserLogin, UserLoginResponse
from src.schemas.token import Token # Importar o novo schema Token (vamos criar em breve)
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES # Importar o tempo de expiração

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# Vamos mudar o response_model para Token
@router.post("/token", response_model=Token) # Mudar o path para /token e o response_model
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # Usar OAuth2PasswordRequestForm
    db: Session = Depends(get_db),
):
    """
    Realiza login de um usuário com username e senha e retorna um token JWT.

    - Busca usuário pelo username.
    - Verifica a senha usando verify_password.
    - Se falhar, retorna 401 Unauthorized.
    - Se der certo, gera um token JWT e o retorna.
    """
    user = user_service.get_user_by_username(db, form_data.username) # Buscar por username
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
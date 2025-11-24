from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr, Field
from src.schemas.roles import UserRole


class UserBase(BaseModel):
    """
    Campos comuns entre entrada e saída (sem senha).
    """
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Opcional. Se não informado, pode ser derivado do email."
    )
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=120)
    birth_date: date
    role: str = UserRole
    rank: str | None = Field(default=None, max_length=50)


class UserCreate(UserBase):
    """
    Dados necessários para criar um novo usuário.
    Inclui o campo de senha em texto puro.
    """
    password: str = Field(..., min_length=8, max_length=128)


class UserRead(UserBase):
    """
    Dados retornados pela API ao criar/buscar usuário.
    Não inclui senha.
    """
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
        # Se estivesse usando Pydantic v1: orm_mode = True

class UserLogin(BaseModel):
    """
    Dados necessários para o login de um usuário.
    Login será feito por email + senha.
    """
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserLoginResponse(BaseModel):
    """
    Resposta do endpoint de login.
    Por enquanto, devolve apenas dados básicos do usuário.
    Mais tarde podemos trocar/estender para incluir JWT.
    """
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        from_attributes = True  # permite criar a partir do objeto ORM

class UserUpdate(BaseModel):
    """
    Campos que o próprio usuário poderá atualizar.
    Não incluímos 'role' nem 'id'.
    """
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    rank: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)
# src/schemas/token.py

from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema para a resposta do token de acesso.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema para os dados contidos no token (payload).
    """
    username: str | None = None
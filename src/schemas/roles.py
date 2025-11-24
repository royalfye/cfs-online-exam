from enum import Enum


class UserRole(str, Enum):
    ALUNO = "aluno"
    INSTRUTOR = "instrutor"
    ADMIN = "admin"
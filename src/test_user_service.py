# src/test_user_service.py

from datetime import date

from src.db.database import SessionLocal
from src.services.user_service import create_user, get_user_by_username
from src.services.security import hash_password, verify_password


def main():
    db = SessionLocal()
    try:
        senha_plana = "minha_senha_super_secreta"

        # Gerar o hash da senha
        senha_hash = hash_password(senha_plana)
        print(f"Hash gerado: {senha_hash}")

        # 1) Tentar criar um usuário
        try:
            user = create_user(
                db,
                username="teste1",
                email="teste1@example.com",
                password_hash=senha_hash,
                full_name="Usuário de Teste 1",
                birth_date=date(1990, 1, 1),
                role="aluno",
                rank="CB",
            )
            print("Usuário criado com sucesso:")
            print(f"id={user.id}, username={user.username}, email={user.email}")
        except ValueError as e:
            print("Erro ao criar usuário:", e)

        # 2) Buscar o usuário pelo username
        user_busca = get_user_by_username(db, "teste1")
        if user_busca:
            print("Usuário encontrado na busca:")
            print(f"id={user_busca.id}, username={user_busca.username}, email={user_busca.email}")
            print(f"Hash armazenado: {user_busca.password_hash}")

            # 3) Testar verificação de senha (igual e diferente)
            senha_correta = verify_password(senha_plana, user_busca.password_hash)
            senha_errada = verify_password("outra_senha", user_busca.password_hash)

            print(f"Senha correta confere? {senha_correta}")
            print(f"Senha errada confere? {senha_errada}")
        else:
            print("Usuário não encontrado.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
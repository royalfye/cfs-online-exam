from datetime import date

from src.services.user_service import create_user, get_user_by_username


def main():
    # 1) Tentar criar um usuário
    try:
        user = create_user(
            username="teste1",
            email="teste1@example.com",
            password_hash="SENHA_TESTE",  # depois será hash de verdade
            full_name="Usuário de Teste 1",
            birth_date=date(1990, 1, 1),
            role="aluno",
            rank="CB"
        )
        print("Usuário criado com sucesso:")
        print(f"id={user.id}, username={user.username}, email={user.email}")
    except ValueError as e:
        print("Erro ao criar usuário:", e)

    # 2) Buscar o usuário pelo username
    user_busca = get_user_by_username("teste1")
    if user_busca:
        print("Usuário encontrado na busca:")
        print(f"id={user_busca.id}, username={user_busca.username}, email={user_busca.email}")
    else:
        print("Usuário não encontrado.")


if __name__ == "__main__":
    main()
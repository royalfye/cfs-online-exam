from src.db.database import SessionLocal
from src.db.models import User

def main():
    # Cria uma sessão
    db = SessionLocal()
    try:
        # Tenta buscar todos os usuários (vai vir lista vazia por enquanto)
        users = db.query(User).all()
        print(f"Usuarios encontrados: {len(users)}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
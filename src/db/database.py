from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session # Importar Session

DATABASE_URL = "postgresql+psycopg2://cfs_user:123456%40@localhost:5432/cfs_online_exam"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Adicionar a função get_db aqui
def get_db() -> Session:
    """
    Dependência que fornece uma sessão de banco de dados por requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
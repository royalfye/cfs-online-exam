from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# TROQUE 'SUA_SENHA_AQUI' pela senha que você definiu para o cfs_user
DATABASE_URL = "postgresql+psycopg2://cfs_user:123456%40@localhost:5432/cfs_online_exam"

# Cria a engine (conexão com o banco)
engine = create_engine(DATABASE_URL, echo=False)  # echo=True mostra as queries no console

# Fábrica de sessões do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base para os modelos
Base = declarative_base()
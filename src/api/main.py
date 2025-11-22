from fastapi import FastAPI

# Importar os routers que acabamos de criar
from src.api.routes import auth, users
from src.db.database import Base, engine # Importar Base e engine para criar as tabelas

# Criar as tabelas no banco de dados (se não existirem)
# Isso é útil para desenvolvimento, em produção você pode usar migrações (Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CFS Online Exam API")

# Incluir os routers na aplicação principal
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health")
def health_check(): # Não precisamos mais do Depends(get_db) aqui
    """
    Endpoint simples de saúde da aplicação.
    """
    return {"status": "ok"}
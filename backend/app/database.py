from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🚨 LINK DO NEON CONFIGURADO DIRETAMENTE
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_VvKxfdwh8u4g@ep-fragrant-mode-aqnkilug-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Cria o motor de conexão com a nuvem do Neon
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configura a sessão de conversação com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para a criação das tabelas
Base = declarative_base()

# Função de dependência para abrir e fechar as conexões nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
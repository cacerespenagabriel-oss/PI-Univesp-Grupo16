from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Ocorrencia(Base):
    # 🚨 FORÇA O SQLALCHEMY A USAR EXATAMENTE A TABELA DO NEON
    __tablename__ = "ocorrencias"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)
    nivel_agua = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    imagem_url = Column(String, nullable=True)
    status = Column(String, default="pendente")
    numero_morador = Column(String, nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
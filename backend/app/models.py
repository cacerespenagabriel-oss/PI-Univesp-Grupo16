from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from database import Base

class Ocorrencia(Base):
    __tablename__ = "ocorrencias"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=True)
    nivel_agua = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    imagem_url = Column(String, nullable=True)  # Campo corrigido aqui
    status = Column(String, default="pendente")
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)

class Telefone(Base):
    __tablename__ = "telefones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, index=True, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
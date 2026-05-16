from fastapi import APIRouter
from database import SessionLocal
from models import Ocorrencia

router = APIRouter(prefix="/ocorrencias")

@router.get("/")
def listar_ocorrencias():
    db = SessionLocal()
    dados = db.query(Ocorrencia).filter(Ocorrencia.status=="validada").all()
    return dados

@router.post("/")
def criar_ocorrencia(ocorrencia: dict):
    db = SessionLocal()
    nova = Ocorrencia(**ocorrencia)
    db.add(nova)
    db.commit()
    return {"status": "ok"}

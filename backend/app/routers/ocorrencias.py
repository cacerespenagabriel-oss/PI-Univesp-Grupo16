from fastapi import APIRouter
from database import SessionLocal
from models import Ocorrencia
from datetime import datetime

# 1. Definição do router (deve vir antes de usar @router)
router = APIRouter(prefix="/ocorrencias")

# 2. Rota para listar ocorrências validadas
@router.get("/validadas")
def listar_ocorrencias_validadas():
    db = SessionLocal()
    try:
        # Busca todas as ocorrências validadas no banco
        dados = db.query(Ocorrencia).filter(Ocorrencia.status == "validada").all()
        
        resultado = []
        for o in dados:
            # Construção manual do dicionário para garantir compatibilidade JSON
            resultado.append({
                "id": o.id,
                "descricao": o.descricao,
                "nivel_agua": o.nivel_agua,
                "latitude": o.latitude,
                "longitude": o.longitude,
                "status": o.status,
                "numero_morador": o.numero_morador,
                "imagem_url": o.imagem_url,
                # Garantimos a conversão da data para o formato que o JS entende
                "created_at": o.data_criacao.isoformat() if hasattr(o, 'data_criacao') and o.data_criacao else None
            })
        return resultado
    finally:
        db.close()

# 3. Rota para criar nova ocorrência
@router.post("/")
def criar_ocorrencia(ocorrencia: dict):
    db = SessionLocal()
    try:
        # Cria a instância com os dados recebidos
        nova = Ocorrencia(**ocorrencia)
        db.add(nova)
        db.commit()
        db.refresh(nova)
        return {"status": "ok", "id": nova.id}
    finally:
        db.close()
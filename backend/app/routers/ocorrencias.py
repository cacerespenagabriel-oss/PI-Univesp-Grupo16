from fastapi import APIRouter
from database import SessionLocal
from models import Ocorrencia
from datetime import datetime

# 1. Definimos o roteador
router = APIRouter(prefix="/ocorrencias")

# 2. Rota para listar (GET)
@router.get("/validadas")
def listar_ocorrencias_validadas():
    db = SessionLocal()
    try:
        dados = db.query(Ocorrencia).filter(Ocorrencia.status == "validada").all()
        resultado = []
        for o in dados:
            resultado.append({
                "id": o.id,
                "descricao": o.descricao,
                "nivel_agua": o.nivel_agua,
                "latitude": o.latitude,
                "longitude": o.longitude,
                # Forçamos a data aqui. Se 'o.data_criacao' for None, 
                # vamos usar o tempo atual como plano B para não quebrar o front
                #
                "created_at": o.data_criacao.isoformat() if o.data_criacao else datetime.utcnow().isoformat()
            })
        return resultado
    finally:
        db.close()

# 3. Rota para CRIAR (POST) - É AQUI QUE VOCÊ COLOCA O NOVO CÓDIGO!
@router.post("/")
def criar_ocorrencia(ocorrencia_data: dict):
    db = SessionLocal()
    try:
        # Criamos a instância do modelo
        nova_ocorrencia = Ocorrencia(**ocorrencia_data)
        
        # O SQLAlchemy usa o valor default definido no models.py (datetime.utcnow)
        # se você não passar a data no JSON de entrada.
        db.add(nova_ocorrencia)
        db.commit()
        db.refresh(nova_ocorrencia)
        return {"status": "ok", "id": nova_ocorrencia.id}
    finally:
        db.close()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from services.alerta_automatico import executar_alerta

router = APIRouter(prefix="/alertas", tags=["Alertas e Notificações"])

# Esquema do Pydantic para validar a entrada do telefone
class TelefoneCreate(BaseModel):
    numero: str

@router.get("/status")
def status_regiao():
    risco, nivel = executar_alerta(simulacao=True)
    return {"risco": risco, "nivel": nivel}

@router.post("/telefones")
def cadastrar_telefone(telefone: TelefoneCreate, db: Session = Depends(get_db)):
    # Verifica se o telefone já está cadastrado
    existe = db.query(models.Telefone).filter(models.Telefone.numero == telefone.numero).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este telefone já está cadastrado.")
    
    novo_telefone = models.Telefone(numero=telefone.numero)
    db.add(novo_telefone)
    db.commit()
    db.refresh(novo_telefone)
    return {"status": "sucesso", "mensagem": "Telefone cadastrado para alertas!", "id": novo_telefone.id}

@router.get("/telefones")
def listar_telefones(db: Session = Depends(get_db)):
    telefones = db.query(models.Telefone).all()
    return telefones
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import models
import os
from database import engine, SessionLocal
from services.alerta_automatico import executar_alerta
from services.whatsapp_service import receber_relato_whatsapp

# Garante a criação das tabelas no banco SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Alerta de Alagamentos - Anhaia Mello",
    description="API para monitoramento preditivo de 1h de antecedência e recepção de imagens via WhatsApp."
)

# CONFIGURAÇÃO INTELIGENTE DE CAMINHO (Evita erro 500 e 404)
# Detecta se o servidor foi iniciado de dentro da pasta 'app' ou da raiz 'backend'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR) == "app":
    templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
else:
    templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app", "templates"))

# Esquemas de Validação (Pydantic)
class TelefoneCreate(BaseModel):
    numero: str

class OcorrenciaCreate(BaseModel):
    descricao: str
    nivel_agua: str
    latitude: float
    longitude: float
    imagem_url: Optional[str] = None

class OcorrenciaResponse(BaseModel):
    id: int
    descricao: str
    nivel_agua: str
    latitude: float
    longitude: float
    imagem_url: Optional[str]
    status: str
    
    class Config:
        from_attributes = True

class WhatsAppMessageInput(BaseModel):
    numero_morador: str
    latitude: float
    longitude: float
    imagem_url: str

# Dependência do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS DA APLICAÇÃO ---

@app.get("/", response_class=HTMLResponse)
def abrir_painel_mapa(request: Request):
    """Página principal do aplicativo que renderiza o painel com o mapa geográfico."""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        return HTMLResponse(
            content=f"<h3>Erro ao carregar o template: {str(e)}</h3><p>Verifique se o arquivo index.html está dentro da pasta app/templates/</p>", 
            status_code=500
        )

@app.get("/alertas/status")
def obter_status_alerta():
    """Analisa a previsão meteorológica para alertar com antecedência."""
    risco, nivel = executar_alerta()
    return {"risco": round(risco, 2), "nivel": nivel}

@app.post("/ocorrencias/webhook-whatsapp", response_model=OcorrenciaResponse, status_code=status.HTTP_201_CREATED)
def webhook_whatsapp_receber_relato(payload: WhatsAppMessageInput, db: Session = Depends(get_db)):
    """Recebe o relato (localização e foto) enviado pelo morador via WhatsApp."""
    dados_relato = receber_relato_whatsapp(
        payload.numero_morador, payload.latitude, payload.longitude, payload.imagem_url
    )
    nova_ocorrencia = models.Ocorrencia(**dados_relato)
    db.add(nova_ocorrencia)
    db.commit()
    db.refresh(nova_ocorrencia)
    return nova_ocorrencia

@app.get("/ocorrencias/validadas", response_model=List[OcorrenciaResponse])
def listar_ocorrencias_validadas(db: Session = Depends(get_db)):
    """Retorna apenas os pontos de alagamento confirmados pela Defesa Civil."""
    return db.query(models.Ocorrencia).filter(models.Ocorrencia.status == "validada").all()

@app.patch("/ocorrencias/{ocorrencia_id}/validar", response_model=OcorrenciaResponse)
def validar_ocorrencia(ocorrencia_id: int, status_validacao: str, db: Session = Depends(get_db)):
    """Defesa Civil analisa a imagem e valida ou recusa o ponto."""
    if status_validacao not in ["validada", "recusada"]:
        raise HTTPException(status_code=400, detail="Status inválido. Use 'validada' ou 'recusada'.")
    
    ocorrencia = db.query(models.Ocorrencia).filter(models.Ocorrencia.id == ocorrencia_id).first()
    if not ocorrencia:
        raise HTTPException(status_code=404, detail="Ocorrência não encontrada.")
    
    ocorrencia.status = status_validacao
    db.commit()
    db.refresh(ocorrencia)
    return ocorrencia

@app.post("/moradores/cadastro")
def cadastrar_telefone(telefone: TelefoneCreate, db: Session = Depends(get_db)):
    """Cadastra moradores para receberem as notificações preditivas."""
    existe = db.query(models.Telefone).filter(models.Telefone.numero == telefone.numero).first()
    if existe:
        return {"status": "já cadastrado"}
    novo = models.Telefone(numero=telefone.numero)
    db.add(novo)
    db.commit()
    return {"status": "sucesso"}
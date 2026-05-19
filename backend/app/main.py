from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Importações de escopo local (Correto)
from database import SessionLocal, engine, get_db
import models

# 1. Cria as tabelas no Neon
models.Base.metadata.create_all(bind=engine)

# 2. Inicializa o objeto 'app' ANTES de criar as rotas (Resolve o NameError!)
app = FastAPI(
    title="Sistema de Alerta de Alagamentos - Vila Prudente",
    description="API para monitoramento de enchentes na região da Anhaia Mello para o Projeto Integrador I",
    version="1.0.0"
)

# 3. Configura o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# ==============================================================================
# ROTAS DO SISTEMA
# ==============================================================================

# Rota da página principal
@app.get("/")
def acessar_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Rota que lista todas as ocorrências
@app.get("/ocorrencias/validadas")
def listar_ocorrencias(db: Session = Depends(get_db)):
    try:
        ocorrencias = db.query(models.Ocorrencia).all()
        return ocorrencias
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados no Neon: {str(e)}")


# Rota do Webhook com o Print de Debug do Akita para pegar erros do banco
@app.post("/ocorrencias/webhook-whatsapp", status_code=201)
def receber_relato_whatsapp(ocorrencia: dict, db: Session = Depends(get_db)):
    print("\n=== [DEBUG AKITA] DADOS RECEBIDOS DO SWAGGER ===")
    print(ocorrencia)
    print("================================================\n")
    
    try:
        nova_ocorrencia = models.Ocorrencia(
            descricao=ocorrencia.get("descricao"),
            nivel_agua=ocorrencia.get("nivel_agua"),
            latitude=ocorrencia.get("latitude"),
            longitude=ocorrencia.get("longitude"),
            imagem_url=ocorrencia.get("imagem_url"),
            status=ocorrencia.get("status", "pendente"),
            numero_morador=ocorrencia.get("numero_morador")
        )
        
        print("-> Tentando adicionar ao banco...")
        db.add(nova_ocorrencia)
        
        print("-> Tentando dar o commit...")
        db.commit()
        
        print("-> Atualizando objeto...")
        db.refresh(nova_ocorrencia)
        
        print(f"-> SUCESSO ABSOLUTO! Gravado com ID: {nova_ocorrencia.id}")
        return {"status": "sucesso", "id": nova_ocorrencia.id}
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ ERRO CRÍTICO NO BANCO: {str(e)}\n")
        raise HTTPException(status_code=500, detail=f"Erro interno de banco: {str(e)}")
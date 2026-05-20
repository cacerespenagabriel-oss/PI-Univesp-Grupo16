from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

# Importações do núcleo
from database import engine
import models

# Importações dos roteadores
from routers import alertas, ocorrencias

# 1. Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# 2. Inicialização do App
app = FastAPI(
    title="Sistema de Alerta de Alagamentos - Anhaia Mello",
    description="Monitoramento colaborativo e preditivo - Projeto Integrador UNIVESP",
    version="1.0.0"
)

# 3. Configuração de CORS (Essencial para o front acessar o back)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Caminho do arquivo HTML (Certifique-se que o arquivo está na pasta 'templates')
BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML = BASE_DIR / "templates" / "validadas.html"

# ==============================================================================
# ROTAS DE INTERFACE (FRONTEND)
# ==============================================================================

@app.get("/", summary="Painel de Monitoramento")
def acessar_home():
    """Entrega a interface do mapa (validadas.html) na raiz."""
    if not INDEX_HTML.exists():
        return {"erro": "Arquivo templates/validadas.html não encontrado no servidor."}
    return FileResponse(str(INDEX_HTML))

# ==============================================================================
# ROTEADORES DE DADOS (BACKEND)
# ==============================================================================

# As rotas de dados (/alertas/status, /ocorrencias/validadas, etc)
# são gerenciadas aqui:
app.include_router(alertas.router)
app.include_router(ocorrencias.router)

# Dica: Se quiser testar se a API está rodando, adicione um endpoint de health check:
@app.get("/health")
def health_check():
    return {"status": "online", "projeto": "Anhaia Mello - UNIVESP"}
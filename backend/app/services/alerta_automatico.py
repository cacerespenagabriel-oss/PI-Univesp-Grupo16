from services.chuva_service import buscar_chuva_inmet
from services.risco_service import calcular_risco
from services.whatsapp_service import enviar_alerta_whatsapp  # Trocado para WhatsApp
from database import SessionLocal
import models

def executar_alerta(simulacao=False):
    # 1. Puxa os dados climáticos em tempo real da API (incluindo previsão de curto prazo)
    chuva_3h, chuva_24h, chuva_prev_2h = buscar_chuva_inmet()

    # 2. Conecta ao banco SQLite local e conta os relatos validados com imagem
    db = SessionLocal()
    try:
        alagamentos_ativos = db.query(models.Ocorrencia).filter(models.Ocorrencia.status == "validada").count()
    except Exception as e:
        print(f"⚠️ Erro ao ler tabela de Ocorrências no SQLite: {e}")
        alagamentos_ativos = 0

    # 3. Processa o algoritmo matemático de cálculo de risco
    risco = calcular_risco(chuva_3h, chuva_24h, chuva_prev_2h, alagamentos_ativos)

    nivel = (
        "BAIXO" if risco <= 30 else
        "ATENÇÃO" if risco <= 60 else
        "ALERTA" if risco <= 80 else
        "EMERGÊNCIA"
    )

    # 4. DISPARO DE WHATSAPP ANTECIPADO: Se a previsão detetar perigo para a próxima 1 hora
    if risco >= 60 or nivel in ["ALERTA", "EMERGÊNCIA"]:
        try:
            mensagem = f"⚠️ ALERTA PREVENTIVO DEFESA CIVIL (Anhaia Mello): Previsão de forte chuva com risco de alagamento nos próximos 60 minutos. Evite a região! Risco calculado: {risco}%."
            telefones = db.query(models.Telefone).all()
            for t in telefones:
                enviar_alerta_whatsapp(mensagem, t.numero)
        except Exception as e:
            print(f"⚠️ Erro ao enviar notificações via WhatsApp: {e}")

    db.close()
    return risco, nivel
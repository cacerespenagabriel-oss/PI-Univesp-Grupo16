from services.chuva_service import buscar_chuva_inmet
from services.risco_service import calcular_risco
from services.whatsapp_service import enviar_alerta_whatsapp  
from database import SessionLocal
import models

def executar_alerta(simulacao=False):
    # 1. Puxa os dados climáticos em tempo real da API (incluindo previsão de curto prazo)
    chuva_3h, chuva_24h, chuva_prev_2h = buscar_chuva_inmet()

    # 2. Conecta ao banco Neon na nuvem e conta os relatos pendentes ou ativos
    db = SessionLocal()
    try:
        # Busca "pendente", "validada" ou "Ativo" para validar seu teste do Neon
        alagamentos_ativos = db.query(models.Ocorrencia).filter(
            models.Ocorrencia.status.in_(["validada", "pendente", "Ativo"])
        ).count()
    except Exception as e:
        print(f"⚠️ Erro ao ler tabela de Ocorrências no Neon: {e}")
        alagamentos_ativos = 0

    # 3. Processa o algoritmo matemático de cálculo de risco
    risco = calcular_risco(chuva_3h, chuva_24h, chuva_prev_2h, alagamentos_ativos)

    nivel = (
        "BAIXO" if risco <= 30 else
        "ATENÇÃO" if risco <= 60 else
        "ALERTA" if risco <= 80 else
        "EMERGÊNCIA"
    )

    print(f"\n📊 [LOG AUTOMÁTICO] Ocorrências no Banco: {alagamentos_ativos} | Risco: {risco}% | Nível: {nivel}")

    # 4. DISPARO DE WHATSAPP ANTECIPADO: Se a previsão detetar perigo
    if risco >= 60 or nivel in ["ALERTA", "EMERGÊNCIA"]:
        try:
            mensagem = f"⚠️ ALERTA PREVENTIVO DEFESA CIVIL (Anhaia Mello): Previsão de forte chuva com risco de alagamento nos próximos 60 minutos. Evite a região! Risco calculated: {risco}%."
            telefones = db.query(models.Telefone).all()
            print(f"📱 Encontrados {len(telefones)} telefones cadastrados para envio.")
            for t in telefones:
                enviar_alerta_whatsapp(mensagem, t.numero)
        except Exception as e:
            print(f"⚠️ Erro ao enviar notificações via WhatsApp: {e}")

    db.close()
    return risco, nivel

# Bloco de teste local para simular a tomada de decisão do sistema
if __name__ == "__main__":
    print("🤖 Iniciando o motor de monitoramento automático...")
    executar_alerta()
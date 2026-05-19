import requests
from datetime import datetime

def buscar_chuva_inmet():
    """
    Busca o volume de chuva passado (3h e 24h) e a previsão para as 
    climas/próximas 2h na Vila Prudente/Anhaia Melo usando a API da Open-Meteo.
    """
    LATITUDE = -23.5812
    LONGITUDE = -46.5834
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=rain&timezone=America/Sao_Paulo&past_days=1"
    
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        
        horas = dados["hourly"]["time"]
        chuva_por_hora = dados["hourly"]["rain"]
        
        agora_str = datetime.now().strftime("%Y-%m-%dT%H:00")
        
        if agora_str in horas:
            indice_atual = horas.index(agora_str)
        else:
            indice_atual = len(horas) - 1

        # Cortes para pegar o histórico passado
        idx_3h = max(0, indice_atual - 3)
        idx_24h = max(0, indice_atual - 24)
        
        # Corte para pegar o futuro (próximas 2 horas)
        idx_prev_2h = min(len(chuva_por_hora), indice_atual + 3)
        
        # Cálculos dos acumulados e da previsão futura
        acumulado_3h = sum(chuva_por_hora[idx_3h:indice_atual])
        acumulado_24h = sum(chuva_por_hora[idx_24h:indice_atual])
        previsao_2h = sum(chuva_por_hora[indice_atual+1:idx_prev_2h])
        
        return round(acumulado_3h, 2), round(acumulado_24h, 2), round(previsao_2h, 2)
        
    except Exception as e:
        print(f"⚠️ Erro ao acessar API de clima (Open-Meteo): {e}")
        # Retorno de segurança caso o serviço caia
        return 0.0, 0.0, 0.0

# Bloco de teste local para validação instantânea
if __name__ == "__main__":
    print("\n⏳ Buscando dados de chuva ao vivo na Open-Meteo para a Vila Prudente...")
    acum_3h, acum_24h, prev_2h = buscar_chuva_inmet()
    print("-" * 50)
    print(f"🌧️  Acumulado das últimas 3 horas:  {acum_3h} mm")
    print(f"🌧️  Acumulado das últimas 24 horas: {acum_24h} mm")
    print(f"🔮 Previsão para as próximas 2 horas: {prev_2h} mm")
    print("-" * 50)
def calcular_risco(chuva_3h, chuva_24h, chuva_prev_2h, alagamentos_ativos):
    risco = (chuva_3h * 0.4) + \
            (chuva_24h * 0.2) + \
            (chuva_prev_2h * 0.3) + \
            (alagamentos_ativos * 10)

    return min(risco, 100)

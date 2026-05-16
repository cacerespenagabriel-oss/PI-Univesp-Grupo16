import datetime

def enviar_alerta_whatsapp(mensagem: str, numero_morador: str):
    """
    Simula o envio de uma notificação ativa de emergência via WhatsApp API.
    Disparado com antecedência de 1 hora com base na previsão meteorológica.
    """
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print("\n" + "="*60)
    print(f"🟢 [WHATSAPP OUTBOUND] -> Enviado para: {numero_morador} às {timestamp}")
    print(f"💬 Mensagem: {mensagem}")
    print("="*60 + "\n")

def receber_relato_whatsapp(numero_morador: str, latitude: float, longitude: float, imagem_url: str):
    """
    Simula o recebimento de um relato de alagamento enviado por um morador via WhatsApp.
    O morador envia a localização em tempo real e a foto da via inundada.
    """
    print("\n" + "#"*60)
    print(f"📥 [WHATSAPP INBOUND] -> Relato recebido de: {numero_morador}")
    print(f"📍 Coordenadas: Lat {latitude}, Lng {longitude}")
    print(f"📸 Link da Imagem recebida: {imagem_url}")
    print("#"*60 + "\n")
    
    # Retorna os dados estruturados prontos para serem injetados no banco via rota
    return {
        "descricao": f"Relato via WhatsApp enviado pelo morador do número {numero_morador}",
        "nivel_agua": "alto",
        "latitude": latitude,
        "longitude": longitude,
        "imagem_url": imagem_url
    }
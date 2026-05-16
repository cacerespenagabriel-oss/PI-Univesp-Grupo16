from twilio.rest import Client

def enviar_alerta(mensagem, telefone):
    SID = "SEU_SID"
    TOKEN = "SEU_TOKEN"
    client = Client(SID, TOKEN)

    # WhatsApp
    client.messages.create(
        body=mensagem,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:+55{telefone}'
    )

    # SMS
    client.messages.create(
        body=mensagem,
        from_='+1XXXXXXXXXX',
        to=f'+55{telefone}'
    )

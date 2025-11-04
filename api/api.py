import requests
import json

def enviar(url, dados):
    resposta = requests.post(url, data=dados)
    status = resposta.status_code

    try:
        corpo = json.dumps(resposta.json(), indent=2, ensure_ascii=False)
    except:
        corpo = resposta.text
    
    return status, corpo

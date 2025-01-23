import os
import json

import requests
from dotenv import load_dotenv

load_dotenv()

#url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
baseUrl = 'https://gigachat.devices.sberbank.ru/api/v1'

def get_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload='scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': os.getenv('CLIENT_SECRET'),
        'Authorization': f'Basic {os.getenv("AUTHORIZATION_KEY")}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')

    return response.json()

def get_answer(text, access_token):
    payload = json.dumps({
        "model": "GigaChat", #есть еще GigaChat-Pro (50к бесплатных) и GigaChat-Plus (платный)
        "messages": [
            {
            "role": "user",
            "content": text #ваш запрос
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 100, #максимальное кол-во использованных токенов
        "repetition_penalty": 1
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' #токен доступа
    }
    
    response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')

    return response.json()

def get_models():
    url = f'{baseUrl}/models'
    
    payload = {}
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' #токен доступа
    }
    
    response = requests.request("POST", url, headers=headers, data=payload, verify='chain.pem')

    return response.json()

#print(get_token())

#print(get_answer('Расскажи что ты умеешь', os.getenv('access_token')))
#print(os.getenv('access_token'))

print(get_token())
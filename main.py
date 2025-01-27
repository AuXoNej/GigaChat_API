import os
import json
import logging

import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
baseUrl = 'https://gigachat.devices.sberbank.ru/api/v1'

def get_token():
    url_authorization = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload='scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': os.getenv('CLIENT_SECRET'),
        'Authorization': f'Basic {os.getenv("AUTHORIZATION_KEY")}'
    }

    response = requests.request("POST", url_authorization, headers=headers, data=payload, verify='chain.pem')

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

def get_models(access_token):
    url = f'{baseUrl}/models'
    url = 'https://gigachat.devices.sberbank.ru/api/v1/models'
    
    payload = {}
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}' #токен доступа
    }
    
    response = requests.request(
        "GET",
        url,
        headers=headers,
        data=payload,
        verify='chain.pem'
    )

    return response.json()

#print(get_token())

#print(get_answer('Расскажи что ты умеешь', os.getenv('access_token')))
#print(os.getenv('access_token'))
def save_token(response):
    #file_cache = open('cache.txt')
    with open('cache.txt') as file_cache:
        # Конвертация в Unix-таймштамп
        datetime_now_to_unix = int(datetime.now().timestamp())
        datetime_cache_to_unix = file_cache.readline()
        if datetime_cache_to_unix != '' and (int(datetime_cache_to_unix) > datetime_now_to_unix):
            logging.info(f'Берем токен аторизации из кеша')
            return file_cache.readline()
    try:
        response_get_token = get_token()
        access_token = response_get_token['access_token']
        time_expiration_token = str(response_get_token['expires_at'])[:-3]
        
        logging.info(f'Токен аторизации получен: {access_token[:20]}...')
        logging.info(f'Время окончания действия токена:{time_expiration_token}')
        
        with open('cache.txt', 'w') as file_cache:
            file_cache.write(f'{time_expiration_token}\n{access_token}')
            
        logging.info('Записали токен и время его действия в кеш')

        return access_token

    except Exception as error:
        logging.error(f'Не удалось получить токен авторизации: {error}')
        raise error
    

def get_count_tokens(access_token):
    url = "https://gigachat.devices.sberbank.ru/api/v1/tokens/count"

    payload = json.dumps({
      "model": "GigaChat",
      "input": [
        "Расскажи что ты умеешь"
      ]
    })
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.request(
        'POST',
        url,
        headers=headers,
        data=payload,
        verify='chain.pem'
    )
    
    print(response.text)

def get_balance(access_token):

    url = "https://gigachat.devices.sberbank.ru/api/v1/balance"
    
    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.request(
        'GET',
        url,
        headers=headers,
        data=payload,
        verify='chain.pem'
    )
    return response.json()

print(get_count_tokens(save_token(get_token())))
#print(get_models(save_token(get_token())))
#print(int(datetime.now().timestamp()))

#1737709137411

#1737710185.588596

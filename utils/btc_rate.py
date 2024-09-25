import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import aiogram_bot
import requests
from fake_useragent import UserAgent

previous_btc_usd = 0

# Прокси (по желанию)
USE_PROXY = True  # Установите False, если не хотите использовать прокси
PROXY_URL = "http://r86wCP:8ueGf5@194.45.34.190:8000"


async def try_get_rate():
    global previous_btc_usd  # Глобальная переменная для сравнения

    # Обновляем URL, добавив etherium и ton
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,toncoin&vs_currencies=usd,rub"

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    proxies = {
        'http': PROXY_URL,
        'https': PROXY_URL
    } if USE_PROXY else None

    response = requests.get(url, headers=headers, proxies=proxies)
    data = response.json()

    # Получаем данные по биткоину
    btc_usd = data["bitcoin"]["usd"]
    btc_rub = data["bitcoin"]["rub"]

    # Получаем данные по etherium
    eth_usd = data["ethereum"]["usd"]
    eth_rub = data["ethereum"]["rub"]

    # Получаем данные по toncoin
    ton_usd = data["toncoin"]["usd"]
    ton_rub = data["toncoin"]["rub"]

    # Форматируем данные
    btc_usd = '{:,.2f}'.format(btc_usd).replace(',', ' ')
    btc_rub = '{:,.2f}'.format(btc_rub).replace(',', ' ')
    eth_usd = '{:,.2f}'.format(eth_usd).replace(',', ' ')
    eth_rub = '{:,.2f}'.format(eth_rub).replace(',', ' ')
    ton_usd = '{:,.2f}'.format(ton_usd).replace(',', ' ')
    ton_rub = '{:,.2f}'.format(ton_rub).replace(',', ' ')

    # Ограничиваем длину строк и убираем лишние точки
    btc_usd, btc_rub = btc_usd[:6].rstrip('.'), btc_rub[:9].rstrip('.')
    eth_usd, eth_rub = eth_usd[:6].rstrip('.'), eth_rub[:9].rstrip('.')
    ton_usd, ton_rub = ton_usd[:6].rstrip('.'), ton_rub[:9].rstrip('.')

    # Генерируем сообщение
    msg = (
        f'💰 <b>1 BTC</b> | 🇺🇸 <b>${btc_usd[:6]}</b> | 🇷🇺 <b>₽{btc_rub[:9]}</b>\n'
        f'💰 <b>1 ETH</b> | 🇺🇸 <b>${eth_usd[:6]}</b> | 🇷🇺 <b>₽{eth_rub[:9]}</b>\n'
        f'💰 <b>1 TON</b> | 🇺🇸 <b>${ton_usd[:6]}</b> | 🇷🇺 <b>₽{ton_rub[:9]}</b>'
    )

    print(msg)
    return msg


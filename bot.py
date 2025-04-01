import logging
import requests
import time
import schedule
from telegram import Bot
from telegram.error import TelegramError
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен бота и ID чата из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
CUSTOM_SIGNATURE = os.getenv('CUSTOM_SIGNATURE', '')
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 5))

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Глобальные переменные для хранения предыдущих значений курсов
previous_ton_price = None
previous_usdt_rub = None
previous_freenet_price = None

# Функция для получения курса TON/USDT
def get_ton_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd')
        data = response.json()
        return data['the-open-network']['usd']
    except Exception as e:
        logger.error(f"Ошибка при получении курса TON: {e}")
        return None

# Функция для получения курса FREENET/USDT
def get_freenet_price():
    try:
        # Используем API GeckoTerminal для получения данных о пуле ликвидности
        pool_address = "EQBUxfy9mTrgRhVVJZ-DzyD7Ha_YNfRIx7TTOdsEsGfr7YQk"
        response = requests.get(f"https://api.geckoterminal.com/api/v2/networks/ton/pools/{pool_address}")
        data = response.json()
        
        # Извлекаем цену из ответа API
        base_token_price_usd = float(data['data']['attributes']['base_token_price_usd'])
        return base_token_price_usd
    except Exception as e:
        logger.error(f"Ошибка при получении курса FREENET: {e}")
        return None

# Функция для получения курса USDT/RUB
def get_usdt_rub_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=rub')
        data = response.json()
        return data['tether']['rub']
    except Exception as e:
        logger.error(f"Ошибка при получении курса USDT/RUB: {e}")
        return None

# Функция для расчета процентного изменения
def calculate_percentage_change(current, previous):
    if previous is None or current is None:
        return None
    return ((current - previous) / previous) * 100

# Функция для отправки сообщения с курсами
def send_crypto_rates():
    global previous_ton_price, previous_usdt_rub, previous_freenet_price
    
    try:
        ton_price = get_ton_price()
        freenet_price = get_freenet_price()
        usdt_rub = get_usdt_rub_price()
        
        # Расчет курсов в рублях
        if ton_price and usdt_rub:
            ton_rub = ton_price * usdt_rub
        else:
            ton_rub = None
            
        if freenet_price and usdt_rub:
            freenet_rub = freenet_price * usdt_rub
        else:
            freenet_rub = None
        
        # Расчет процентного изменения
        ton_change = calculate_percentage_change(ton_price, previous_ton_price)
        freenet_change = calculate_percentage_change(freenet_price, previous_freenet_price)
        
        # Формирование компактного сообщения
        message = []
        
        # Добавляем информацию о TON
        ton_line = f"💎 $TON: {ton_price:.3f}$ / {ton_rub:.3f}₽"
        if ton_change is not None:
            change_emoji = "⬆️" if ton_change >= 0 else "⬇️"
            ton_line += f" {change_emoji} {abs(ton_change):.2f}%"
        message.append(ton_line)
        
        # Добавляем курс USDT/RUB
        message.append(f"💵 USDT/RUB: {usdt_rub:.2f}₽")
        
        # Добавляем курс FREENET
        if freenet_price and freenet_rub:
            freenet_line = f"🌐 $FREENET: {freenet_price:.6f}$ / {freenet_rub:.6f}₽"
            if freenet_change is not None:
                change_emoji = "⬆️" if freenet_change >= 0 else "⬇️"
                freenet_line += f" {change_emoji} {abs(freenet_change):.2f}%"
            message.append(freenet_line)
        else:
            message.append("🌐 $FREENET: Н/Д")
        
        # Объединяем все строки и добавляем подпись
        final_message = "\n\n".join(message)
        if CUSTOM_SIGNATURE:
            final_message += f"\n\n{CUSTOM_SIGNATURE}"
        
        # Отправка сообщения
        bot.send_message(
            chat_id=CHAT_ID, 
            text=final_message, 
            parse_mode='Markdown',
            disable_web_page_preview=True  # Отключаем предпросмотр ссылок
        )
        
        # Сохранение текущих значений для следующего сравнения
        previous_ton_price = ton_price
        previous_usdt_rub = usdt_rub
        previous_freenet_price = freenet_price
        
        logger.info("Сообщение с курсами успешно отправлено")
    except TelegramError as e:
        logger.error(f"Ошибка Telegram при отправке сообщения: {e}")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")

# Функция для запуска планировщика
def run_scheduler():
    # Отправляем сообщение сразу при запуске
    send_crypto_rates()
    
    # Планируем отправку с заданным интервалом
    schedule.every(UPDATE_INTERVAL).minutes.do(send_crypto_rates)
    
    logger.info(f"Планировщик запущен. Сообщения будут отправляться каждые {UPDATE_INTERVAL} минут.")
    
    # Бесконечный цикл для выполнения запланированных задач
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    logger.info("Бот запущен")
    run_scheduler() 
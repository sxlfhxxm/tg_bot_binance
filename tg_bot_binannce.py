import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price'


async def get_price(symbol):
    response = requests.get(f"{BINANCE_API_URL}?symbol={symbol}")
    if response.status_code == 200:
        return float(response.json()['price'])
    return None


async def check_price_changes():
    while True:
        # Отримання курсу двох криптовалют (наприклад, BTC та ETH)
        btc_price = await get_price('BTCUSDT')
        eth_price = await get_price('ETHUSDT')

        # Перевірка зміни курсу більше ніж на 5%
        if btc_price and eth_price and abs(btc_price - eth_price) / eth_price > 0.05:
            message = f"Ціна Bitcoin: {btc_price} USD\nЦіна Ethereum: {eth_price} USD"
            await bot.send_message(chat_id='', text=message, parse_mode=ParseMode.HTML)

        # Очікування перед наступною перевіркою (наприклад, кожні 5 хвилин)
        await asyncio.sleep(300)  # Час у секундах


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привіт! Я тут, щоб сповіщувати тебе про зміни ціни криптовалют!")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_price_changes())
    executor.start_polling(dp, skip_updates=True)

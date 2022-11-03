import aiogram
from modules.config import TOKEN

bot = aiogram.Bot(TOKEN, parse_mode=aiogram.types.ParseMode.HTML)
dp = aiogram.Dispatcher(bot)

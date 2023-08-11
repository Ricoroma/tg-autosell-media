from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import *

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

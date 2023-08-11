from nu import dp
from aiogram import executor
from data.db import check_db
print(dp.message_handlers.handlers)
check_db()
executor.start_polling(dp)

from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data.loader import bot
import data.config as config


# проверка на подписку канала
class IsSub(BoundFilter):
    async def check(self, message: Message):
        channels = config.sub_channels
        for channel_id in channels:
            try:
                channel_id = int(channel_id)
                user_status = await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)
                if user_status["status"] == 'left':
                    return True
                else:
                    return False
            except:
                return False

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os, hashlib
from aiogram.types import InputContactMessageContent, InlineQueryResultArticle

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "echo"
    link = 'https://ru.wikipedia.org/wiki/'+text
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id = result_id,
        title='Статья Wikipedia:',
        url=link,
        input_message_content=types.InputTextMessageContent(
            message_text=link))]
    
    await query.answer(articles, cache_time=1, is_personal=True)

executor.start_polling(dp, skip_updates=True)
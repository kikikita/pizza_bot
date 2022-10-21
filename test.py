from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os, hashlib
from aiogram.dispatcher import filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

#ВИКИПЕДИЯ
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

#ТЕКСТОВЫЕ ФИЛЬТРЫ
@dp.message_handler(commands=['start', 'help'])
async def comand_start(message: types.Message):
    await message.reply('Здаров')


@dp.message_handler(commands=['команда'])
async def echo(message : types.Message):
    await message.answer(message.text)


@dp.message_handler(lambda message: 'ита бот люблю' in message.text)
async def taxi(message : types.Message):
    await message.reply('Я тебя люблю ❤')

@dp.message_handler(lambda message: 'ита бот споки' in message.text)
@dp.message_handler(lambda message: 'ита бот сладких' in message.text)
async def taxi(message : types.Message):
    await message.reply('Спокойной ночи!)')

@dp.message_handler(lambda message: message.text.startswith('Рита бот, кино'))
async def ufo(message : types.Message):
    await message.answer('Какое тебе кино?')
    await message.answer(message.text[2:])



# @dp.message_handler()
# async def empty(message : types.Message):
#     await message.answer('Нет такой команды')
#     await message.delete()


executor.start_polling(dp, skip_updates=True)
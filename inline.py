from tracemalloc import start
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

answ = dict()

# Кнопка-ссылка
urlkb = InlineKeyboardMarkup(row_width=2)
#text - название кнопки, url - ссылка куда ведет кнопка
urlButton = InlineKeyboardButton(text='Ссылка', url='https://www.youtube.com')
urlButton2 = InlineKeyboardButton(text='Ссылка2', url='https://mail.google.com')
x = [InlineKeyboardButton(text='Ссылка3', url='https://mail.google.com'),\
    InlineKeyboardButton(text='Ссылка4', url='https://mail.google.com'),\
    InlineKeyboardButton(text='Ссылка5', url='https://mail.google.com')]
urlkb.add(urlButton, urlButton2).row(*x).insert(InlineKeyboardButton(text='Ссылка6', url='https://mail.google.com'))

@dp.message_handler(commands='ссылки')
async def url_command(message : types.Message):
    await message.answer('Ссылочки:', reply_markup=urlkb)

#клавиатура с кнопкой
inkb = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton(text='Like', callback_data='like_1'),\
        InlineKeyboardButton(text='Не Like', callback_data='like_-1'))#название кнопки

#срабатывает на команду /test и отправляет клавиатуру выше
@dp.message_handler(commands='test')
async def test_commands(message : types.Message):
    #текст над кнопкой, а также кнопка inkb
    await message.answer('За видео с котятами', reply_markup=inkb)

#хендлер отлавливающий событие
@dp.callback_query_handler(Text(startswith='like_'))
#необходимо записать аннотацию типа
async def www_call(callback : types.CallbackQuery):
    #методом сплита разбиваем на список из двух знач [1]-индекс символа после '_'
    res = int(callback.data.split('_')[1])
    #проверка голосовал или нет
    if f'{callback.from_user.id}' not in answ:
        #по ключу id записываем результат 1 или -1
        answ[f'{callback.from_user.id}'] = res
        await callback.answer('Вы проголосовали')
    else:
        await callback.answer('Вы уже проголосовали', show_alert=True)
    await callback.answer('Вы проголосовали')
    #.answer - выдает всплывающее окно о том что нажата кнопка
    #.message.answer - выдает сообщение о том что нажата кнопка
    #await callback.message.answer('Кнопка нажата')
    # ответом мы подтверждаем отработку кода(часики исчезают)
    # show alert - вывод уведомления с кнопкой 'ОК'
    await callback.answer('Спасибо!', show_alert=True)


executor.start_polling(dp, skip_updates=True)
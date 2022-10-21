from cmd import IDENTCHARS
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types,Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

#@dp.message_handler(commands=['moderator'], is_chat_admin=True)#ЕСЛИ модератор
async def make_changes_comand(message: types.Message):
    global ID 
    #получаем id модератора
    ID = message.from_user.id 
    #отправляем сообщение модератору в ЛС
    #вставляем клавиатуру из модуля admin_kb
    await bot.send_message(message.from_user.id, 'Что желаете, хозяин?', reply_markup=admin_kb.button_case_admin)
    await message.delete()

#Начало диалога загрузки нового пункта меню
#@dp.message_handler(commands='Загрузить',state=None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID: #проверка id админа
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

async def cancel_handler(message: types.Message, state:FSMContext):
    if message.from_user.id == ID: #проверка id админа
        current_state = await state.get_state() #в каком состоянии бот
        if current_state is None: #если бот не в состоянии ожидания то не выполнится
            return
        await state.finish() #если в состоянии то исполнится код
        await message.reply('ОК')

#Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo) #передаем ранее ожидаемое состояние
async def load_photo(message : types.Message, state: FSMContext):
    if message.from_user.id == ID: #проверка id админа
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next() #ввод бота в состояние ожидания след ответа
        await message.reply('Теперь введи название')

#Ловим второй ответ
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID: #проверка id админа
        async with state.proxy() as data:
            data['name'] = message.text #вытягиваем текст
        await FSMAdmin.next()
        await message.reply('Введи описание')

#Ловим третий ответ
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID: #проверка id админа
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену')

#Ловим четвертый ответ
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID: #проверка id админа
        async with state.proxy() as data:
            data['price'] = float(message.text)

    await sqlite_db.sql_add_command(state)       
    await state.finish()

#Выход из состояний
#@dp.message_handler(state="*", commands='отмена') #state - любое из 4х состояний; -команда
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*") #-просто текст

#если событие начинается с 'del '
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
#запускаем ф-цию sql_delete_command
#callback_qerry - не имеет значение, просто название пар-ра
async def del_callback_run(callback_qerry: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_qerry.data.replace('del ', ''))
    #отвечает о том что запрос выполнен и отправляет что такая-то пицца удалена
    #из callback_qerry берем data, и с помощью replace заменяем на пустое знач, что остается название
    await callback_qerry.answer(text=f'{callback_qerry.data.replace("del ", "")} удалена.', show_alert=True)

#добавляем админу кнопку удалить
@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    #проверяем ялвяется ли он админом
    if message.from_user.id == ID:
        #читаем из модуля sqlite_db с помощью sql_read2()
        read = await sqlite_db.sql_read2()
        #по списку меню проходимся циклом for
        for ret in read:
        #отправляем администратору как и клиенту фото, описание, цена    
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
        #к каждому отправлению добавляем одну инлайн кнопку и текст (^^^), чтобы понять к какой пицце относится кнопка    
        #добавляем кнопку удалить del 'Название пиццы'    
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup()\
                .add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_comand, commands=['moderator'], is_chat_admin=True )


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

#СОЗДАНИЕ КНОПОК
b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
# b4 = KeyboardButton('Поделиться номером', request_contact=True)
# b5 = KeyboardButton('Отправить где я', request_location=True)


#ЗАМЕНЯЕТ КЛАВИАТУРУ НА НАШУ
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

#МЕТОД ДОБАВЛЯЕТ КНОПКУ 
kb_client.add(b3).row(b1,b2)#.row(b4,b5) #.insert() если есть место


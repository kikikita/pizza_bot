import sqlite3 as sq
from create_bot import bot

#определяем функцию подключения БД
def sql_start():
    global base, cur 
    #connect - позволяет подключиться к файлу БД\
    #если его не будет, то он создастся
    base = sq.connect('pizza_cool.db')
    #cursor - часть базы кот осущ поиск, встраивание, выборку
    cur = base.cursor()
    #когда подключается - выводит уведомление о подключении
    if base:
        print('Data base connected OK!')
    #создаем таблицу в которую будем вносить данные
    #IF NOT EXISTS - создать табл 'menu' если такой не существует
    #(4 столбца Название Формат)
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    #сохраняем изменения
    base.commit()


async def sql_add_command(state):
    #запускаем ассинхронно менеджер контекста with
    #открываем словарь 
    async with state.proxy() as data:
        #execute - исполнить, вставляем в таблицу меню значения data.values()
        cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))
        #сохраняем изменения
        base.commit()

#получаем событие - сообщение, когда срабатывает хендлер "МЕНЮ"
async def sql_read(message):
    # выбрать все из таблицы меню.fetchall
    # ret - список из строк нашей таблицы
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        #отправляем каждую строку таблицы, разбираяя ее
        #[0] - фотка, f-строка: ret[1]-название, описание: ret[2], Цена: ret[-1]
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')

# читает выборку из БД и возвращает в админ     
async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()

#передается название пиццы
async def sql_delete_command(data):
    #посылаем sql-запрос удалить из меню по названию конкретную запись
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

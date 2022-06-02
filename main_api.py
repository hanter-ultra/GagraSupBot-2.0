import telebot
import requests
import dbworker
import psycopg2
import config
import datetime
import os
import random
from telebot import types
from config import Token, admins

DATABASE_URL = os.environ['DATABASE_URL']

con = psycopg2.connect(DATABASE_URL, sslmode='require')
# con = psycopg2.connect(
#     database="postgres",
#     user="postgres",
#     password="gs",
#     host="127.0.0.1",
#     port="5432"
# )
cur = con.cursor()

bot = telebot.TeleBot(Token)

cur.execute(f'''CREATE TABLE IF NOT EXISTS events
                                 (Id Text,
                                 Name TEXT,
                                 Text TEXT,
                                 ImgName TEXT, 
                                 Price TEXT);''')
con.commit()
cur.execute(f'''CREATE TABLE IF NOT EXISTS claims
                                 (Id TEXT,
                                 ChatId TEXT,
                                 Name TEXT,
                                 Date TEXT,
                                 State TEXT,
                                 NameUser TEXT, 
                                 Price INT,
                                 TextC TEXT);''')
con.commit()


claim_a = {}
claim_p = {}
new_event = {}


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in admins:
        cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                             (Name TEXT,
                                                             Date TEXT,
                                                             State TEXT,
                                                             NameUser TEXT, 
                                                             Price INT, 
                                                             AnswerAdmin TEXT);''')
        con.commit()
        buttons = [
            types.InlineKeyboardButton(text="Прогулки", callback_data="ClbEvents-A"),
            types.InlineKeyboardButton(text="Все заявки", callback_data="ClbClaims-A"),
            types.InlineKeyboardButton(text="Бот", callback_data="ClbBot-A")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, 'Панель администратора. По кнопке "Бот" можно зайти в бота, как обычный пользователь...',
                             reply_markup=keyboard)
    else:
        cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                     (Name TEXT,
                                                     Date TEXT,
                                                     State TEXT,
                                                     NameUser TEXT, 
                                                     Price INT, 
                                                     AnswerAdmin TEXT);''')
        con.commit()
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        EventsNames = ''
        for i in range(len(rows)):
            EventsNames += f'{rows[i][1]}\n'
        buttons = [
            types.InlineKeyboardButton(text="Прайс", callback_data="ClbEvents"),
            types.InlineKeyboardButton(text="Помощь", callback_data="ClbHelp"),
            types.InlineKeyboardButton(text="Мои заявки", callback_data="ClbClaims")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, f' 👋🏻 <b>Приветствую! Я GAGRASUPbot.</b>'
                                          f' Откройте для себя новый увлекательный мир морских прогулок. '
                                          f'Ознакомьтесь с нашим предложением и выберите для себя самое лучшее'
                                          f'\n\n <b>Сапбординг</b> <em>— именно тот вид активности, который '
                                          f'понравится абсолютно всем, это по-настоящему универсальный вид '
                                          f'активного отдыха, который по душе и взрослым, и детям. Многие хотят '
                                          f'просто кататься по морю, по реке, встречать рассветы и загорать. '
                                          f'\nНикакого экстрима.</em>'
                                          f'\n\nИНСТРУКТАЖ И БЕЗОПАСНОСТЬ'
                                          f'\n У нас только качественные и брендовые сапборды Stormline, Bombitto и другие.'
                                          f'\n\n Гид проводит обязательный инструктаж перед сплавом, выдает спасательные '
                                          f'жилеты, водонепроницаемые чехлы для телефонов. '
                                          f'\n\n <em>*При неблагоприятных климатических условиях возможен перенос прогулки</em>'
                                          f'\n\n<b>ПРОКАТ • ПРОГУЛКИ • ИНДИВИДУАЛЬНЫЕ ТУРЫ</b>'
                                          f'\n\n<code>нажмите «Прайс» и выберите прогулку</code>', parse_mode='html', reply_markup=keyboard)


@bot.message_handler(commands=['price_list'])
def price_list(message):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                                 (Name TEXT,
                                                                 Date TEXT,
                                                                 State TEXT,
                                                                 NameUser TEXT, 
                                                                 Price INT, 
                                                                 AnswerAdmin TEXT);''')
    con.commit()
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}", callback_data=f"ClbEvents{rows[i][0]}") for i in
               range(len(rows))]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Главное меню »", callback_data=f"ClbStart"))
    bot.send_message(chat_id=message.chat.id, text='<b>ПРОГУЛКИ. Выберите подходящий вариант:</b>', parse_mode='html',
                          reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help(message):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                                     (Name TEXT,
                                                                     Date TEXT,
                                                                     State TEXT,
                                                                     NameUser TEXT, 
                                                                     Price INT, 
                                                                     AnswerAdmin TEXT);''')
    con.commit()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='WhatsApp', url='https://wa.me/+79407120912'),
                 types.InlineKeyboardButton(text='Telegram', url='tg://resolve?domain=simeon_kolchin'),
                 types.InlineKeyboardButton(text='Instagram', url='tg://resolve?domain=simeon_kolchin'),
                 types.InlineKeyboardButton(text=f"Главное меню »", callback_data=f"ClbStart"))
    bot.send_message(chat_id=message.chat.id, text='Вы можете написать нам:', reply_markup=keyboard)


@bot.message_handler(commands=['my_claims'])
def my_claims(message):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
                                                                     (Name TEXT,
                                                                     Date TEXT,
                                                                     State TEXT,
                                                                     NameUser TEXT, 
                                                                     Price INT, 
                                                                     AnswerAdmin TEXT);''')
    con.commit()
    cur.execute(f"SELECT * FROM p{message.chat.id}")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][0]} ({'.'.join(rows[i][1].split()[0].split('-')[::-1])})",
                                          callback_data=f"ClbEvents{rows[i][1].split()[0]}_{rows[i][1].split()[1]}")
               for i in
               range(len(rows))]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Главное меню »", callback_data=f"ClbStart"))
    bot.send_message(chat_id=message.chat.id, text='Выберите название прогулки:', reply_markup=keyboard)


# Добавление заявки пользователя ----- Добавление заявки пользователя ----- Добавление заявки пользователя ----- Добавление заявки пользователя
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.SendClaim.value)
def user_age(message):
    date = datetime.datetime.now()
    user_name = message.chat.username
    cur.execute(f'''INSERT INTO p{message.chat.id} (Name, Date, State, NameUser, Price, AnswerAdmin) VALUES 
                                                                           ('{claim_p[message.chat.id, 'name_event']}', 
                                                                           '{date}', 
                                                                           'На рассмотрении', 
                                                                           '{user_name}', 
                                                                           '{claim_p[message.chat.id, 'price_event']}',
                                                                           ' ');''')
    con.commit()
    cur.execute(f"SELECT * FROM p{message.chat.id}")
    rowssss = cur.fetchall()
    claim_id = f'{message.chat.id}_{len(rowssss)}'
    ttt = message.text
    cur.execute(f'''INSERT INTO claims (Id, ChatId, Name, Date, State, NameUser, Price, TextC) VALUES 
                                                                                       ('{claim_id}',
                                                                                       '{message.chat.id}',
                                                                                       '{claim_p[message.chat.id, 'name_event']}', 
                                                                                       '{date}', 
                                                                                       'На рассмотрении', 
                                                                                       '{user_name}', 
                                                                                       '{claim_p[message.chat.id, 'price_event']}',
                                                                                       '{ttt}');''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
    keya = types.InlineKeyboardMarkup(row_width=1)
    keya.add(types.InlineKeyboardButton(text=f"Написать", callback_data=f"ClbSendMessage"))
    bot.send_message(message.chat.id,
                     'Заявка успешно создана. Ожидайте! В ближайшее время с вами свяжется администратор!',
                     reply_markup=key)
    claim_a['admin_claim_id'] = claim_id
    claim_a['admin_chat_id'] = message.chat.id
    claim_a['admin_chat_date'] = date
    for o in admins:
        bot.send_message(int(o), f'Новая заявка!!!'
                                 f'\n\nПрогулка: {claim_p[message.chat.id, "name_event"]}'
                                 f'\nДата: {date}'
                                 f'\nИмя пользователя: {user_name}'
                                 f'\nЦена: {claim_p[message.chat.id, "price_event"]}'
                                 f'\n\nКомментарий: {ttt}', reply_markup=keya)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


# Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.WFMesT.value)
def user_age(message):
    text = message.text
    cur.execute(f'''SELECT ChatId FROM claims WHERE Id = '{claim_a['admin_claim_id']}';''')
    rows = cur.fetchone()
    bot.send_message(int(rows[0]), text)
    cur.execute(
        f'''UPDATE p{claim_a['admin_chat_id']} SET AnswerAdmin = '{text}' WHERE Date = '{claim_a['admin_chat_date']}';''')
    con.commit()
    dbworker.set_state(message.chat.id, config.States.S_START.value)


# Новое мероприятие_название ----- Новое мероприятие_название ----- Новое мероприятие_название ----- Новое мероприятие_название ----- Новое мероприятие_название
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewEventName.value)
def user_age(message):
    new_event[message.chat.id, 'name'] = message.text
    bot.send_message(message.chat.id, 'Напишите описание мероприятия...')
    dbworker.set_state(message.chat.id, config.States.NewEventText.value)


# Новое мероприятие_описание ----- Новое мероприятие_описание ----- Новое мероприятие_описание ----- Новое мероприятие_описание ----- Новое мероприятие_описание
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewEventText.value)
def user_age(message):
    new_event[message.chat.id, 'text'] = message.text
    bot.send_message(message.chat.id, 'Какая цена одного билета на данное мероприятие? (Кол-во: 1 шт)')
    dbworker.set_state(message.chat.id, config.States.NewEventPrice.value)


# Новое мероприятие_цена ----- Новое мероприятие_цена ----- Новое мероприятие_цена ----- Новое мероприятие_цена ----- Новое мероприятие_цена
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.NewEventPrice.value)
def user_age(message):
    new_event[message.chat.id, 'price'] = message.text
    cur.execute(f'''INSERT INTO events (Id, Name, Text, ImgName, Price) VALUES 
                                                            ('{datetime.datetime.now()}',
                                                            '{new_event[message.chat.id, "name"]}',
                                                            '{new_event[message.chat.id, "text"]}',
                                                            ' ',
                                                            '{new_event[message.chat.id, "price"]}');''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
    bot.send_message(message.chat.id, f'Мероприятие успешно создано!!!'
                         f'\n\nНазвание кнопки: {new_event[message.chat.id, "name"]}'
                         f'\nОписание: {new_event[message.chat.id, "text"]}'
                         f'\nЦена: {new_event[message.chat.id, "price"]}₽', reply_markup=key)
    dbworker.set_state(message.chat.id, config.States.S_START.value)


# Callback ----- Callback ----- Callback ----- Callback ----- Callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS p{call.message.chat.id}
                                                                 (Name TEXT,
                                                                 Date TEXT,
                                                                 State TEXT,
                                                                 NameUser TEXT, 
                                                                 Price INT, 
                                                                 AnswerAdmin TEXT);''')
    con.commit()


    # Старт callback ----- Старт callback ----- Старт callback ----- Старт callback ----- Старт callback
    if call.data == 'ClbStart':
        if call.message.chat.id in admins:
            buttons = [
                types.InlineKeyboardButton(text="Прогулки", callback_data="ClbEvents-A"),
                types.InlineKeyboardButton(text="Все заявки", callback_data="ClbClaims-A"),
                types.InlineKeyboardButton(text="Бот", callback_data="ClbBot-A")
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Панель администратора. По кнопке "Бот" можно зайти в бота, как обычный пользователь...',
                reply_markup=keyboard)
        else:
            cur.execute("SELECT * FROM events")
            rows = cur.fetchall()
            EventsNames = ''
            for i in range(len(rows)):
                EventsNames += f'{rows[i][1]}\n'
            buttons = [
                types.InlineKeyboardButton(text="Прайс", callback_data="ClbEvents"),
                types.InlineKeyboardButton(text="Помощь", callback_data="ClbHelp"),
                types.InlineKeyboardButton(text="Мои заявки", callback_data="ClbClaims")
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f' 👋🏻 <b>Приветствую! Я GAGRASUPbot.</b>'
                                          f' Откройте для себя новый увлекательный мир морских прогулок. '
                                          f'Ознакомьтесь с нашим предложением и выберите для себя самое лучшее'
                                          f'\n\n <b>Сапбординг</b> <em>— именно тот вид активности, который '
                                          f'понравится абсолютно всем, это по-настоящему универсальный вид '
                                          f'активного отдыха, который по душе и взрослым, и детям. Многие хотят '
                                          f'просто кататься по морю, по реке, встречать рассветы и загорать. '
                                          f'\nНикакого экстрима.</em>'
                                          f'\n\nИНСТРУКТАЖ И БЕЗОПАСНОСТЬ'
                                          f'\n У нас только качественные и брендовые сапборды Stormline, Bombitto и другие.'
                                          f'\n\n Гид проводит обязательный инструктаж перед сплавом, выдает спасательные '
                                          f'жилеты, водонепроницаемые чехлы для телефонов. '
                                          f'\n\n <em>*При неблагоприятных климатических условиях возможен перенос прогулки</em>'
                                          f'\n\n<b>ПРОКАТ • ПРОГУЛКИ • ИНДИВИДУАЛЬНЫЕ ТУРЫ</b>'
                                          f'\n\n<code>нажмите «Прайс» и выберите прогулку</code>', parse_mode='html', reply_markup=keyboard)


    # Показать мероприятия для пользователя ----- Показать мероприятия для пользователя ----- Показать мероприятия для пользователя
    if call.data == 'ClbEvents':
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}", callback_data=f"ClbEvents{rows[i][0]}") for i in
                   range(len(rows))]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='<b>ПРОГУЛКИ. Выберите подходящий вариант:</b>', parse_mode='html', reply_markup=keyboard)


    # Показать мероприятия для пользователя вывод ----- Показать мероприятия для пользователя вывод ----- Показать мероприятия для пользователя вывод
    cur.execute("SELECT * FROM events")
    rows_events = cur.fetchall()
    for i in range(len(rows_events)):
        if call.data == f"ClbEvents{rows_events[i][0]}":
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Подать заявку", callback_data=f"ClbEventsSend{rows_events[i][0]}"),
                    types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'{rows_events[i][2]}'
                                       f'\n\n<b>Цена: {rows_events[i][4]}₽</b>', parse_mode='html', reply_markup=key)


        # Подать заявку ----- Подать заявку ----- Подать заявку ----- Подать заявку ----- Подать заявку
        if call.data == f"ClbEventsSend{rows_events[i][0]}":
            cur.execute(f"SELECT * FROM p{call.message.chat.id}")
            row_sel = cur.fetchall()
            k = 1
            for p in range(len(row_sel)):
                if (row_sel[p][1].split()[0] == f'{datetime.datetime.now()}'.split()[0]) and (
                        rows_events[i][1] == row_sel[p][0]):
                    k = 0
            if k:
                dbworker.set_state(call.message.chat.id, config.States.SendClaim.value)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Напишите сообщение к заявке и укажите в нем контактные данные (номер телефона/ссылка на телеграм/ссылка на страницу вк)...')
                claim_p[call.message.chat.id, 'name_event'] = rows_events[i][1]
                claim_p[call.message.chat.id, 'price_event'] = rows_events[i][4]

            else:
                keyss = types.InlineKeyboardMarkup(row_width=1)
                keyss.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Заявка повторно быть подана не может! Второй раз подать заявку вы сможете только завтра!',
                                      reply_markup=keyss)


        # Все мероприятия вывод ----- Все мероприятия вывод ----- Все мероприятия вывод ----- Все мероприятия вывод ----- Все мероприятия вывод
        if call.data == f"ClbEvents{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}-A":
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Удалить",
                                               callback_data=f"ClbDelEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}"),
                    types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'{rows_events[i][2]}'
                                         f'\n\n<b>Цена: {rows_events[i][4]}₽</b>', parse_mode='html', reply_markup=key)


        # Удалить мероприятие ----- Удалить мероприятие ----- Удалить мероприятие ----- Удалить мероприятие ----- Удалить мероприятие
        if call.data == f"ClbDelEvent{rows_events[i][0].split()[0]}_{rows_events[i][0].split()[1]}":
            cur.execute(f'''DELETE FROM events WHERE Id = '{rows_events[i][0]}';''')
            con.commit()
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Мероприятие удалено!', reply_markup=key)



    # Все заявки для пользователя ----- Все заявки для пользователя ----- Все заявки для пользователя ----- Все заявки для пользователя ----- Все заявки для пользователя
    if call.data == 'ClbClaims':
        cur.execute(f"SELECT * FROM p{call.message.chat.id}")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][0]} ({'.'.join(rows[i][1].split()[0].split('-')[::-1])})",
                                              callback_data=f"ClbEvents{rows[i][1].split()[0]}_{rows[i][1].split()[1]}")
                   for i in range(len(rows))]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению у вас пока нет заявок((( ' \
                   '\n\n<code>Чтобы подать заявку нажмите «Прайс» и выберите прогулку</code>'
            keyboard.add(types.InlineKeyboardButton(text=f"Прайс", callback_data=f"ClbEvents"))
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, parse_mode='html', reply_markup=keyboard)


    # Все заявки для пользователя вывод ----- Все заявки для пользователя вывод ----- Все заявки для пользователя вывод ----- Все заявки для пользователя вывод ----- Все заявки для пользователя вывод
    cur.execute(f"SELECT * FROM p{call.message.chat.id}")
    rows_claims_user = cur.fetchall()
    for i in range(len(rows_claims_user)):
        if call.data == f"ClbEvents{rows_claims_user[i][1].split()[0]}_{rows_claims_user[i][1].split()[1]}":
            keydpl = types.InlineKeyboardMarkup(row_width=1)
            keydpl.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'<b>{rows_claims_user[i][0]}</b>'
                                       f'\nДата: {".".join(rows_claims_user[i][1].split()[0].split("-")[::-1])}'
                                       f'\nВремя: {":".join(rows_claims_user[i][1].split()[1].split(":")[0:2])}'
                                       f'\n\nСтатус: {rows_claims_user[i][2]}'
                                       f'\nЦена: {rows_claims_user[i][4]}'
                                       f'\n\nСообщение от администратора: {rows_claims_user[i][5]}', parse_mode='html', reply_markup=keydpl)


    # Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора ----- Сообщение администратора
    if call.data == 'ClbSendMessage':
        dbworker.set_state(call.message.chat.id, config.States.WFMesT.value)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Напишите сообщение...')


    # Прайс / мероприятия ----- Прайс / мероприятия ----- Прайс / мероприятия ----- Прайс / мероприятия ----- Прайс / мероприятия
    if call.data == 'ClbEvents-A':
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}",
                                              callback_data=f"ClbEvents{rows[i][0].split()[0]}_{rows[i][0].split()[1]}-A")
                   for i in
                   range(len(rows))]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"Создать мероприятие", callback_data=f"ClbNewEvent-A"),
                     types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению мероприятий пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.S_START.value)


    # Новое мероприятие ----- Новое мероприятие ----- Новое мероприятие ----- Новое мероприятие ----- Новое мероприятие
    if call.data == 'ClbNewEvent-A':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbEvents-A"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Напишите название мероприятия...', reply_markup=keyboard)
        dbworker.set_state(call.message.chat.id, config.States.NewEventName.value)


    # Виды заявок ----- Виды заявок ----- Виды заявок ----- Виды заявок ----- Виды заявок
    if call.data == 'ClbClaims-A':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=f"На рассмотрении", callback_data=f"ClbClaimsTrue_0-A"),
                     types.InlineKeyboardButton(text=f"Одобренные", callback_data=f"ClbClaimsTrue_2-A"),
                     types.InlineKeyboardButton(text=f"Выполненные", callback_data=f"ClbClaimsFalse_1-A"),
                     types.InlineKeyboardButton(text=f"Отклоненные", callback_data=f"ClbClaimsTrue_3-A"),
                     types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите тип заявок:', reply_markup=keyboard)


    # Виды заявок вывод ----- Виды заявок вывод ----- Виды заявок вывод ----- Виды заявок вывод ----- Виды заявок вывод
    if call.data == 'ClbClaimsTrue_0-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'На рассмотрении']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    if call.data == 'ClbClaimsTrue_2-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'Одобрена']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    if call.data == 'ClbClaimsTrue_3-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'Отклонена']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    if call.data == 'ClbClaimsFalse_1-A':
        cur.execute("SELECT * FROM claims")
        rows = cur.fetchall()
        buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{'_'.join(rows[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows[i][3].split()[1].split(':')[0:2])}-A") for i in
                range(len(rows)) if rows[i][4] == 'Выполнена']
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        keyboard.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
        text = 'Выберите название прогулки:'
        if buttons == []:
            text = 'К сожалению новых заявок пока нет!'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)


    # Вывод заявки ----- Вывод заявки ----- Вывод заявки ----- Вывод заявки ----- Вывод заявки
    cur.execute("SELECT * FROM claims")
    rows_claims = cur.fetchall()
    for i in range(len(rows_claims)):
        if call.data == f"ClbClaimTrue{'_'.join(rows_claims[i][3].split()[0].split('-')[::-1])}_{'_'.join(rows_claims[i][3].split()[1].split(':')[0:2])}-A":
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"Поставить статус - Выполнена",
                                                callback_data=f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_1-A"),
                     types.InlineKeyboardButton(text=f"Поставить статус - Одобрена",
                                                callback_data=f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_2-A"),
                     types.InlineKeyboardButton(text=f"Поставить статус - Отклонена",
                                               callback_data=f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_3-A"),
                     types.InlineKeyboardButton(text=f"Написать сообщение к заявке", callback_data=f"ClbSendMessage"),
                     types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            claim_a['admin_claim_id'] = rows_claims[i][0]
            cur.execute(f"SELECT * FROM p{rows_claims[i][1]} WHERE Date = '{rows_claims[i][3]}'")
            r = cur.fetchall()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'ChatId - {rows_claims[i][1]}'
                                         f'\n\nНазвание мероприятия: {rows_claims[i][2]}'
                                         f'\nДата: {".".join(rows_claims[i][3].split()[0].split("-")[::-1])} в {":".join(rows_claims[i][3].split()[1].split(":")[0:2])}'
                                         f'\nСтатус: {rows_claims[i][4]}'
                                         f'\nИмя пользователя: @{rows_claims[i][5]}'
                                         f'\n\nЦена: {rows_claims[i][6]}'
                                         f'\n\nСообщение администратора: {r[0][5]}'
                                         f'\n\nКомментарий пользователя: {rows_claims[i][7]}', reply_markup=keyb)


        # Статусы заявок ----- Статусы заявок ----- Статусы заявок ----- Статусы заявок ----- Статусы заявок
        if call.data == f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_1-A":
            cur.execute(f'''UPDATE claims SET State = 'Выполнена' WHERE Id = '{rows_claims[i][0]}';''')
            con.commit()
            cur.execute(f'''UPDATE p{rows_claims[i][1]} SET State = 'Выполнена' WHERE Date = '{rows_claims[i][3]}';''')
            con.commit()
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            bot.send_message(rows_claims[i][1], f'Ваша заявка "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} выполнена!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Успешно! Статус заявки "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} изменен на "Выполнена"', reply_markup=keyb)


        if call.data == f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_2-A":
            cur.execute(f'''UPDATE claims SET State = 'Одобрена' WHERE Id = '{rows_claims[i][0]}';''')
            con.commit()
            cur.execute(f'''UPDATE p{rows_claims[i][1]} SET State = 'Одобрена' WHERE Date = '{rows_claims[i][3]}';''')
            con.commit()
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            bot.send_message(rows_claims[i][1], f'Ваша заявка "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} одобрена!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Успешно! Статус заявки "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} изменен на "Одобрена"', reply_markup=keyb)


        if call.data == f"ClbClaimTrue{rows_claims[i][3].split()[0]}_{rows_claims[i][3].split()[1]}-True_3-A":
            cur.execute(f'''UPDATE claims SET State = 'Отклонена' WHERE Id = '{rows_claims[i][0]}';''')
            con.commit()
            cur.execute(f'''UPDATE p{rows_claims[i][1]} SET State = 'Отклонена' WHERE Date = '{rows_claims[i][3]}';''')
            con.commit()
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbClaims-A"))
            bot.send_message(rows_claims[i][1], f'Ваша заявка "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} отклонена!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Успешно! Статус заявки "{rows_claims[i][2]}" от '
                                                f'{".".join(rows_claims[i][3].split()[0].split("-")[::-1])} '
                                                f'{":".join(rows_claims[i][3].split()[1].split(":")[0:2])} изменен на "Отклонена"', reply_markup=keyb)


    # Помощь ----- Помощь ----- Помощь ----- Помощь ----- Помощь
    if call.data == "ClbHelp":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='WhatsApp', url='https://wa.me/+79407120912'),
                     types.InlineKeyboardButton(text='Telegram', url='tg://resolve?domain=simeon_kolchin'),
                     types.InlineKeyboardButton(text='Instagram', url='tg://resolve?domain=simeon_kolchin'),
                     types.InlineKeyboardButton(text=f"« Назад", callback_data=f"ClbStart"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Вы можете написать нам:', reply_markup=keyboard)

bot.polling(none_stop = True, interval = 0)
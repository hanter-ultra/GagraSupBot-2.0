import logging
import psycopg2
import datetime
import os
import config
from aiogram import Bot
from aiogram import executor
from config import Token, admins
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram.utils.markdown as fmt

DATABASE_URL = os.environ['DATABASE_URL']

con = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = con.cursor()

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

cur.execute(f'''CREATE TABLE IF NOT EXISTS events
                                 (Id Text,
                                 Name TEXT,
                                 Text TEXT,
                                 ImgName TEXT, 
                                 Price INT);''')
con.commit()
cur.execute(f'''CREATE TABLE IF NOT EXISTS claims
                                 (Id TEXT,
                                 ChatId TEXT,
                                 Name TEXT,
                                 Date TEXT,
                                 State TEXT,
                                 NameUser TEXT, 
                                 Price INT);''')
con.commit()

claim_a = {}


class SendMessage(StatesGroup):
    waiting_for_message_text = State()


class NewEvent(StatesGroup):
    name_event = State()
    text_event = State()
    price_event = State()


class EditEvent(StatesGroup):
    edit_name_event = State()
    edit_text_event = State()
    edit_price_event = State()

# cur.execute(f'''CREATE TABLE IF NOT EXISTS p{message.chat.id}
#                              (id TEXT,
#                              Name TEXT,
#                              Number TEXT);''')
# con.commit()
# cur.execute("DELETE FROM p1647407069")
# cur.execute("SELECT * FROM p1647407069")
# rows = cur.fetchall()
# print(len(rows))
# for i in range(len(rows)):
#     await message.answer(rows[i][0])

@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.chat.id in admins:
        buttons = [
            types.InlineKeyboardButton(text="Прогулки", callback_data="ClbEvents-A"),
            types.InlineKeyboardButton(text="Все заявки", callback_data="ClbClaims-A"),
            types.InlineKeyboardButton(text="Редактировать текст", callback_data="ClbEditText-A"),
            types.InlineKeyboardButton(text="Бот", callback_data="ClbBot-A")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer('Панель администратора. По кнопке "Бот" можно зайти в бота, как обычный пользователь...', reply_markup=keyboard)
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
            types.InlineKeyboardButton(text="Прогулки", callback_data="ClbEvents"),
            types.InlineKeyboardButton(text="Помощь", callback_data="ClbHelp"),
            types.InlineKeyboardButton(text="Мои заявки", callback_data="ClbClaims")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer(f'👋🏻 <b>Приветствую! Я GAGRASUPbot.</b>'
                             f'\n\nПредлагаем вашему вниманию ощутить себя сакурой на сапах!'
                             f'\n\nStand Up Paddle - так полностью звучит и его перевод. История появления сапов. Он подойдёт как для подростков так и для детей, даже для самых юных серферов, ведь плавать на нем совсем не сложно'
                             f'\n\nПредлагаем вам покататься на лучших сапах Bombitto, Stormline и др.'
                             f'\n\nДанный вид безопасен. Мы вам выдаём водонепроницаемые чехлы для телефонов, спасательные жилеты 🦺.'
                             f'\n\nНа сапе можно уместить груз, ведь для этого есть специальный кармашек.'
                             f'\n\nНаши услуги:\n{EventsNames}'
                             f'\nИндивидуальные туры на сапах на Рицу, каньон Хашупсе, реку Мчишта, Белые скалы'
                             f'\n\nЕсли хотите вы определились с прогулкой или хотите узнать более подробно про каждую прогулку нажмите на «ПРОГУЛКИ»',
                             parse_mode=types.ParseMode.HTML, reply_markup=keyboard)



@dp.callback_query_handler(text="ClbStart")
async def clb_start(call: types.CallbackQuery):
    if call.message.chat.id in admins:
        buttons = [
            types.InlineKeyboardButton(text="Прогулки", callback_data="ClbEvents-A"),
            types.InlineKeyboardButton(text="Все заявки", callback_data="ClbClaims-A"),
            types.InlineKeyboardButton(text="Редактировать текст", callback_data="ClbEditText-A"),
            types.InlineKeyboardButton(text="Бот", callback_data="ClbBot-A")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await call.message.edit_text('Панель администратора. По кнопке "Бот" можно зайти в бота, как обычный пользователь...', reply_markup=keyboard)
    else:
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        EventsNames = ''
        for i in range(len(rows)):
            EventsNames += f'{rows[i][1]}\n'
        buttons = [
            types.InlineKeyboardButton(text="Прогулки", callback_data="ClbEvents"),
            types.InlineKeyboardButton(text="Помощь", callback_data="ClbHelp"),
            types.InlineKeyboardButton(text="Мои заявки", callback_data="ClbClaims")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await call.message.edit_text(f'👋🏻 <b>Приветствую! Я GAGRASUPbot.</b>'
                                     f'\n\nПредлагаем вашему вниманию ощутить себя сакурой на сапах!'
                                     f'\n\nStand Up Paddle - так полностью звучит и его перевод. История появления сапов. Он подойдёт как для подростков так и для детей, даже для самых юных серферов, ведь плавать на нем совсем не сложно'
                                     f'\n\nПредлагаем вам покататься на лучших сапах Bombitto, Stormline и др.'
                                     f'\n\nДанный вид безопасен. Мы вам выдаём водонепроницаемые чехлы для телефонов, спасательные жилеты 🦺.'
                                     f'\n\nНа сапе можно уместить груз, ведь для этого есть специальный кармашек.'
                                     f'\n\nНаши услуги:\n{EventsNames}'
                                     f'\nИндивидуальные туры на сапах на Рицу, каньон Хашупсе, реку Мчишта, Белые скалы'
                                     f'\n\nЕсли хотите вы определились с прогулкой или хотите узнать более подробно про каждую прогулку нажмите на «ПРОГУЛКИ»',
                                     parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(text="ClbEvents")
async def clb_events(call: types.CallbackQuery):
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}", callback_data=f"ClbEvents{rows[i][0]}") for i in
               range(len(rows))]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbStart"))
    await call.message.edit_text('Выберите название прогулки:', reply_markup=keyboard)

    for i in range(len(rows)):
        @dp.callback_query_handler(text=f"ClbEvents{rows[i][0]}")
        async def clb_events_events(call: types.CallbackQuery):
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Подать заявку", callback_data=f"ClbEventsSend"),
                    types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbEvents"))
            await call.message.edit_text(f'<b>{rows[i][1]}</b>'
                                         f'\n\n{rows[i][2]}'
                                         f'\n\nЦена: {rows[i][4]}', parse_mode=types.ParseMode.HTML, reply_markup=key)

        @dp.callback_query_handler(text=f"ClbEventsSend")
        async def clb_events_send(call: types.CallbackQuery):
            date = datetime.datetime.now()
            user_name = call.message.chat.username
            cur.execute(f'''INSERT INTO p{call.message.chat.id} (Name, Date, State, NameUser, Price, AnswerAdmin) VALUES 
                                                   ('{rows[i][1]}', 
                                                   '{date}', 
                                                   'На рассмотрении', 
                                                   '{user_name}', 
                                                   '{rows[i][4]}',
                                                   ' ');''')
            con.commit()
            cur.execute(f"SELECT * FROM p{call.message.chat.id}")
            rowssss = cur.fetchall()
            claim_id = f'{call.message.chat.id}_{len(rowssss)}'
            cur.execute(f'''INSERT INTO claims (Id, ChatId, Name, Date, State, NameUser, Price) VALUES 
                                                               ('{claim_id}',
                                                               '{call.message.chat.id}',
                                                               '{rows[i][1]}', 
                                                               '{date}', 
                                                               'На рассмотрении', 
                                                               '{user_name}', 
                                                               '{rows[i][4]}');''')
            con.commit()
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbStart"))
            keya = types.InlineKeyboardMarkup(row_width=1)
            keya.add(types.InlineKeyboardButton(text=f"Написать", callback_data=f"ClbSendMessage"))
            await call.message.edit_text(
                'Заявка успешно создана. Ожидайте! В ближайшее время с вами свяжется администратор!', reply_markup=key)
            claim_a['admin_claim_id'] = claim_id
            claim_a['admin_chat_id'] = call.message.chat.id
            claim_a['admin_chat_date'] = date
            for o in admins:
                await bot.send_message(int(o), f'Новая заявка!!!'
                                               f'\n\nПрогулка: {rows[i][1]}'
                                               f'\nДата: {date}'
                                               f'\nИмя пользователя: {user_name}'
                                               f'\nЦена: {rows[i][4]}', reply_markup=keya)


@dp.callback_query_handler(text="ClbHelp")
async def clb_help(call: types.CallbackQuery):
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbStart"))
    await call.message.edit_text('Здесь будет помощь!', reply_markup=key)


@dp.callback_query_handler(text="ClbClaims")
async def clb_help(call: types.CallbackQuery):
    cur.execute(f"SELECT * FROM p{call.message.chat.id}")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][0]} ({'.'.join(rows[i][1].split()[0].split('-')[::-1])})", callback_data=f"ClbEvents{rows[i][1]}") for i in
               range(len(rows))]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbStart"))
    await call.message.edit_text('Выберите название прогулки:', reply_markup=keyboard)
    for i in range(len(rows)):
        @dp.callback_query_handler(text=f"ClbEvents{rows[i][1]}")
        async def clb_events_events(call: types.CallbackQuery):
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbClaims"))
            await call.message.edit_text(f'<b>{rows[i][0]}</b>'
                                         f'\nДата: {".".join(rows[i][1].split()[0].split("-")[::-1])}'
                                         f'\nВремя: {":".join(rows[i][1].split()[1].split(":")[0:2])}'
                                         f'\n\nСтатус: {rows[i][2]}'
                                         f'\nЦена: {rows[i][4]}'
                                         f'\n\nСообщение от администратора: {rows[i][5]}', parse_mode=types.ParseMode.HTML, reply_markup=key)


@dp.callback_query_handler(text="ClbSendMessage")
async def clb_send_message(call: types.CallbackQuery):
    await SendMessage.waiting_for_message_text.set()
    await call.message.edit_text('Напишите сообщение...')

@dp.message_handler(state=SendMessage.waiting_for_message_text)
async def send_message(message: types.Message, state: FSMContext):
    text = message.text
    cur.execute(f'''SELECT ChatId FROM claims WHERE Id = '{claim_a['admin_claim_id']}';''')
    rows = cur.fetchone()
    await dp.bot.send_message(int(rows[0]), text)
    cur.execute(f'''UPDATE p{claim_a['admin_chat_id']} SET AnswerAdmin = '{text}' WHERE Date = '{claim_a['admin_chat_date']}';''')
    con.commit()
    await state.finish()


# ADMINISTRATION
@dp.callback_query_handler(text="ClbEvents-A")
async def events_adm(call: types.CallbackQuery):
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][1]}", callback_data=f"ClbEvents{rows[i][0]}-A") for i in
               range(len(rows))]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Создать мероприятие", callback_data=f"ClbNewEvent-A"),
                 types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbStart"))
    text = 'Выберите название прогулки:'
    if buttons == []:
        text = 'К сожалению мероприятий пока нет!'
    await call.message.edit_text(text, reply_markup=keyboard)

    for i in range(len(rows)):
        @dp.callback_query_handler(text=f"ClbEvents{rows[i][0]}-A")
        async def clb_events_events_adm(call: types.CallbackQuery):
            key = types.InlineKeyboardMarkup(row_width=1)
            key.add(types.InlineKeyboardButton(text=f"Удалить", callback_data=f"ClbDelEvent{rows[i][0]}"),
                    types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbEvents-A"))
            await call.message.edit_text(f'<b>{rows[i][1]}</b>'
                                         f'\n\n{rows[i][2]}'
                                         f'\n\nЦена: {rows[i][4]}', parse_mode=types.ParseMode.HTML, reply_markup=key)


            @dp.callback_query_handler(text=f"ClbDelEvent{rows[i][0]}")
            async def clb_del_event_adm(call: types.CallbackQuery):
                cur.execute(f'''DELETE FROM events WHERE Id = '{rows[i][0]}';''')
                con.commit()
                key = types.InlineKeyboardMarkup(row_width=1)
                key.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbEvents-A"))
                await call.message.edit_text('Мероприятие удалено!', reply_markup=key)

@dp.callback_query_handler(text=f"ClbNewEvent-A")
async def clb_new_event_1_adm(call: types.CallbackQuery):
    await call.message.edit_text('Напишите название мероприятия...')
    await NewEvent.name_event.set()

@dp.message_handler(state=NewEvent.name_event)
async def clb_new_event_2_adm(message: types.Message, state: FSMContext):
    await state.update_data(name_event=message.text.lower())
    await NewEvent.next()
    await message.answer('Напишите описание мероприятия...')

@dp.message_handler(state=NewEvent.text_event)
async def clb_new_event_3_adm(message: types.Message, state: FSMContext):
    await state.update_data(text_event=message.text.lower())
    await NewEvent.next()
    await message.answer('Какая цена одного билета на данное мероприятие? (Кол-во: 1 шт)')

@dp.message_handler(state=NewEvent.price_event)
async def clb_new_event_4_adm(message: types.Message, state: FSMContext):
    await state.update_data(price_event=message.text.lower())
    user_data = await state.get_data()
    cur.execute(f'''INSERT INTO events (Id, Name, Text, ImgName, Price) VALUES 
                                                        ('{datetime.datetime.now()}',
                                                        '{user_data["name_event"]}',
                                                        '{user_data["text_event"]}',
                                                        ' ',
                                                        '{user_data["price_event"]}');''')
    con.commit()
    key = types.InlineKeyboardMarkup(row_width=1)
    key.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbEvents-A"))
    await message.answer(f'Мероприятие успешно создано!!!'
                            f'\n\nНазвание: {user_data["name_event"]}'
                            f'\nОписание: {user_data["text_event"]}'
                            f'\nЦена: {user_data["price_event"]}', reply_markup=key)
    await state.finish()



@dp.callback_query_handler(text=f"ClbClaims-A")
async def clb_claims_adm(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=f"На рассмотрении", callback_data=f"ClbClaimsTrue-A"),
                 types.InlineKeyboardButton(text=f"Выполненные", callback_data=f"ClbClaimsFalse-A"),
                 types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbStart"))
    await call.message.edit_text('Выберите тип заявок:', reply_markup=keyboard)

@dp.callback_query_handler(text=f"ClbClaimsTrue-A")
async def clb_claims_true_adm(call: types.CallbackQuery):
    cur.execute("SELECT * FROM claims")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({'.'.join(rows[i][3].split()[0].split('-')[::-1])})", callback_data=f"ClbClaimTrue{rows[i][0]}-A") for i in
               range(len(rows)) if rows[i][4] == 'На рассмотрении']
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbClaims-A"))
    text = 'Выберите название прогулки:'
    if buttons == []:
        text = 'К сожалению новых заявок пока нет!'
    await call.message.edit_text(text, reply_markup=keyboard)
    for i in range(len(rows)):
        @dp.callback_query_handler(text=f"ClbClaimTrue{rows[i][0]}-A")
        async def clb_claims_true_adm_1(call: types.CallbackQuery):
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"Поставить статус - Выполнена", callback_data=f"ClbClaimTrue{rows[i][0]}-True-A"),
                     types.InlineKeyboardButton(text=f"Написать сообщение к заявке", callback_data=f"ClbSendMessage"),
                     types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbClaimsTrue-A"))
            claim_a['admin_claim_id'] = rows[i][0]
            cur.execute(f"SELECT * FROM p{rows[i][1]} WHERE Date = '{rows[i][3]}'")
            r = cur.fetchall()
            print(r)
            await call.message.edit_text(f'ChatId - {rows[i][1]}'
                                         f'\n\nНазвание мероприятия: {rows[i][2]}'
                                         f'\nДата: {".".join(rows[i][3].split()[0].split("-")[::-1])} в {":".join(rows[i][3].split()[1].split(":")[0:2])}'
                                         f'\nСтатус: {rows[i][4]}'
                                         f'\nИмя пользователя: @{rows[i][5]}'
                                         f'\n\nЦена: {rows[i][6]}'
                                         f'\n\nСообщение администратора: {r[0][5]}', reply_markup=keyb)

        @dp.callback_query_handler(text=f"ClbClaimTrue{rows[i][0]}-True-A")
        async def clb_claims_true_adm_2(call: types.CallbackQuery):
            cur.execute(f'''UPDATE claims SET State = 'Выполнена' WHERE Id = '{rows[i][0]}';''')
            con.commit()
            cur.execute(f'''UPDATE p{rows[i][1]} SET State = 'Выполнена' WHERE Date = '{rows[i][3]}';''')
            con.commit()
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbClaimsTrue-A"))
            await call.message.edit_text(f'Успешно!', reply_markup=keyb)

@dp.callback_query_handler(text=f"ClbClaimsFalse-A")
async def clb_claims_false_adm(call: types.CallbackQuery):
    cur.execute("SELECT * FROM claims")
    rows = cur.fetchall()
    buttons = [types.InlineKeyboardButton(text=f"{rows[i][2]} ({rows[i][3].split()[0]})", callback_data=f"ClbClaimFalse{rows[i][0]}-A") for i in
               range(len(rows)) if rows[i][4] == 'Выполнена']
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbClaims-A"))
    text = 'Выберите название прогулки:'
    if buttons == []:
        text = 'К сожалению новых заявок пока нет!'
    await call.message.edit_text(text, reply_markup=keyboard)
    for i in range(len(rows)):
        @dp.callback_query_handler(text=f"ClbClaimFalse{rows[i][0]}-A")
        async def clb_claims_false_adm_1(call: types.CallbackQuery):
            keyb = types.InlineKeyboardMarkup(row_width=1)
            keyb.add(types.InlineKeyboardButton(text=f"Назад", callback_data=f"ClbClaimsFalse-A"))
            await call.message.edit_text(f'ChatId - {rows[i][1]}'
                                         f'\n\nНазвание мероприятия: {rows[i][2]}'
                                         f'\nДата: {rows[i][3]}'
                                         f'\nСтатус: {rows[i][4]}'
                                         f'\nИмя пользователя: {rows[i][5]}'
                                         f'\n\nЦена: {rows[i][6]}', reply_markup=keyb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
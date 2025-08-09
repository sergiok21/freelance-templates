import os
import shutil

from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, dp
from admin import AdminStates, handle_start_admin
from utils import add_user_id


class UserStates(StatesGroup):
    START = State()
    HELP = State()
    LOAD_DATA = State()
    PROCESS_DATA = State()
    PROCESS_COOKIES = State()
    EDIT_DATA = State()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await add_user_id(str(message.chat.id))
    if message.chat.id == ...:
        await AdminStates.START.set()
        await handle_start_admin(message, state)
    else:
        await UserStates.START.set()
        await handle_start(message, state)


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message, state: FSMContext):
    commands = '<b>Команди бота</b>:\n' \
               '<b>/start</b> - Повертає до початкового стану.\n' \
               '<b>/help</b> - Надсилає детальну інформацію по використанню застосунку.\n\n'
    load_data = '<b>Інструкція по завантаженню даних</b>:\nНатискаєте на кнопку "<b>Завантажити дані</b>". ' \
                'Далі надсилаєте <b>Cookies</b>. Вони можуть бути надіслані як по одному, так і пачкою. ' \
                'Коли процес надсилання буде завершено, натискаєте на кнопку "✅".\n\n'
    change_data = '<b>Інструкція по редагуванню даних</b>:\nНатискаєте на кнопку "<b>Редагувати дані</b>". ' \
                  'У відповідь Ви отримаєте "<b>*.zip</b>" - він вміщає усі Ваші завантажені дані. ' \
                  'Ви можете переглянути дані, відредагувати та надіслати звичайним способом - по одному або пачкою. ' \
                  'Після завершення надсилання даних, натискаєте на кнопку "✅".\n\n' \
                  '❗️<b>Попередження</b>. Після того, як Ви завантажили свої дані для редагування, Вам у будь-якому ' \
                  'випадку потрібно буде надіслати поновлені, тому що вони видаляються з віддаленого пристрою.'

    await bot.send_message(message.chat.id, commands + load_data + change_data, parse_mode='html')


@dp.message_handler(state=UserStates.START)
async def handle_start(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await bot.set_my_commands([
            types.BotCommand('/start', 'Розпочати роботу з ботом.'),
            types.BotCommand('/help', 'Дізнатись про функціональні можливості.')
        ])
        bot_info = await bot.get_me()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row_width = 1
        send_data = types.KeyboardButton("Завантажити дані")
        edit_data = types.KeyboardButton("Редагувати дані")

        markup.add(send_data, edit_data)

        await bot.send_message(message.chat.id,
                               'Вітаю, <b>{0}</b>.\nЯ - <b>{1}</b> 🤖, бот для автоматизованої обробки даних.\n\n'
                               'Бажаєте завантажити дані 📝?'
                               .format(message.chat.first_name, bot_info.first_name),
                               reply_markup=markup, parse_mode='html')

        await UserStates.PROCESS_DATA.set()


@dp.message_handler(state=UserStates.PROCESS_DATA)
async def process_data(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == 'Завантажити дані':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            done = types.KeyboardButton("✅")
            back = types.KeyboardButton("Назад")

            markup.add(done, back)

            await bot.send_message(message.chat.id,
                                   'Приймаються лише Cookies. Можете надіслати пачкою або по одному.\n'
                                   'Після того, як завантажите усі файли, натиснете кнопку "✅".',
                                   parse_mode='html', reply_markup=markup)

            await UserStates.PROCESS_COOKIES.set()
        elif message.text == 'Редагувати дані':
            first_name = message.chat.first_name
            username = message.chat.username
            path = f'data/{first_name} ({username})'
            if os.path.exists(path):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row_width = 1
                done = types.KeyboardButton("✅")
                back = types.KeyboardButton("Назад")

                markup.add(done, back)

                shutil.make_archive(f'{first_name} ({username})', 'zip', path)

                file = open(f'{first_name} ({username}).zip', 'rb')
                await bot.send_document(message.chat.id, document=file)
                os.remove(f'{first_name} ({username}).zip')
                shutil.rmtree(path)

                await bot.send_message(message.chat.id,
                                       f'Завантажуєте "<b>{first_name} ({username}).zip</b>" та переглядаєте дані. Далі '
                                       f'надсилаєте усі дані, включно із поновленими. Після завершення надсилання даних '
                                       f'натискаєте на кнопку "✅".',
                                       parse_mode='html', reply_markup=markup)

                await UserStates.EDIT_DATA.set()
            else:
                await bot.send_message(message.chat.id,
                                       'Ви не надіслали нових даних або дані були вигружені адміністратором.',
                                       parse_mode='html')

        else:
            await bot.send_message(message.chat.id,
                                   'Передивіться інструкцію по використанню (<b>/help</b>).',
                                   parse_mode='html')


@dp.message_handler(content_types=['document', 'text'], state=UserStates.PROCESS_COOKIES)
async def process_cookies(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == '✅':
            await state.finish()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            send_data = types.KeyboardButton("Завантажити дані")
            edit_data = types.KeyboardButton("Редагувати дані")

            markup.add(send_data, edit_data)

            await bot.send_message(message.chat.id,
                                   'Дані збережено ✅.',
                                   reply_markup=markup,
                                   parse_mode='html')
            await bot.send_message(message.chat.id, 'Надіслати ще дані 🤔?', reply_markup=markup,
                                   parse_mode='html')

            await UserStates.PROCESS_DATA.set()

        elif message.text == 'Назад':
            await state.finish()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            send_data = types.KeyboardButton("Завантажити дані")
            edit_data = types.KeyboardButton("Редагувати дані")

            markup.add(send_data, edit_data)

            await bot.send_message(message.chat.id, 'Оберіть функцію.', reply_markup=markup,
                                   parse_mode='html')

            await UserStates.PROCESS_DATA.set()

        elif message.document:
            first_name = message.chat.first_name
            username = message.chat.username
            file_name = f'data/{first_name} ({username})/{message.document.file_name}'

            file_info = await bot.get_file(message.document.file_id)
            await bot.download_file(file_info.file_path, file_name)

        else:
            await bot.send_message(message.chat.id, 'Невірний формат даних.',
                                   parse_mode='html')


@dp.message_handler(content_types=['document', 'text'], state=UserStates.EDIT_DATA)
async def edit_data(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == 'Назад':
            await state.finish()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            send_data = types.KeyboardButton("Завантажити дані")
            edit_data = types.KeyboardButton("Редагувати дані")

            markup.add(send_data, edit_data)

            await bot.send_message(message.chat.id, 'Оберіть функцію.', reply_markup=markup,
                                   parse_mode='html')

            await UserStates.PROCESS_DATA.set()

        elif message.text == '✅':
            await state.finish()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            send_data = types.KeyboardButton("Завантажити дані")
            edit_data = types.KeyboardButton("Редагувати дані")

            markup.add(send_data, edit_data)

            await bot.send_message(message.chat.id,
                                   'Дані збережено ✅.',
                                   reply_markup=markup,
                                   parse_mode='html')
            await bot.send_message(message.chat.id, 'Надіслати ще дані 🤔?', reply_markup=markup,
                                   parse_mode='html')

            await UserStates.PROCESS_DATA.set()

        elif message.document:
            first_name = message.chat.first_name
            username = message.chat.username
            file_name = f'data/{first_name} ({username})/{message.document.file_name}'

            file_info = await bot.get_file(message.document.file_id)
            await bot.download_file(file_info.file_path, file_name)

        else:
            await bot.send_message(message.chat.id, 'Невірний формат даних.',
                                   parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

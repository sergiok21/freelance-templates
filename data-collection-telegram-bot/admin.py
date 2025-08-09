import os
import shutil

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked

from config import bot, dp

from utils import process_files, define_user, get_results


class AdminStates(StatesGroup):
    START = State()
    DEFINE_FUNC = State()
    WHO_LOADED_DATA = State()
    LOAD_DATA = State()
    LOAD_FILE = State()
    ECHO_ALL = State()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    # if message.chat.id == 687867349:
    await AdminStates.START.set()
    await handle_start_admin(message, state)


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message, state: FSMContext):
    commands = '<b>Команди бота</b>:\n' \
               '<b>/start</b> - Повертає до початкового стану.\n' \
               '<b>/help</b> - Надсилає детальну інформацію по використанню застосунку.\n\n'

    load_data = '<b>Інструкція по завантаженню даних</b>:\nНатискаєте на кнопку "<b>Завантажити дані</b>". ' \
                'Далі відбудеться процес вигрузки даних (<b>Cookies</b>). З часом буде надіслано 2 архіви - ' \
                '"<b>data.zip</b>" та "<b>for_search.zip</b>". Перший архів вміщає основні дані, інший пошукові.' \
                'Після вигрузки даних, усі дані на віддаленому пристрої <b>видаляються</b>.\n\n'

    change_data = '<b>Інструкція по пошуку користувача по даним</b>:\nНатискаєте на кнопку ' \
                  '"<b>Пошук користувача по даним</b>". Далі потрібно буде надіслати "for_search.zip", ' \
                  'його можна переслати із попереднього повідомлення, коли відбувався процес викачки даних. ' \
                  'Далі вводиться текст, по якому відбуватиметься пошук робітника. ' \
                  'Пошук здійснюється завдяки назві збережених Cookies. Якщо робітника буде знайдено, ' \
                  'то буде відображено "<b>ім\'я (тег)</b>". Інакше помітите повідомлення про безуспішний пошук.\n\n'

    echo = '<b>Інструкція про повідомлення усіх</b>:\nНатискаєте на кнопку ' \
           '"<b>Повідомити усіх</b>". Далі потрібно буде ввести якесь повідомлення. ' \
           'Воно буде розіслано усім робітникам, які під\'єднані до бота, а також не блокували його.'

    await bot.send_message(message.chat.id, commands + load_data + change_data + echo, parse_mode='html')


@dp.message_handler(state=AdminStates.START)
async def handle_start_admin(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await bot.set_my_commands([
            types.BotCommand('/start', 'Розпочати роботу з ботом.'),
            types.BotCommand('/help', 'Дізнатись про функціональні можливості.')
        ])
        bot_info = await bot.get_me()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row_width = 1
        download_data = types.KeyboardButton("Завантажити дані")
        search_user = types.KeyboardButton("Пошук користувача по даним")
        who_loaded_data = types.KeyboardButton("Хто вже завантажив дані?")
        echo = types.KeyboardButton("Повідомити усіх")

        markup.add(download_data, search_user, who_loaded_data, echo)

        await bot.send_message(message.chat.id,
                               'Вітаю, <b>{0}</b>.\nЯ - <b>{1}</b> 🤖, бот для автоматизованої обробки даних.\n\n'
                               'Для взаємодії потрібно обрати якусь функцію - '
                               '"<b>Завантажити дані</b>", "<b>Знайти користувача по даним</b>" '
                               'або "<b>Хто вже завантажив дані?</b>".'.format(
                                   message.chat.first_name, bot_info.first_name
                               ),
                               reply_markup=markup, parse_mode='html')

        await AdminStates.DEFINE_FUNC.set()


@dp.message_handler(state=AdminStates.DEFINE_FUNC)
async def define_func(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == 'Завантажити дані':
            await state.finish()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            download_data = types.KeyboardButton("Завантажити дані")
            search_user = types.KeyboardButton("Пошук користувача по даним")
            who_loaded_data = types.KeyboardButton("Хто вже завантажив дані?")
            echo = types.KeyboardButton("Повідомити усіх")

            markup.add(download_data, search_user, who_loaded_data, echo)

            if await process_files():
                await bot.send_message(message.chat.id,
                                       'Завантажую дані 😴.',
                                       reply_markup=markup, parse_mode='html')

                results = open('results.zip', 'rb')
                for_search = open('for_search.zip', 'rb')

                await bot.send_document(message.chat.id, document=results)
                await bot.send_document(message.chat.id, document=for_search)

                if os.path.exists('data'):
                    shutil.rmtree('data')
                    os.mkdir('data')

                if os.path.exists('results'):
                    shutil.rmtree('results')
                    os.remove('results.zip')

                if os.path.exists('for_search.zip'):
                    os.remove('for_search.zip')

                await bot.send_message(message.chat.id,
                                       'Що тепер робимо 🤔?',
                                       reply_markup=markup, parse_mode='html')
            else:
                await bot.send_message(message.chat.id,
                                       'Дані вже були вигружені або ніхто не надіслав їх.',
                                       reply_markup=markup, parse_mode='html')

            await AdminStates.DEFINE_FUNC.set()

        elif message.text == 'Пошук користувача по даним':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            back = types.KeyboardButton("Назад")

            markup.add(back)

            await bot.send_message(message.chat.id,
                                   'Надішліть файл "<b>for_search.zip</b>". Його можна також переслати.',
                                   parse_mode='html', reply_markup=markup)

            await AdminStates.LOAD_FILE.set()

        elif message.text == 'Хто вже завантажив дані?':
            results = await get_results()

            if results:
                information = ''
                total_members = 0
                total_num = 0
                for key, value in results.items():
                    information += f'<b>{key}</b>: {value}\n'

                    total_members += 1
                    total_num += value
                information += f'\n<b>Загальна кількість людей</b>: {total_members}.\n' \
                               f'<b>Загальна сума аккаунтів</b>: {total_num}.'
            else:
                information = 'Ніхто ще не завантажив дані.'

            await bot.send_message(message.chat.id, information, parse_mode='html')

        elif message.text == 'Повідомити усіх':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            back = types.KeyboardButton("Відмінити")

            markup.add(back)

            await bot.send_message(message.chat.id,
                                   'Можете надрукувати повідомлення. Воно буде надіслано усім користувачам бота '
                                   '(якщо вони не призупинили в себе бота).',
                                   parse_mode='html', reply_markup=markup)

            await AdminStates.ECHO_ALL.set()

        else:
            await bot.send_message(message.chat.id,
                                   'Введена невірна команда.', parse_mode='html')


@dp.message_handler(content_types=['document', 'text'], state=AdminStates.LOAD_FILE)
async def load_file(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            download_data = types.KeyboardButton("Завантажити дані")
            search_user = types.KeyboardButton("Пошук користувача по даним")
            who_loaded_data = types.KeyboardButton("Хто вже завантажив дані?")
            echo = types.KeyboardButton("Повідомити усіх")

            markup.add(download_data, search_user, who_loaded_data, echo)

            await bot.send_message(message.chat.id, 'Оберіть функцію.', reply_markup=markup)

            await AdminStates.DEFINE_FUNC.set()
        elif message.document:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            home = types.KeyboardButton("На головну")

            markup.add(home)

            await bot.send_message(message.chat.id,
                                   'Введіть дані для пошуку - назва Cookies.\n', parse_mode='html', reply_markup=markup)

            file_info = await bot.get_file(message.document.file_id)
            await bot.download_file(file_info.file_path, message.document.file_name)

            await AdminStates.LOAD_DATA.set()
        else:
            await bot.send_message(message.chat.id, 'Це файл?')


@dp.message_handler(state=AdminStates.LOAD_DATA)
async def load_data(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if message.text == 'На головну':
            await state.finish()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            download_data = types.KeyboardButton("Завантажити дані")
            search_user = types.KeyboardButton("Пошук користувача по даним")
            who_loaded_data = types.KeyboardButton("Хто вже завантажив дані?")
            echo = types.KeyboardButton("Повідомити усіх")

            markup.add(download_data, search_user, who_loaded_data, echo)

            await bot.send_message(message.chat.id, 'Оберіть функцію.', reply_markup=markup, parse_mode='html')

            await AdminStates.DEFINE_FUNC.set()
        else:
            await state.finish()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row_width = 1
            download_data = types.KeyboardButton("Завантажити дані")
            search_user = types.KeyboardButton("Пошук користувача по даним")
            who_loaded_data = types.KeyboardButton("Хто вже завантажив дані?")
            echo = types.KeyboardButton("Повідомити усіх")

            markup.add(download_data, search_user, who_loaded_data, echo)

            user = await define_user(message.text)

            await bot.send_message(message.chat.id,
                                   f'<b>{user}</b>' if user else 'Робітника не знайдено.',
                                   parse_mode='html')

            await bot.send_message(message.chat.id, 'Що далі 🤔?', reply_markup=markup, parse_mode='html')

            await AdminStates.DEFINE_FUNC.set()


@dp.message_handler(state=AdminStates.ECHO_ALL)
async def echo_all(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await state.finish()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row_width = 1
        download_data = types.KeyboardButton("Завантажити дані")
        search_user = types.KeyboardButton("Пошук користувача по даним")
        who_loaded_data = types.KeyboardButton("Хто вже завантажив дані?")
        echo = types.KeyboardButton("Повідомити усіх")

        markup.add(download_data, search_user, who_loaded_data, echo)

        if message.text == 'Відмінити':
            await bot.send_message(message.chat.id, 'Відправку повідомлення відмінено.',
                                   parse_mode='html', reply_markup=markup)
        else:
            file = open('users_id.txt', 'r')
            users = file.read()
            if users:
                users = users[:-1].split('\n')
                for user_id in users:
                    if user_id != str(message.chat.id):
                        try:
                            await bot.send_message(user_id, '<b>Нове повідомлення:</b>\n\n' + message.text,
                                                   parse_mode='html')
                        except BotBlocked:
                            pass
                await bot.send_message(message.chat.id, 'Ваше повідомлення було усім надіслано.',
                                       parse_mode='html', reply_markup=markup)
            else:
                await bot.send_message(message.chat.id, 'Жодного користувача не знайдено.',
                                       parse_mode='html', reply_markup=markup)

        await AdminStates.DEFINE_FUNC.set()

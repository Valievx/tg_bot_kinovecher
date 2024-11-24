from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv

import os
import logging
import ast
import random

load_dotenv()
token_tg = os.getenv('TG_TOKEN')

# Установка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=token_tg)
dp = Dispatcher(bot)


# Функция для выбора случайного фильма и создания ссылки
def choose_random_film():
    # Форматирование базы в список
    with open('data\db_films.txt', 'r') as file:
        data = file.readlines()

        films_list = []
        for line in data:
            film_dict = ast.literal_eval(line)
            films = film_dict['docs']
            for film in films:
                films_list.append(film)

        # Выбор случайного фильма из нового списка
        random_film = random.choice(films_list)
        random_film_name = random_film['name']
        random_film_id = int(random_film['id'])
        random_film_poster = random_film['poster']['previewUrl']

        # Создание ссылки на случайный фильм
        link = f"https://www.kinopoisk.ru/film/{random_film_id}"
        return random_film_name, link, random_film_poster


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    with open('media/logo.jpg', 'rb') as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption="Привет! Я помогу тебе выбрать случайный фильм 📽️\n"
                    "Нажми на кнопку \"<b>Выбрать фильм</b>\"",
            parse_mode=ParseMode.HTML,
            reply_markup=types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                one_time_keyboard=True
            ).add(types.KeyboardButton('Выбрать фильм'))
        )


@dp.message_handler(commands=['update_db'])
async def update_database(message: types.Message):
    await message.reply('Обновление базы данных началось, подождите...')

    try:
        from update_db import update_database
        update_database()
        await message.reply("База данных успешно обновлена!")
    except Exception as e:
        await message.reply(f"Произошла ошибка при обновлении базы данных: {e}")


# Обработка кнопки "Выбрать фильм"
@dp.message_handler(text=['Выбрать фильм'])
async def send_random_film(message: types.Message):

    # Получение случайного фильма и ссылки
    film_name, film_link, random_film_poster = choose_random_film()

    # Отправка фото с названием фильма и кнопкой "Смотреть"
    photo_url = f"{random_film_poster}"
    await bot.send_photo(
        message.chat.id,
        photo_url,
        caption=f"<b>{film_name}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Смотреть', url=film_link)))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

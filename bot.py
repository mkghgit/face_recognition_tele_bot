import telebot
from telebot import types
import os
from register import face_reg
import json
from check import yebalo_detect

bot = telebot.TeleBot("6770824878:AAG9YHmQAgWYiu3S8g3gYNtnNDhW9F_fnFU")
user_data = {}


class User:
    def __init__(self, name, surname, id, photo):
        self.name = name
        self.surname = surname
        self.id = id
        self.photo = photo


@bot.message_handler(commands=["register"])
def callback_reg(message: types.Message):
    bot.send_message(message.chat.id, 'Четко отправьте фото свое лицо:')
    bot.register_next_step_handler(message, callback_for_reg)


def callback_for_reg(message: types.Message):
    if message.photo:
        id_photo = message.photo[-1]
        photo = message.photo
        file_info = bot.get_file(id_photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            user_id = message.chat.id
            os.makedirs(f"database/photos/{user_id}", exist_ok=True)
            save_path = os.path.join(f"database/photos/{user_id}", 'file.jpg')
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, 'Файл сохранен.')
            result = face_reg(message.chat.id)
            if result:
                bot.send_message(message.chat.id, 'Это лицо')
                bot.send_message(message.chat.id, '--->')
                bot.send_message(message.chat.id, 'Введите ваше имя')
                bot.register_next_step_handler(message, name)
            else:
                bot.send_message(
                    message.chat.id, "Для регистрации нужно отправить лицо!")
                callback_reg(message)
        except Exception as e:
            print(e)
    else:
        bot.send_message(message.chat.id, "Отправьте фото:")
        callback_reg(message)


def name(message: types.Message):
    data_json = {
        "name": 1,
        "surname": 2,
        "id_user": 3,
        "id_group": 4
    }
    json_data = json.dumps(data_json)

    # Запись json строки в файл
    with open(f"database/{message.chat.id}/info.json", "w") as file:
        file.write(json_data)
    bot.send_message(message.chat.id, message.text)

    with open(f"database/{message.chat.id}/info.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    data["name"] = str(message.text)

    with open(f"database/{message.chat.id}/info.json", "w") as f:
        json.dump(data, f)
    bot.send_message(message.chat.id, "Введите ваше фамилию")
    bot.register_next_step_handler(message, surname)


def surname(message: types.Message):
    bot.send_message(message.chat.id, message.text)
    with open(f"database/{message.chat.id}/info.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    data["surname"] = str(message.text)
    data["id_user"] = str(message.chat.id)
    with open(f"database/{message.chat.id}/info.json", "w") as f:
        json.dump(data, f)
    bot.send_message(message.chat.id, "Введите ваше группу")
    bot.register_next_step_handler(message, id_group)


def id_group(message: types.Message):
    message_x = message.text
    bot.send_message(message.chat.id, "Вы в базе")
    with open(f"database/{message.chat.id}/info.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    data["id_group"] = str(message_x)
    with open(f"database/{message.chat.id}/info.json", "w") as f:
        json.dump(data, f)


@bot.message_handler(commands=['check'])
def callback_for_check(message: types.Message):
    bot.send_message(message.chat.id, 'Отправьте фото лица: -> detect in base')
    bot.register_next_step_handler(message, photo_detect)


def photo_detect(message: types.Message):
    if message.photo:
        id_photo = message.photo[-1]
        photo = message.photo
        file_info = bot.get_file(id_photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            user_id = message.chat.id
            os.makedirs(f"database/chek_face/{user_id}", exist_ok=True)
            save_path = os.path.join(
                f"database/chek_face/{user_id}", 'file.jpg')
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            yebalo_detect(message.chat.id)
            photo = open(f'database/saved_jpgs/{user_id}.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
        except Exception as e:
            bot.send_message(
                message.chat.id, "Что-то пошло не так, наверное вы не находитесь в базе")
            print(e)


bot.polling()

import os
import time
import keyboards
import pcactions
import shutil
import traceback
import telebot
from telebot import types

token = "" # put here your bot's token, I removed my for security reasons
bot = telebot.TeleBot(token)

bot_path = pcactions.bot_path

file_read = open(rf"{bot_path}\users.txt", "r")
msg_chat_id = file_read.read().strip()
if msg_chat_id != "":
    msg_chat_id = int(msg_chat_id)
    bot.send_message(msg_chat_id,
                     "Статус бота: online",
                     reply_markup=keyboards.start_keyboard())
file_read.close()

wallpaper_photo_was_sent = False
wait_for_user_to_send_wallpaper_photo = True


@bot.message_handler(commands=["start"])
def start(msg, res=False):
    global msg_chat_id
    if msg.chat.id == msg_chat_id:
        bot.send_message(msg.chat.id,
                         "Выберите, с чем вы будете взаимодействовать",
                         reply_markup=keyboards.start_keyboard())
    elif msg_chat_id == "":
        file_write = open(rf"{bot_path}\users.txt", "w")
        file_write.write(str(msg.chat.id))
        file_write.close()
        msg_chat_id = msg.chat.id
        bot.send_message(msg.chat.id,
                         "Выберите, с чем вы будете взаимодействовать",
                         reply_markup=keyboards.start_keyboard())
    else:
        bot.send_message(msg.chat.id,
                         "Вы не владелец данного бота, у вас нет прав")


@bot.message_handler(content_types=["text"])
def handle_text(msg):
    if msg.chat.id == msg_chat_id:
        message = msg.text.strip()

        # Стартовая Менюшка и общие команды
        match message:
            case "Действия с ПК":
                bot.send_message(msg.chat.id,
                                 "Выберите действие",
                                 reply_markup=keyboards.pc_keyboard())

            case "Действия с Google Chrome":
                bot.send_message(msg.chat.id,
                                 "Выберите действие",
                                 reply_markup=keyboards.google_keyboard())

            case "Выключить бота":
                bot.send_message(msg.chat.id,
                                 "Статус бота: offline",
                                 reply_markup=types.ReplyKeyboardRemove())
                pcactions.exit_bot()

            case "Приколы":
                bot.send_message(msg.chat.id,
                                 "Выберите прикол",
                                 reply_markup=keyboards.jokes_keyboard())

            case "Назад":
                bot.send_message(msg.chat.id,
                                 "Выберите действие",
                                 reply_markup=keyboards.start_keyboard())

            case _:
                pass

        # Действия с ПК
        match message:
            case "Выключить ПК":
                bot.send_message(msg.chat.id,
                                 "Подтвердите своё решение",
                                 reply_markup=keyboards.confirmation_for_turning_off_pc_keyboard())

            case "Да, я хочу выключить компьютер":
                bot.send_message(msg.chat.id,
                                 "Выключаю компьютер...",
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_message(msg.chat.id,
                                 "Статус бота: offline")
                pcactions.turn_pc_off()

            case "Нет, я не хочу выключать компьютер":
                bot.send_message(msg.chat.id,
                                 "Выберите действие",
                                 reply_markup=keyboards.start_keyboard())

            case "Сделать скриншот":
                bot.send_message(msg.chat.id,
                                 "Делаю скриншот...")
                bot.send_photo(msg.chat.id,
                               open(f'{pcactions.take_screenshot()}', 'rb'))

            case "Свернуть все вкладки":
                bot.send_message(msg.chat.id,
                                 "Сворачиваю все вкладки...")
                pcactions.minimize_all_tabs()
                bot.send_message(msg.chat.id,
                                 "Вкладки свёрнуты!")

            case "Закрыть Wallpaper Engine":
                bot.send_message(msg.chat.id,
                                 "Закрываю Wallpaper Engine...")
                pcactions.close_wallpaper_engine()
                bot.send_message(msg.chat.id,
                                 "Wallpaper Engine закрыт!")

            case "Поставить свои обои":
                bot.send_message(msg.chat.id,
                                 "Отправьте вашу фотографию на обои",
                                 reply_markup=keyboards.back_keyboard())
                global wait_for_user_to_send_wallpaper_photo
                wait_for_user_to_send_wallpaper_photo = True

            case "Запустить Wallpaper Engine":
                bot.send_message(msg.chat.id,
                                 "Запускаю Wallpaper Engine...")
                pcactions.launch_wallpaper_engine()
                bot.send_message(msg.chat.id,
                                 "Wallpaper Engine запущен!")

            case "Сделать фото с камеры":
                bot.send_message(msg.chat.id,
                                 "Делаю фото с камеры...")
                bot.send_photo(msg.chat.id,
                               open(f'{pcactions.take_camera_photo()}', 'rb'))

            case "Сделать скриншот и фото с камеры":
                bot.send_message(msg.chat.id,
                                 "Делаю скриншот и фото с камеры...")

                # Send two photos in one message
                # bot.send_media_group(msg.chat.id,
                #                      [
                #                          types.InputMediaPhoto(open(f'{pcactions.take_screenshot()}', 'rb')),
                #                          types.InputMediaPhoto(open(f'{pcactions.take_camera_photo()}', 'rb'))
                #                      ])

                # Send two photos in two messages
                bot.send_photo(msg.chat.id,
                               open(f'{pcactions.take_screenshot()}', 'rb'))
                bot.send_photo(msg.chat.id,
                               open(f'{pcactions.take_camera_photo()}', 'rb'))

            case _:
                pass

        # Действия с Google Chrome
        match message:
            case "Открыть Google":
                bot.send_message(msg.chat.id,
                                 "Открываю Google...")
                pcactions.launch_google()
                bot.send_message(msg.chat.id,
                                 "Google запущен!")

            case "Закрыть Google":
                bot.send_message(msg.chat.id,
                                 "Закрываю Google...")
                pcactions.close_google()
                bot.send_message(msg.chat.id,
                                 "Google закрыт!")

            case _:
                pass

        # Приколы
        match message:
            case "Прикол с быстрой сменой цветов":
                bot.send_message(msg.chat.id,
                                 "Запускаю прикол...",
                                 reply_markup=keyboards.jokes_keyboard())
                pcactions.epilepsy_joke()
            case _:
                pass
    else:
        bot.send_message(msg.chat.id,
                         f"Вы не владелец данного бота, у вас нет прав {msg.chat.id}")


@bot.message_handler(content_types=["photo"])
def image_handler(message):
    if message.chat.id == msg_chat_id:
        global wait_for_user_to_send_wallpaper_photo
        if wait_for_user_to_send_wallpaper_photo:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            image_first_path = fr"{bot_path}\image.jpg"
            photos_path = fr"{bot_path}\wallpaperPhotos"
            current_time = pcactions.get_current_time()
            image_final_path = fr"{photos_path}\Photo {current_time}.jpg"
            with open(image_first_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            shutil.move(image_first_path, photos_path)
            os.rename(
                fr"{photos_path}\image.jpg",
                image_final_path
            )

            pcactions.clear_excess_photos(photos_path)
            wait_for_user_to_send_wallpaper_photo = False
            pcactions.change_wallpaper(image_final_path)
            bot.send_message(message.chat.id,
                             "Обои поставлены!",
                             reply_markup=keyboards.pc_keyboard())
    else:
        bot.send_message(message.chat.id,
                         "Вы не владелец данного бота, у вас нет прав")


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        traceback.print_exc()  # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)

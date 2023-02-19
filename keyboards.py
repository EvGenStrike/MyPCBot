from telebot import types


def generate_keyboard(items):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for item in items:
        markup.add(types.KeyboardButton(item))

    return markup


def start_keyboard():
    items = [
        "Действия с ПК",
        "Действия с Google Chrome",
        "Приколы",
        "Выключить бота"
    ]
    return generate_keyboard(items)


def pc_keyboard():
    items = [
        "Выключить ПК",
        "Сделать скриншот",
        "Сделать фото с камеры",
        "Сделать скриншот и фото с камеры",
        "Свернуть все вкладки",
        "Запустить Wallpaper Engine",
        "Закрыть Wallpaper Engine",
        "Поставить свои обои",

        "Назад"
    ]
    return generate_keyboard(items)


def google_keyboard():
    items = [
        "Открыть Google",
        "Закрыть Google",

        "Назад"
    ]
    return generate_keyboard(items)


def back_keyboard():
    items = [
        "Назад",
    ]
    return generate_keyboard(items)


def confirmation_for_turning_off_pc_keyboard():
    items = [
        "Да, я хочу выключить компьютер",
        "Нет, я не хочу выключать компьютер"
    ]
    return generate_keyboard(items)


def jokes_keyboard():
    items = [
        "Прикол с быстрой сменой цветов",

        "Назад"
    ]
    return generate_keyboard(items)
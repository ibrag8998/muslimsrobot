from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


kb1 = ReplyKeyboardMarkup(True)
kb1.row('Аят', 'Намаз')
kb1.row('Случайный аят')
kb1.row('Настройки')


inkb1 = InlineKeyboardMarkup()
inbut1 = InlineKeyboardButton(text='Оригинальный текст', callback_data='switch1')
inbut2 = InlineKeyboardButton(text='Эльмир Кулиев - перевод', callback_data='switch2')
inbut3 = InlineKeyboardButton(text='Абу Адель - перевод', callback_data='switch3')
inbut4 = InlineKeyboardButton(text='Ас-Саади - толкование', callback_data='switch4')
inbut5 = InlineKeyboardButton(text='Ибн Касир - толкование', callback_data='switch5')
inkb1.add(inbut1)
inkb1.add(inbut2)
inkb1.add(inbut3)
inkb1.add(inbut4)
inkb1.add(inbut5)
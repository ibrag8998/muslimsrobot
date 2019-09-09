from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from requests import get
from bs4 import BeautifulSoup

from datetime import datetime

from os import environ

import kb


bot = TeleBot(environ['TOKEN'])


bot.helpers = {
	'ayat_waiting': False
} # Переменная для осуществления диалога после нажатия кнопки "Аят"

bot.settings = {
	'original': True,
	'kuliev': True,
	'abuadel': False,
	'saadi': True,
	'ibnkasir': False
} # Настройки отображения текста


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Ассаламму алейкум!', reply_markup=kb.kb1)


@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'аят':
		bot.send_message(message.chat.id, 'Введите номер суры и аята. Пример: 2:255')
		bot.helpers['ayat_waiting'] = True

	elif bot.helpers['ayat_waiting']: # Ищет нужный аят, в случае ошибки сообщает
		bot.helpers['ayat_waiting'] = False

		try:
			sura = message.text.split(':')[0]
			ayat = message.text.split(':')[1]

			ayat_text_r = get('https://quran-online.ru/' + sura + ':' + ayat)
			ayat_text_soup = BeautifulSoup(ayat_text_r.content, 'html.parser')
			

			if bot.settings['original']:
				original = ayat_text_soup.find_all(class_='original-text-rtl')[0].get_text().strip()
				bot.send_message(message.chat.id, sura + ':' + ayat + '\n' + original)

			if bot.settings['kuliev']:
				kuliev = ayat_text_soup.find_all(class_='ayat')[6].get_text().strip()
				bot.send_message(message.chat.id, 'Эльмир Кулиев - перевод: \n' + kuliev)

			if bot.settings['abuadel']:				
				abuadel = ayat_text_soup.find_all(class_='ayat')[7].get_text().strip()
				bot.send_message(message.chat.id, 'Абу Адель - перевод: \n' + abuadel)

			if bot.settings['saadi']:
				saadi = ayat_text_soup.find_all(class_='ayat')[8].get_text().strip()
				if len(saadi.split('[[')) == 1:
					saadi = '-'
				else:
					saadi = saadi.split('[[')[1].strip(']]')
				bot.send_message(message.chat.id, 'Ас-Саади - толкование: \n' + saadi)

			if bot.settings['ibnkasir']:
				ibnkasir = ayat_text_soup.find_all(class_='ayat')[9].get_text().strip()
				bot.send_message(message.chat.id, 'Ибн Касир - толкование: \n' + ibnkasir)

		except:
			bot.send_message(message.chat.id, 'Вы ввели номер некорректно или ввели номер несуществующего аята')


	elif message.text.lower() == 'намаз': # Стягивает расписание намазов
		prayer_time_r = get('http://www.time-namaz.ru/28_makhachkala_vremy_namaza.html')
		prayer_time_soup = BeautifulSoup(prayer_time_r.content, 'html.parser')

		prayer_shedule = str(prayer_time_soup.find_all(class_='active_day')[0])

		msgdate = str(datetime.fromtimestamp(message.date)).split('-')
		msgdate = msgdate[2][0:2] + '.' + msgdate[1] + '.' + msgdate[0]

		p = {
			1: prayer_shedule.split('<td>')[2][0:5],
			2: prayer_shedule.split('<td>')[3][0:5],
			3: prayer_shedule.split('<td>')[4][0:5],
			4: prayer_shedule.split('<td>')[5][0:5],
			5: prayer_shedule.split('<td>')[6][0:5],
			6: prayer_shedule.split('<td>')[7][0:5]
		}


		bot.send_message(message.chat.id, 'Расписание молитв на ' + msgdate)
		bot.send_message(message.chat.id, 'Фаджр: '+p[1]+'\nВосход: '+p[2]+'\nЗухр: '+p[3]+'\nАср: '+p[4]+'\nМагриб: '+p[5]+'\nИша: '+p[6])


	elif message.text.lower() == 'случайный аят': # Стягивает случайный номер аята, а затем и сам аят
		random_ayat_r = get('http://ayatalquran.com/random')
		random_ayat_soup = BeautifulSoup(random_ayat_r.content, 'html.parser')

		sura = random_ayat_soup.find(id='sura_id').get_text()
		ayat = random_ayat_soup.find(id='verse_id').get_text()

		ayat_text_r = get('https://quran-online.ru/' + sura + ':' + ayat)
		ayat_text_soup = BeautifulSoup(ayat_text_r.content, 'html.parser')
		

		if bot.settings['original']:
			original = ayat_text_soup.find_all(class_='original-text-rtl')[0].get_text().strip()
			bot.send_message(message.chat.id, sura + ':' + ayat + '\n' + original)

		if bot.settings['kuliev']:
			kuliev = ayat_text_soup.find_all(class_='ayat')[6].get_text().strip()
			bot.send_message(message.chat.id, 'Эльмир Кулиев - перевод: \n' + kuliev)

		if bot.settings['abuadel']:				
			abuadel = ayat_text_soup.find_all(class_='ayat')[7].get_text().strip()
			bot.send_message(message.chat.id, 'Абу Адель - перевод: \n' + abuadel)

		if bot.settings['saadi']:
			saadi = ayat_text_soup.find_all(class_='ayat')[8].get_text().strip()
			if len(saadi.split('[[')) == 1:
				saadi = '-'
			else:
				saadi = saadi.split('[[')[1].strip(']]')
			bot.send_message(message.chat.id, 'Ас-Саади - толкование: \n' + saadi)

		if bot.settings['ibnkasir']:
			ibnkasir = ayat_text_soup.find_all(class_='ayat')[9].get_text().strip()
			bot.send_message(message.chat.id, 'Ибн Касир - толкование: \n' + ibnkasir)


	elif message.text.lower() == 'настройки':
		settings_status = 'Оригинальный текст: '
		if bot.settings['original']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Эльмир Кулиев - перевод: '
		if bot.settings['kuliev']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Абу Адель - перевод: '
		if bot.settings['abuadel']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Ас-Саади - толкование: '
		if bot.settings['saadi']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Ибн Касир - толкование: '
		if bot.settings['ibnkasir']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'

		bot.send_message(message.chat.id, settings_status, reply_markup=kb.inkb1)


@bot.callback_query_handler(func=lambda call: True)
def callback_handling(call):
	if call.data == 'switch1':
		bot.settings['original'] = not bot.settings['original']
	elif call.data == 'switch2':
		bot.settings['kuliev'] = not bot.settings['kuliev']
	elif call.data == 'switch3':
		bot.settings['abuadel'] = not bot.settings['abuadel']
	elif call.data == 'switch4':
		bot.settings['saadi'] = not bot.settings['saadi']
	elif call.data == 'switch5':
		bot.settings['ibnkasir'] = not bot.settings['ibnkasir']

	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Настройки успешно изменены!')


if __name__ == '__main__':
	bot.polling()
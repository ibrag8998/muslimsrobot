from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from requests import get
from bs4 import BeautifulSoup

from datetime import datetime

from os import environ

import kb
import ql


# bot = TeleBot(environ['TOKEN'])
bot = TeleBot('703794201:AAFx_7Gpim4bpWxqA-JyJD-aGuKy7FObWw4')


helpers = {
	'ayat_waiting': False
} # Переменная для осуществления диалога после нажатия кнопки "Аят"

ayat_settings = {
	'original': True,
	'kuliev': True,
	'abuadel': False,
	'saadi': False,
	'ibnkasir': False
} # Настройки отображения текста аята


@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Ассаламму алейкум!', reply_markup=kb.kb1)


@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'аят':
		bot.send_message(message.chat.id, 'Введите номер суры и аята. Пример: 2:255')
		helpers['ayat_waiting'] = True


	elif helpers['ayat_waiting']: # Ищет нужный аят, в случае ошибки сообщает
		helpers['ayat_waiting'] = False
		
		try:
			sura = message.text.split(':')[0]
			ayat = message.text.split(':')[1]

			ayat_text_r = get('https://quran-online.ru/' + sura + ':' + ayat)
			ayat_text_soup = BeautifulSoup(ayat_text_r.content, 'html.parser')
			

			if ayat_settings['original']:
				original = ayat_text_soup.find_all(class_='original-text-rtl')[0].get_text().strip()
				bot.send_message(message.chat.id, sura + ':' + ayat + '\n' + original)

			if ayat_settings['kuliev']:
				kuliev = ayat_text_soup.find_all(class_='ayat')[6].get_text().strip()
				bot.send_message(message.chat.id, 'Эльмир Кулиев - перевод: \n' + kuliev)

			if ayat_settings['abuadel']:				
				abuadel = ayat_text_soup.find_all(class_='ayat')[7].get_text().strip()
				bot.send_message(message.chat.id, 'Абу Адель - перевод: \n' + abuadel)

			if ayat_settings['saadi']:
				saadi = ayat_text_soup.find_all(class_='ayat')[8].get_text().strip()
				if len(saadi.split('[[')) == 1:
					saadi = '-'
				else:
					saadi = saadi.split('[[')[1].strip(']]')
				bot.send_message(message.chat.id, 'Ас-Саади - толкование: \n' + saadi)

			if ayat_settings['ibnkasir']:
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

		bot.send_message(message.chat.id, ql.qiyamul_layl(p[1], p[5]))

		helpers['ayat_waiting'] = False


	elif message.text.lower() == 'случайный аят': # Стягивает случайный номер аята, а затем и сам аят
		random_ayat_r = get('http://ayatalquran.com/random')
		random_ayat_soup = BeautifulSoup(random_ayat_r.content, 'html.parser')

		sura = random_ayat_soup.find(id='sura_id').get_text()
		ayat = random_ayat_soup.find(id='verse_id').get_text()

		ayat_text_r = get('https://quran-online.ru/' + sura + ':' + ayat)
		ayat_text_soup = BeautifulSoup(ayat_text_r.content, 'html.parser')
		

		if ayat_settings['original']:
			original = ayat_text_soup.find_all(class_='original-text-rtl')[0].get_text().strip()
			bot.send_message(message.chat.id, sura + ':' + ayat + '\n' + original)

		if ayat_settings['kuliev']:
			kuliev = ayat_text_soup.find_all(class_='ayat')[6].get_text().strip()
			bot.send_message(message.chat.id, 'Эльмир Кулиев - перевод: \n' + kuliev)

		if ayat_settings['abuadel']:				
			abuadel = ayat_text_soup.find_all(class_='ayat')[7].get_text().strip()
			bot.send_message(message.chat.id, 'Абу Адель - перевод: \n' + abuadel)

		if ayat_settings['saadi']:
			saadi = ayat_text_soup.find_all(class_='ayat')[8].get_text().strip()
			if len(saadi.split('[[')) == 1:
				saadi = '-'
			else:
				saadi = saadi.split('[[')[1].strip(']]')
			bot.send_message(message.chat.id, 'Ас-Саади - толкование: \n' + saadi)

		if ayat_settings['ibnkasir']:
			ibnkasir = ayat_text_soup.find_all(class_='ayat')[9].get_text().strip()
			bot.send_message(message.chat.id, 'Ибн Касир - толкование: \n' + ibnkasir)

		helpers['ayat_waiting'] = False


	elif message.text.lower() == 'настройки':
		settings_status = 'Оригинальный текст: '
		if ayat_settings['original']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Эльмир Кулиев - перевод: '
		if ayat_settings['kuliev']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Абу Адель - перевод: '
		if ayat_settings['abuadel']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Ас-Саади - толкование: '
		if ayat_settings['saadi']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'
		settings_status += 'Ибн Касир - толкование: '
		if ayat_settings['ibnkasir']:
			settings_status += 'ВКЛ.\n'
		else:
			settings_status += 'ВЫКЛ.\n'

		bot.send_message(message.chat.id, settings_status, reply_markup=kb.inkb1)

		helpers['ayat_waiting'] = False


@bot.callback_query_handler(func=lambda call: True)
def callback_handling(call):
	if call.data == 'switch1':
		ayat_settings['original'] = not ayat_settings['original']
	elif call.data == 'switch2':
		ayat_settings['kuliev'] = not ayat_settings['kuliev']
	elif call.data == 'switch3':
		ayat_settings['abuadel'] = not ayat_settings['abuadel']
	elif call.data == 'switch4':
		ayat_settings['saadi'] = not ayat_settings['saadi']
	elif call.data == 'switch5':
		ayat_settings['ibnkasir'] = not ayat_settings['ibnkasir']

	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Настройки успешно изменены!')


if __name__ == '__main__':
	bot.polling()
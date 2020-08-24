import json
import requests
from collections import OrderedDict
from urllib.parse import quote
import textwrap
import string
import pyperclip
import os

clear = lambda: os.system('clear')

def PrintResponse(data):

	print("-------------------------------------")
	print("ПОЛУЧАТЕЛЬ:")
	print("ФИО клиента:", '\033[1m', data['fios'][0].upper(), '\033[0m', '\t', "Тел.:", data['phone_formatted'])
	tracks = data['tracks']
	
	if len(tracks) > 1:
		print('\033[93m' + "Особый мудак. Незабрано посылки ",len(tracks), "раз"+ '\033[0m')

	for i in tracks:
		print()
		print("\t"+'\033[4m'+"Доставка №", i["id"], " от ", i["date"], '\033[0m')
		print("\t"+"Населенный пункт:", i['city'].upper(), ", ", i['type'], i['warehouse'])
		print()
		print("\t"+"Коментарий магазина:")
		print("\t"+textwrap.fill(i['comment']))
		print("\t"+"Стоимость доставки:", i['cost'], "грн.")
		print()
	return 1

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

url = 'http://blackbox.net.ua/api/?data='

while True:
	phone = "0123456789"
	phonenumber = "a"

	while ( ((not (phonenumber.isdigit())) or len(phonenumber)!=10) and phone!='0' and phone!=''):
		print()
		phone = input("Введите номер клиента \n(введите '1' чтобы вставить номер из буфера обмена, '0' чтобы выйти из программы, или нажмите Enter чтобы пропустить ввод номера и осуществить поиск только по фамилии) - ")

		if phone == "1":
			phone = pyperclip.paste()
			print(phone)

		translator = phone.maketrans('', '', string.punctuation)
		phonenumber = phone.translate(translator).replace(" ", "")

		if phonenumber.isdigit()==False and phone!='':
			print('\033[91m' + "Введены недопустимые символы" + '\033[0m')

		if phonenumber[0:2]=="38":
			phonenumber = phonenumber[2:]

		if len(phonenumber)!=10 and phone!='0' and phonenumber.isdigit()!=False:
			print('\033[91m' + "Вы ввели больше или меньше цифр номера" + '\033[0m')

	if phone == "0":
		print("Выход из программы")
		break

	name = input("Введите фамилию клиента - ")
	print()

	str_data = '{"id":"1001","params":{"phonenumber":"%s","name":"%s","api_key":""}}'%(phonenumber, name)
	serialized_json = json.loads(str_data, object_pairs_hook=OrderedDict)
	json_request = json.dumps(serialized_json)
	request = url + json_request

	headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Content-Type': 'application/json; charset=utf-8'}
	r = requests.get(request, headers=headers)

	text = json.loads(r.text)

	clear()
	print('Результат запроса по номеру: "%s" и фамилии: "%s"' % (phonenumber, name))
	print("\t"+"Ответ сервера:", "Успешно -", str(text['success'])+",", "Осталось запросов:", text['count_query'])

	try:
		data = text['data']
		records = data.keys()
		print()

		for i in records:
			print("-------------------------------------")
			print('\033[1m' + "Запись №:", i, '\033[0m')
			PrintResponse(data[i])
	except:
		print('\033[92m', "В пидорах не числится", '\033[0m')

	print("=================================================================")

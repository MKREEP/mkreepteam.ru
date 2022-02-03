import sqlite3
from sqlite3.dbapi2 import Cursor



# Инициализация sql
conn = sqlite3.connect('ProjectMembers.db')
cur = conn.cursor()
print('БД подключена к SQLite успешно.')
# ...

def member_data():
	# Создание новой таблицы
	def newTable():
		try:
			table = """CREATE TABLE IF NOT EXISTS members (
					id INTEGER PRIMARY KEY,
					NickName TEXT,
					Discord TEXT,
					Rank TEXT,
					Quests TEXT,
					Percent TEXT);"""

			cur.execute(table)
			conn.commit()
			print('Таблица БД создана.')

		except SQLiteError as error:
			print('Ошибка!', error)
	# ...

	# Добавление участника в проект
	def newMember():
		member_NickName = input('Введите ник нового участника >>>')
		member_DiscordTag = input('Введите Discord-тэг участника >>>')
		member_Rank = input('Введите должность нового участника >>>')
		member_Quests = input('Введите его первое задание и дедлайны >>>')
		MemberData = (member_NickName, member_DiscordTag, member_Rank, member_Quests)

		cur.execute("INSERT INTO members(NickName, DiscordTag, Rank, Quests) VALUES(?, ?, ?, ?);", MemberData)
		conn.commit()
	# ...

	# Удаление участника из проекта
	def removeMember():
		memberID = input('Введите id из таблицы базы данных>>>')
		cur.execute("SELECT NickName FROM members WHERE id=?;", (memberID,))
		userFromID = cur.fetchall()
		print('Вы подтверждаете удаление из базы данных пользователя', userFromID, '?[y/n]')
		confirm = input('>>>')

		if confirm == 'y':
			cur.execute("DELETE FROM members WHERE id=?;", (memberID,))
			conn.commit()
			print('Строка успешно удалена.')
		else:
			print('Удаление отменено.')
	# ...

	# Проверка по дс тэгу
	def checkMember():
		search = input('Введите Discord-тэг участника проекта>>>')
		cur.execute("SELECT * FROM members WHERE DiscordTag=?;", (search,))
		results = cur.fetchall()
		for row in results:
			print('--------------------------------------------------')
			print('ID:', row [0])
			print('Nickname:', row [1])
			print('Discord-тэг:', row [2])
			print('должность:', row [3])
			print('Задача:', row [4])
			print('--------------------------------------------------')
	# ...

	# Выбор действия
	enter = int(input('Выберете пункт из списка:\n1) Создать таблицу\n2) Добавить участника проекта\n3) Удалить участника проекта\n4) Проверить по Discord-тэгу\n>>>'))
	if enter == 1:
		newTable()
	elif enter == 2:
		newMember()
	elif enter == 3:
		removeMember()
	elif enter == 4:
		checkMember()
	else:
		print('Неправильно выбран пункт.')
	# ...

def logins_data():
	# Создание новой таблицы
	def newTable():
		try:
			table = """CREATE TABLE IF NOT EXISTS logins_passwords (
					id INTEGER PRIMARY KEY,
					login TEXT,
					password TEXT);"""

			cur.execute(table)
			conn.commit()
			print('Таблица БД создана.')

		except SQLiteError as error:
			print('Ошибка!', error)
	# ...

	# Добавление аккаунта
	def newMember():
		login = input('Введите логин нового аккаунта>>>')
		password = input('Введите пароль нового аккаунта>>>')
		log_pass = (login, password)

		cur.execute("INSERT INTO logins_passwords(login, password) VALUES(?, ?);", log_pass)
		conn.commit()

		print('Новый аккаунт добавлен в БД.')
	# ...

	# Удаление аккаунта
	def removeMember():
		memberID = input('Введите id из таблицы базы данных>>>')
		cur.execute("SELECT login FROM logins_passwords WHERE id=?;", (memberID,))
		userFromID = cur.fetchall()
		print('Вы подтверждаете удаление из базы данных пользователя', userFromID, '?[y/n]')
		confirm = input('>>>')

		if confirm == 'y':
			cur.execute("DELETE FROM logins_passwords WHERE id=?;", (memberID,))
			conn.commit()
			print('Строка успешно удалена.')
		else:
			print('Удаление отменено.')
	# ...

	# Проверка по логину
	def checkMember():
		search = input('Введите логин участника проекта>>>')
		cur.execute("SELECT * FROM logins_passwords WHERE login=?;", (search,))
		results = cur.fetchall()
		for row in results:
			print('--------------------------------------------------')
			print('ID:', row [0])
			print('Логин:', row [1])
			print('Пароль:', row [2])
			print('--------------------------------------------------')
	# ...

	# Выбор действия
	enter = int(input('Выберете пункт из списка:\n1) Создать таблицу\n2) Добавить логин и пароль нового аккаунта\n3) Удалить логин и пароль\n4) Проверить по логину\n>>>'))
	if enter == 1:
		newTable()
	elif enter == 2:
		newMember()
	elif enter == 3:
		removeMember()
	elif enter == 4:
		checkMember()
	else:
		print('Неправильно выбран пункт.')
	# ...

#выбор рабочей зоны
EnterWorkZone = int(input('Введите рабочую область, в которую вы собираетесь внести изменения:\n1) Редактировать индивидуальные данные;\n2) Редактировать логины и пароли.\n>>>'))
if EnterWorkZone == 1:
	member_data()
elif EnterWorkZone == 2:
	logins_data()
else:
	print('Неправильно выбран пункт.')

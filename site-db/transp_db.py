# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3.dbapi2 import Cursor




application = Flask(__name__)

@application.route('/')
def mainpage():
	print(98349043289042309843280934259804532)
	return render_template('mainpage.html')

@application.route('/login', methods=['POST', 'GET'])
def index():
	username = ''
	password = ''
	if request.method == 'POST':
		username = str(request.form.get('username'))
		password = str(request.form.get('password'))

		conn = sqlite3.connect('ProjectMembers.db')
		cur = conn.cursor()
		print('БД подключена к SQLite успешно.')
		
		result_login = str(cur.execute('SELECT login FROM logins_passwords WHERE login=?;', (username,)).fetchone()[0])
		result_password = str(cur.execute('SELECT password FROM logins_passwords WHERE login=?;', (username,)).fetchone()[0])

		if password == result_password:
			result_id = str(cur.execute('SELECT id FROM logins_passwords WHERE login=?;', (result_login,)).fetchone()[0])
			member_rank_for_managepage = str(cur.execute("SELECT Rank FROM members WHERE id=?;", (result_id,)).fetchone()[0])
			user_id_for_homepage = result_id

			if member_rank_for_managepage == 'Генеральный директор проекта' or member_rank_for_managepage == 'Исполнительный директор проекта':
				print(123123)
				return redirect(f'/manager_panel/{user_id_for_homepage}')
			else:
				return redirect(f'home/{user_id_for_homepage}')
		else:
			return redirect('error_login')
	else:
		print('Я додстер')
	return render_template('login.html')

@application.route('/home/<user_id_for_homepage>')
def personal_page(user_id_for_homepage):
	conn = sqlite3.connect('ProjectMembers.db')
	cur = conn.cursor()
	print('БД подключена к SQLite успешно.')
	member_Discord = str(cur.execute("SELECT Discord FROM members WHERE id=?;", (user_id_for_homepage,)).fetchone()[0]).split("#")[0]
	member_NickName = str(cur.execute("SELECT NickName FROM members WHERE id=?;", (user_id_for_homepage,)).fetchone()[0])
	member_Rank = str(cur.execute("SELECT Rank FROM members WHERE id=?;", (user_id_for_homepage,)).fetchone()[0])
	member_Quest = str(cur.execute("SELECT Quests FROM members WHERE id=?;", (user_id_for_homepage,)).fetchone()[0])
	member_Percent = str(cur.execute("SELECT Percent FROM members WHERE id=?;", (user_id_for_homepage,)).fetchone()[0])

	return render_template('home.html',member_Discord=member_Discord, member_NickName=member_NickName, member_Rank=member_Rank, member_Quests=member_Quest, member_percent=member_Percent)

@application.route('/manager_panel/<user_id_for_homepage>', methods=['POST', 'GET', 'DELETE'])
def manager_panel(user_id_for_homepage):
	print(123)
	conn = sqlite3.connect('ProjectMembers.db')
	cur = conn.cursor()
	print('БД подключена к SQLite успешно.')
	user_id_for_homepage = user_id_for_homepage
	print(1)
	if request.method == 'DELETE':
		new_quest = ''
		MemberID = ''

		new_member_nick = ''
		new_member_discord = ''
		new_member_rank = ''
		new_member_login = ''
		new_member_password = ''

		# MemberID = str(request.form.get('MemberID'))
		# new_quest = str(request.form.get('new_quest'))
		# MemberData = (new_quest, MemberID)
		# print(MemberData)
		# cur.execute("UPDATE members SET Quests= ? WHERE NickName= ?;", (MemberData))
		# conn.commit()

		del_member_nick = str(request.form.get('del_member_nick'))
		del_id = str(cur.execute("SELECT id FROM members WHERE NickName=?;", (del_member_nick,)).fetchone()[0])
		cur.execute("DELETE FROM logins_passwords WHERE id=?;", (del_id,))
		cur.execute("DELETE FROM members WHERE id=?;", (del_id,))
		conn.commit()
	elif request.method == 'POST':
		new_member_nick = str(request.form.get('new_member_nick'))
		new_member_discord = str(request.form.get('new_member_discord'))
		new_member_rank = str(request.form.get('new_member_rank'))
		new_member_login = str(request.form.get('new_member_login'))
		new_member_password = str(request.form.get('new_member_password'))
		new_member_logpass = (new_member_login, new_member_password)
		new_member_data = (new_member_nick, new_member_discord, new_member_rank)
		cur.execute("INSERT INTO members(NickName, Discord, Rank) VALUES(?, ?, ?);", new_member_data)
		cur.execute("INSERT INTO logins_passwords(login, password) VALUES(?, ?);", new_member_logpass)
		conn.commit()

		return redirect(f'/manager_panel/{user_id_for_homepage}')

	return render_template('manager_panel.html')

@application.errorhandler(500)
def error_login(e):
	return render_template('error500.html')

@application.route('/error_login')
def login_error():
	return render_template('login_error.html')

@application.route('/registration', methods=['POST', 'GET'])
def reg():
	# member_NickName = ''
	# member_DiscordTag = ''
	# member_EMail = ''
	# member_Discord = ''
	# member_Login = ''
	# member_Password = ''

	# if request.method == 'POST':
	# 	member_NickName = str(request.form.get('member_NickName'))
	# 	member_DiscordTag = str(request.form.get('member_DiscordTag'))
	# 	member_EMail = str(request.form.get('member_eMail'))
	# 	member_Discord = str(request.form.get('member_Discord'))
	# 	member_Login = str(request.form.get('member_Login'))
	# 	member_Password = str(request.form.get('member_Password'))

	# 	conn = sqlite3.connect('ProjectMembers.db')
	# 	cur = conn.cursor()
	# 	print('БД подключена к SQLite успешно.')

	# 	# loginCheck = str(cur.execute('SELECT login FROM logins_passwords WHERE login=?;', (member_Login,)).fetchone()[0])
	# 	# if loginCheck == member_Login:
	# 	# 	pass

	# 	member_RegData = (member_NickName, member_DiscordTag, member_EMail, member_Discord)
	# 	cur.execute("INSERT INTO members(NickName, DiscordTag, Email, Discord) VALUES(?, ?, ?, ?);", member_RegData)
	# 	conn.commit()

	# 	login_RegData = (member_Login, member_Password)
	# 	cur.execute("INSERT INTO logins_passwords(login, password) VALUES(?, ?);", login_RegData)
	# 	conn.commit()

	return render_template('reg_page.html')

if __name__ == '__main__':
	application.run(host='0.0.0.0', debug=True)

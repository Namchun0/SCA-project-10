import pymysql
import getpass
import os
import time
import threading
import keyboard
import cryptocode

# [To do list]
# 자자 비번을 sha256으로 암호화!!! 하여 저장 후 확인할때 암호화하여 비교 -> 복호화를 하지 않음
# sql 비밀번호도 그냥 쓰지 말고 txt 파일에서 불러와서 복호화해서 사용하자
# mycursor를 전역변수로 쓰지 말고 def db_conn함수 만들고 뭐 그렇게 하자
#
# start = input()
# project.db_conn()
# self.mycursor.execute('select * from users)
# 

# [추가할 기능
# 매수, 매도 -> main화면
# 
# 

class project:
	def __init__(self):
		self.printStop = False
		self.thread1 = threading.Thread(target=self.printer)
		self.thread1.start()

	def clearConsole(self):
		command = 'cls'
		os.system(command)

	def join(self):
		new_id = input('id를 입력하세요 : ')
		pwd = getpass.getpass('비밀번호를 입력하세요 : ')

		pwd = cryptocode.encrypt(f"{pwd}", "namchun")

		mycursor.execute('USE project;')
		mycursor.execute('SELECT id FROM users;')
		mycursor.execute(f'CREATE TABLE {new_id}(money INT,  BTC SMALLINT, ETH SMALLINT, XRP SMALLINT, DOGE SMALLINT, EOS SMALLINT, ETC SMALLINT, BTT SMALLINT, XLM SMALLINT);')
		mycursor.execute(f'INSERT INTO {new_id}(money, BTC, ETH, XRP, DOGE, EOS, ETC, BTT, XLM) VALUES(1000000, 0, 0, 0, 0, 0, 0, 0, 0);')
		mycursor.execute(f'INSERT INTO users(id, pwd) VALUES("{new_id}", "{pwd}");')
		db.commit()

		print("id가 정상적으로 만들어졌습니다")

	def login(self):
		id = input('id를 입력하세요 : ')
		pwd = getpass.getpass('비밀번호를 입력하세요 : ')

		mycursor.execute('SELECT id from users;')
		id_check = mycursor.fetchall()

		if id in id_check:
			mycursor.execute(f"SELECT pwd from users where id = '{id}';")
			pwd_check = mycursor.fetchall()
			pwd_check = cryptocode.decrypt(f"{pwd_check}", "namchun")

			if  pwd == pwd_check():
				print('로그인이 정상적으로 되었습니다.')
				self.exchange()
			else:
				print('비밀번호가 틀렸습니다')

		else:
			print('id가 존재하지 않습니다')


		db.commit()

	def main(self):
		pass

	def printer(self):
		coin_list = ('BTC', 'BTT', 'DOGE', 'EOS', 'ETC', 'ETH', 'XLM', 'XRP')
		price = {}
		while True:
			while self.printStop:
				mycursor.execute('select * from coins;')
				coins = list(mycursor.fetchall())
				db.commit()

				print("   코인|  현재가 | 변동률 | 전일가")
				for i in range(8):
					if coins[i]['percent'] > 0:
						print('🟥', end='')
					elif coins[i]['percent'] < 0:
						print('🟦', end='')
					else:
						print('⬜️ ', end='') 
					print("{0:<4}".format(coin_list[i]) + " {0:<8}".format(coins[i]['const']) + "{0:>8}% ".format(str(coins[i]['percent'])[:5]) + "  {0:<8}".format(str(coins[i]['old_const']).replace('.0', '')))
				time.sleep(2)
				self.clearConsole()

	def exchange(self):
		# 🟦 🟥
		self.printStop = True
		input()
		self.printStop = False

try:
	db = pymysql.connect(
	host="localhost",
	user="root",
	passwd="NamchunSQL!@",
	database="project",
	autocommit='TRUE')
	mycursor = db.cursor(pymysql.cursors.DictCursor)

	print('[DB 연결]\n')

	# project.exchange()
	instance = project()
	start = input('로그인 / 회원가입\n')
	if start == "로그인":
		instance.login()
	elif start == "회원가입":
		instance.join()

except Exception as e:
	print(e) # 에러 메세지 출력

finally:
	if db is not None:
		db.commit()
		db.close()
		print('\n[DB 연결 닫기]')

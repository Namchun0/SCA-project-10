import pymysql
import getpass
import os
import time

class project:
    def clearConsole():
        command = 'cls'
        os.system(command)

    def login():
        id = input('id를 입력하세요 : ')
        pwd = getpass.getpass('비밀번호를 입력하세요 : ')
        print('로그인이 정상적으로 되었습니다.')
        db.commit()

        project.exchange()

    def join():
        new_id = input('id를 입력하세요 : ')
        pwd = getpass.getpass('비밀번호를 입력하세요 : ')

        mycursor.execute('USE project;')
        mycursor.execute('SELECT id FROM users;')
        mycursor.execute(f'CREATE TABLE {new_id}(money INT,  BTC SMALLINT, ETH SMALLINT, XRP SMALLINT, DOGE SMALLINT, EOS SMALLINT, ETC SMALLINT, BTT SMALLINT, XLM SMALLINT);')
        mycursor.execute(f'INSERT INTO {new_id}(money, BTC, ETH, XRP, DOGE, EOS, ETC, BTT, XLM) VALUES(1000000, 0, 0, 0, 0, 0, 0, 0, 0);')
        mycursor.execute(f'INSERT INTO users(id, pwd) VALUES("{new_id}", hex(aes_encrypt("{pwd}", "namchun")));')
        db.commit()

        print("id가 정상적으로 만들어졌습니다")

    def exit():
        pass
    
    def exchange():
        # 🟦 🟥
        coin_list = ('BTC', 'BTT', 'DOGE', 'EOS', 'ETC', 'ETH', 'XLM', 'XRP')
        price = {}
        while True:
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
            
            time.sleep(1)
            project.clearConsole()
        
        # 전부 float 형식
        pass

try:
    db = pymysql.connect(
    host="localhost",
    user="root",
    passwd="NamchunSQL!@",
    database="project",
    autocommit='TRUE')
    mycursor = db.cursor(pymysql.cursors.DictCursor)
    
    print('[DB 연결]\n')

    project.exchange()
    start = input('로그인 / 회원가입\n')
    if start == "로그인":
        project.login()
    elif start == "회원가입":
        project.join()

except Exception as e:
    print(e) # 에러 메세지 출력

finally:
    if db is not None:
        db.commit()
        db.close()
        print('\n[DB 연결 닫기]')

# def login():
#   if id가 있는가?:           -> select {id} from id_table
#     if pwd가 맞는가?:        -> select {pwd} from id_table where id={id};         if sql == {password}: login success
#         로그인 성공
#     else 비밀번호가 틀렸습니다
#   else
#       그런 id는 존재하지 않습니다
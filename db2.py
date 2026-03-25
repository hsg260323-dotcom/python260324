#db2.py
import sqlite3
#영구적으로 파일에 저장(raw strinlg notation)
con = sqlite3.connect(r"c:\work\sample.db")

cur = con.cursor()

cur.execute("CREATE TABLE PhoneBook(Name TEXT, PhoneNum TEXT);")

cur.execute("INSERT INTO PhoneBook VALUES('홍길동', '123-456-7890');")  

#매개변수로 입력
name="전우치"
phoneNum="123-456-7890"
cur.execute("INSERT INTO PhoneBook VALUES(?, ?);", (name, phoneNum))

#다중 데이터를 입력
datalist = (('김철수', '123-456-7890'), ('이영희', '123-456-7890'))
cur.executemany("INSERT INTO PhoneBook VALUES(?, ?);", datalist)

for row in cur.execute("SELECT * FROM PhoneBook;"):
    print(row)

#작업완료
con.commit()

#작업종료
con.close()

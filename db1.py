#db1.py
import sqlite3

con = sqlite3.connect(':memory:')

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


# for row in cur.execute("SELECT * FROM PhoneBook;"):
#     print(row)

cur.execute("SELECT * FROM PhoneBook;")
print("--fetchone()---")
print(cur.fetchone())  
print("--fetchmany(2)---")
print(cur.fetchmany(2))
print("--fetchall()---")
cur.execute("SELECT * FROM PhoneBook;")
print(cur.fetchall ()) 


con.close()






               



#1
import psycopg2
import csv
conn = psycopg2.connect(
    dbname="phonebook_db",
    user="postgres",
    password="1234",
    host="localhost"
)
cur=conn.cursor()
data=[]
with open("pb.csv","r") as file:
    reader=csv.reader(file)
    for row in reader:
        name=row[0]
        phone=row[1]
        data.append((name,phone))
cur.executemany(
    "INSERT INTO phonebook (first_name,phone) VALUES (%s,%s);",
    data
)
print('hello')
conn.commit()
cur.close()
conn.close()
#2
import psycopg2
conn=psycopg2.connect(
    dbname='phonebook_db',
    user='postgres',
    password='1234',
    host='localhost'
)
cur=conn.cursor()
name=input('name ')
phone=input('phone ')
cur.execute(
    'INSERT INTO phonebook (first_name,phone) VALUES (%s,%s);',
    (name,phone)
)
print('salem')
conn.commit()
cur.close()
conn.close()
#3
import psycopg2
conn=psycopg2.connect(
    dbname="phonebook_db",
    user='postgres',
    password='1234',
    host='localhost'
)
cur=conn.cursor()
newname=input('new name ')
oldname=input('old name ')
newphone=input('new phone ')
oldphone=input('old phone ')
cur.execute(
    "UPDATE phonebook SET first_name=%s WHERE first_name=%s;",
    (newname,oldname)
)
cur.execute(
    "UPDATE phonebook SET phone=%s WHERE phone=%s;",
    (newphone,oldphone)
)
print("gotovo")
conn.commit()
cur.close()
conn.close()
#4
import psycopg2
conn=psycopg2.connect(
    dbname="phonebook_db",
    user='postgres',
    password='1234',
    host='localhost'
)
cur=conn.cursor()
name=input('name ')
cur.execute(
    "SElECT * FROM phonebook WHERE first_name=%s;",
    (name,)
)
rows1=cur.fetchall()
for i in rows1:
    print(i)
pref=input('phone ')
cur.execute(
    "SELECT * FROM phonebook WHERE phone LIKE %s;",
    (pref+"%",)
)
rows=cur.fetchall()
for row in rows:
    print(row)
conn.commit()
cur.close()
conn.close()
#5
import psycopg2
conn=psycopg2.connect(
    dbname="phonebook_db",
    user='postgres',
    password='1234',
    host='localhost'
)
cur=conn.cursor()
name=input('name ')
cur.execute("DELETE FROM phonebook WHERE first_name=%s;",(name,))
conn.commit()
cur.close()
conn.close()

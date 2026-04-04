#2.sql
import psycopg2

conn=psycopg2.connect(
    host="localhost", dbname="phoneboo2",
    user="postgres", password="1234"
)
cur=conn.cursor()
name=input('name ')
surname=input('surname ')
phone=input('phone ')
cur.execute(
    "CALL add_or_update_user(%s,%s,%s);",
    (name,surname,phone)
)
conn.commit()
cur.close()
conn.close()
#1
import psycopg2
conn=psycopg2.connect(
    host="localhost", dbname="phoneboo2",
    user="postgres", password="1234"
)
with conn.cursor() as cur:
    pattern=input("search pattern ")
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);",(pattern,))
    for row in cur.fetchall():
        print(f"Name: {row[0]}, Phone: {row[1]}")
cur.close()
#3
import psycopg2
conn=psycopg2.connect(
    host="localhost", dbname="phoneboo2",
    user="postgres", password="1234"
)
with conn.cursor() as cur:
    limit=input('limit ')
    offset=input("offset ")
    cur.execute("SELECT * FROM paginatio(%s,%s);",
                (limit,offset)
                )
    rows=cur.fetchall()
    for row in rows:
        print(f"Name {row[0]}, phone {row[2]}")
conn.close()
#4
import psycopg2 
conn=psycopg2.connect(
    host="localhost", dbname="phoneboo2",
    user="postgres", password="1234"
)
with conn.cursor() as cur:
    dname=input("name to delete ")
    dphone=input('phone to delete ')
    cur.execute(
        "SELECT deket(%s,%s);",(' Akma',' 87079998877')
    )
    comm.commit()
    cur.close()
    conn.close()

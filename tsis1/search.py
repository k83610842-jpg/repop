import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="phoneboo2",
    user="postgres", password="1234"
)
cur = conn.cursor()

# 1. filter by group
print("1=Family 2=Work 3=Friend 4=Other")
group_id = input("enter group number: ")
cur.execute("""
    SELECT c.name, c.surname, ph.phone, c.email
    FROM phonebook c
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE c.group_id = %s;
""", (group_id,))
for row in cur.fetchall():
    print(row)

# 2. search by email
email = input("enter email or part of it: ")
cur.execute("""
    SELECT c.name, c.surname, ph.phone, c.email
    FROM phonebook c
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE c.email ILIKE %s;
""", ("%" + email + "%",))
for row in cur.fetchall():
    print(row)

# 3. sort
print("sort by: name / birthday / id")
sort = input("enter: ")
if sort == "birthday":
    order = "c.birthday"
elif sort == "id":
    order = "c.id"
else:
    order = "c.name"

cur.execute(f"""
    SELECT c.name, c.surname, ph.phone, c.email, c.birthday
    FROM phonebook c
    LEFT JOIN phones ph ON ph.contact_id = c.id
    ORDER BY {order};
""")
for row in cur.fetchall():
    print(row)

# 4. pagination with next/prev/quit
limit = 3
offset = 0

while True:
    cur.execute("SELECT * FROM paginatio(%s, %s);", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cmd = input("next / prev / quit: ")
    if cmd == "next":
        offset += limit
    elif cmd == "prev":
        if offset >= limit:
            offset -= limit
    elif cmd == "quit":
        break

cur.close()
conn.close()
import psycopg2

conn = psycopg2.connect(
    host="localhost", dbname="phoneboo2",
    user="postgres", password="1234"
)
cur = conn.cursor()

# #1 поиск по паттерну
print("--- Search ---")
pattern = input("search pattern: ")
cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
for row in cur.fetchall():
    print(f"Name: {row[0]} {row[1]}, Phone: {row[2]}, Email: {row[3]}")

# #2 добавить или обновить контакт
print("\n--- Add / Update contact ---")
name     = input("name: ")
surname  = input("surname: ")
phone    = input("phone: ")
ptype    = input("phone type (home/work/mobile): ")
email    = input("email: ")
birthday = input("birthday (YYYY-MM-DD): ")
group_id = input("group (1=Family 2=Work 3=Friend 4=Other): ")
cur.execute(
    "CALL add_or_update_user(%s,%s,%s,%s,%s,%s,%s);",
    (name, surname, phone, ptype, email, birthday, group_id)
)
conn.commit()
print("Saved.")

# #3 пагинация
print("\n--- Pagination ---")
limit  = input("limit: ")
offset = input("offset: ")
cur.execute("SELECT * FROM paginatio(%s,%s);", (limit, offset))
for row in cur.fetchall():
    print(f"Name: {row[0]} {row[1]}, Phone: {row[2]} ({row[3]})")

# #4 удалить через функцию
print("\n--- Delete ---")
dname  = input("name to delete: ")
dphone = input("phone to delete: ")
cur.execute("SELECT deket(%s,%s);", (dname, dphone))
conn.commit()
print("Deleted.")

# #5 bulk insert
print("\n--- Bulk insert ---")
data = [
    ["Amir",  "Seitkali", "87001112233", "mobile"],
    ["Dana",  "Bekova",   "87002223344", "work"],
    ["",      "Noname",   "87003334455", "home"],    # пропустится
    ["Amir",  "Seitkali", "87001112233", "mobile"],  # пропустится дубликат
]
cur.execute("CALL bulk_insert(%s);", (data,))
conn.commit()
print("Bulk insert done.")

# #6 удалить через процедуру
print("\n--- Delete via procedure ---")
dname  = input("name to delete: ")
dphone = input("phone to delete: ")
cur.execute("CALL delete_contact(%s,%s);", (dname, dphone))
conn.commit()
print("Deleted.")

cur.close()
conn.close()
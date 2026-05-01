import psycopg2
import json
import csv

conn = psycopg2.connect(
    host="localhost", dbname="phoneboo2",
    user="postgres", password="1234"
)
cur = conn.cursor()

# 1. export to json
def export_json():
    cur.execute("""
        SELECT c.name, c.surname, c.email, c.birthday, g.name as group_name,
               ph.phone, ph.type
        FROM phonebook c
        LEFT JOIN phones ph ON ph.contact_id = c.id
        LEFT JOIN groups g ON g.id = c.group_id
    """)
    rows = cur.fetchall()

    contacts = []
    for row in rows:
        contacts.append({
            "name":     row[0],
            "surname":  row[1],
            "email":    row[2],
            "birthday": str(row[3]) if row[3] else None,
            "group":    row[4],
            "phone":    row[5],
            "type":     row[6]
        })

    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=4)
    print("Exported to contacts.json")

# 2. import from json
def import_json():
    with open("contacts.json", "r") as f:
        contacts = json.load(f)

    for c in contacts:
        # check if contact already exists
        cur.execute(
            "SELECT id FROM phonebook WHERE name=%s AND surname=%s;",
            (c["name"], c["surname"])
        )
        existing = cur.fetchone()

        if existing:
            answer = input(f"{c['name']} {c['surname']} already exists. skip or overwrite? ")
            if answer == "skip":
                continue
            elif answer == "overwrite":
                cur.execute(
                    "UPDATE phonebook SET email=%s, birthday=%s WHERE id=%s;",
                    (c["email"], c["birthday"], existing[0])
                )
                conn.commit()
        else:
            # get group id
            cur.execute("SELECT id FROM groups WHERE name=%s;", (c["group"],))
            group = cur.fetchone()
            group_id = group[0] if group else None

            cur.execute(
                "INSERT INTO phonebook(name, surname, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) RETURNING id;",
                (c["name"], c["surname"], c["email"], c["birthday"], group_id)
            )
            contact_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s);",
                (contact_id, c["phone"], c["type"])
            )
            conn.commit()
        print(f"Imported: {c['name']} {c['surname']}")

# 3. import from csv
# csv format: name, surname, phone, type, email, birthday, group
def import_csv():
    with open("contacts.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            name     = row[0]
            surname  = row[1]
            phone    = row[2]
            ptype    = row[3]
            email    = row[4]
            birthday = row[5]
            group    = row[6]

            # get group id
            cur.execute("SELECT id FROM groups WHERE name=%s;", (group,))
            g = cur.fetchone()
            group_id = g[0] if g else None

            # check duplicate
            cur.execute(
                "SELECT id FROM phonebook WHERE name=%s AND surname=%s;",
                (name, surname)
            )
            existing = cur.fetchone()

            if existing:
                answer = input(f"{name} {surname} already exists. skip or overwrite? ")
                if answer == "skip":
                    continue
                elif answer == "overwrite":
                    cur.execute(
                        "UPDATE phonebook SET email=%s, birthday=%s, group_id=%s WHERE id=%s;",
                        (email, birthday, group_id, existing[0])
                    )
                    conn.commit()
            else:
                cur.execute(
                    "INSERT INTO phonebook(name, surname, email, birthday, group_id) VALUES (%s,%s,%s,%s,%s) RETURNING id;",
                    (name, surname, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO phones(contact_id, phone, type) VALUES (%s,%s,%s);",
                    (contact_id, phone, ptype)
                )
                conn.commit()
            print(f"Imported: {name} {surname}")

export_json()
import_json()
import_csv()

cur.close()
conn.close()
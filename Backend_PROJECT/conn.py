import psycopg2

# connect to the postgresql database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="GlobMec_database",
    user="GlobMec",
    password="global44",
    )

cur = conn.cursor()

cur.execute("SELECT * FROM User")
User = cur.fetchall()
cur.execute("SELECT * FROM Address")
Address = cur.fetchall()

for rows in User:
    print(rows)

for row in Address:
    print(row)



cur.close()
conn.close()

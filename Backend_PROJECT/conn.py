import psycopg2
from models import User, Address

# connect to the postgresql database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="GlobMec_database",
    user="GlobMec",
    password="global44",
    )
    
cur = conn.cursor()
cur.execute(User)
cur.execute(Address)

cur.close()
conn.close()

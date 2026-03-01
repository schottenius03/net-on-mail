from pyexpat.errors import messages
from my_server.dbhandler import create_connection

conn = create_connection()
cur = conn.cursor()

sql = '''CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    nr_login INTEGER NOT NULL
)'''

cur.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY,
    sender INTEGER NOT NULL,
    receiver INTEGER NOT NULL,
    heading TEXT NOT NULL,
    context TEXT NOT NULL,
    status TEXT NOT NULL
)'''

cur.execute(sql)
conn.close()
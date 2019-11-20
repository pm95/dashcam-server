import sqlite3

db_path = "./db/dashcam.db"

conn = sqlite3.connect(db_path)
c = conn.cursor()

for row in c.execute("SELECT * FROM USERS"):
    print(row)

c.close()

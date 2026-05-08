import sqlite3

conn = sqlite3.connect("placements.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(placements)")
cols = cur.fetchall()

print("TABLE COLUMNS:\n")
for c in cols:
    print(c)

conn.close()

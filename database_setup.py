import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

with open("inventory.sql", "r") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()
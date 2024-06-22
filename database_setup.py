# database_setup.py
import sqlite3

def setup_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    with open('inventory.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
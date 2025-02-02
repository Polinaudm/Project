import sqlite3

conn = sqlite3.connect('Leaders.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS leaders_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nick TEXT NOT NULL,
    level_1 REAL DEFAULT 0.0,
    level_2 REAL DEFAULT 0.0,
    level_3 REAL DEFAULT 0.0)''')

conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("shop.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balance REAL DEFAULT 0,
    discount INTEGER DEFAULT 0,
    lang TEXT,
    purchase_count INTEGER DEFAULT 0
)''')
c.execute('''CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item TEXT,
    amount REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
c.execute('''CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    qty INTEGER,
    city TEXT,
    district TEXT
)''')

conn.commit()
conn.close()
print("DB initialized")

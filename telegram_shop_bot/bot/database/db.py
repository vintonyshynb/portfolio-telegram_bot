import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "shop.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
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

        c.execute('''CREATE TABLE IF NOT EXISTS payment_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            telegram_payment_charge_id TEXT UNIQUE,
            provider_payment_charge_id TEXT,
            amount INTEGER,
            currency TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )''')

        conn.commit()
    print("DB initialized")


def get_user(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "balance": row[2],
                "discount": row[3],
                "lang": row[4],
                "purchase_count": row[5]
            }
        return None


def create_user(user_id, username, lang):
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (user_id, username, lang, balance) VALUES (?, ?, ?, ?)",
            (user_id, username, lang, 0.0)
        )
        conn.commit()


def update_user_lang(user_id, lang):
    with get_connection() as conn:
        conn.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
        conn.commit()


def get_purchases(limit=10):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, item, amount, date FROM purchases ORDER BY date DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        return [{"id": r[0], "user_id": r[1], "item": r[2], "amount": r[3], "date": r[4]} for r in rows]


def get_items():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM items")
        rows = cur.fetchall()
        return [{"id": r[0], "name": r[1]} for r in rows]


def update_user_balance(user_id, amount):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        if not row:
            return False
        new_balance = row[0] + amount
        cur.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
        conn.commit()
        return True


def add_item(name, price, qty, city, district):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO items (name, price, qty, city, district) VALUES (?, ?, ?, ?, ?)",
            (name, price, qty, city, district)
        )
        conn.commit()


def delete_item(item_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        conn.commit()


def get_all_items():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, price, qty, city, district FROM items WHERE qty > 0")
        rows = cur.fetchall()
        return [{"id": r[0], "name": r[1], "price": r[2], "qty": r[3], "city": r[4], "district": r[5]} for r in rows]


def get_item_by_id(item_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, price, qty, city, district FROM items WHERE id=?", (item_id,))
        row = cur.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "price": row[2], "qty": row[3], "city": row[4], "district": row[5]}
        return None


def purchase_item(user_id, item_id, quantity=1):
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        user_row = cur.fetchone()
        if not user_row:
            return {"success": False, "error": "user_not_found"}

        user_balance = user_row[0]

        cur.execute("SELECT id, name, price, qty FROM items WHERE id=?", (item_id,))
        item_row = cur.fetchone()
        if not item_row:
            return {"success": False, "error": "item_not_found"}

        item_id, item_name, item_price, item_qty = item_row

        if item_qty < quantity:
            return {"success": False, "error": "insufficient_quantity"}

        total_cost = item_price * quantity

        if user_balance < total_cost:
            return {"success": False, "error": "insufficient_balance"}

        try:
            new_balance = user_balance - total_cost
            cur.execute("UPDATE users SET balance=?, purchase_count=purchase_count+? WHERE user_id=?",
                        (new_balance, quantity, user_id))

            new_qty = item_qty - quantity
            cur.execute("UPDATE items SET qty=? WHERE id=?", (new_qty, item_id))

            cur.execute("INSERT INTO purchases (user_id, item, amount) VALUES (?, ?, ?)",
                        (user_id, f"{item_name} x{quantity}", total_cost))

            conn.commit()
            return {"success": True, "item_name": item_name, "quantity": quantity, "total_cost": total_cost,
                    "new_balance": new_balance}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": "transaction_failed"}


def create_payment_transaction(user_id, amount, currency, telegram_charge_id, provider_charge_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO payment_transactions 
            (user_id, telegram_payment_charge_id, provider_payment_charge_id, amount, currency) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, telegram_charge_id, provider_charge_id, amount, currency))
        conn.commit()
        return cur.lastrowid


def complete_payment_transaction(telegram_charge_id, user_id):
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
            SELECT amount, status FROM payment_transactions 
            WHERE telegram_payment_charge_id=? AND user_id=?
        """, (telegram_charge_id, user_id))
        transaction = cur.fetchone()

        if not transaction:
            return {"success": False, "error": "transaction_not_found"}

        amount, status = transaction

        if status == 'completed':
            return {"success": False, "error": "already_completed"}

        try:
            cur.execute("""
                UPDATE payment_transactions 
                SET status='completed', completed_at=CURRENT_TIMESTAMP 
                WHERE telegram_payment_charge_id=? AND user_id=?
            """, (telegram_charge_id, user_id))

            amount_in_currency = amount / 100.0
            cur.execute("""
                UPDATE users SET balance = balance + ? WHERE user_id=?
            """, (amount_in_currency, user_id))

            cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            new_balance = cur.fetchone()[0]

            conn.commit()
            return {"success": True, "amount_added": amount_in_currency, "new_balance": new_balance}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": "transaction_failed"}


def get_payment_transactions(user_id=None, limit=50):
    with get_connection() as conn:
        cur = conn.cursor()
        if user_id:
            cur.execute("""
                SELECT id, user_id, amount, currency, status, created_at, completed_at 
                FROM payment_transactions 
                WHERE user_id=? 
                ORDER BY created_at DESC LIMIT ?
            """, (user_id, limit))
        else:
            cur.execute("""
                SELECT id, user_id, amount, currency, status, created_at, completed_at 
                FROM payment_transactions 
                ORDER BY created_at DESC LIMIT ?
            """, (limit,))

        rows = cur.fetchall()
        return [{
            "id": r[0], "user_id": r[1], "amount": r[2], "currency": r[3],
            "status": r[4], "created_at": r[5], "completed_at": r[6]
        } for r in rows]

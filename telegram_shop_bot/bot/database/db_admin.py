import sqlite3


def add_item(name, price, qty, city, district):
    with sqlite3.connect("shop.db") as conn:
        conn.execute("INSERT INTO items (name, price, qty, city, district) VALUES (?, ?, ?, ?, ?)",
                     (name, price, qty, city, district))


def delete_item(item_id):
    with sqlite3.connect("shop.db") as conn:
        conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        conn.commit()

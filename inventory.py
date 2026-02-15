from database import conn, cursor

def add_part(name, qty, price):
    cursor.execute(
        "INSERT INTO parts (part_name, stock_qty, unit_price) VALUES (?, ?, ?)",
        (name, qty, price)
    )
    conn.commit()

def get_parts():
    cursor.execute("SELECT * FROM parts")
    return cursor.fetchall()

def get_parts():
    cursor.execute("SELECT * FROM parts")
    return cursor.fetchall()

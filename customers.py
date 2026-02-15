from database import cursor, conn

def add_customer(name, phone):
    cursor.execute(
        "INSERT INTO customers (name, phone) VALUES (?, ?)",
        (name, phone)
    )
    conn.commit()

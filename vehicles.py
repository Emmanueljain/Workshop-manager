from database import cursor, conn

def get_customers():
    cursor.execute("SELECT customer_id, name FROM customers")
    return cursor.fetchall()

def add_vehicle(customer_id, plate_no, make, model):
    cursor.execute(
        "INSERT INTO vehicles (customer_id, plate_no, make, model) VALUES (?, ?, ?, ?)",
        (customer_id, plate_no, make, model)
    )
    conn.commit()

def get_vehicles():
    cursor.execute("""
        SELECT v.vehicle_id, v.plate_no, c.name
        FROM vehicles v
        JOIN customers c ON v.customer_id = c.customer_id
    """)
    return cursor.fetchall()

import sqlite3
import os
import sys

# Determine the path to the directory where the .exe is located
if getattr(sys, 'frozen', False):
    # If running as compiled .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # If running as .py script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Combine directory with filename
DB_PATH = os.path.join(BASE_DIR, "workshop.db")

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            plate_no TEXT,
            make TEXT,
            model TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            labor_cost REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parts (
            part_id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_name TEXT,
            stock_qty INTEGER,
            unit_price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            total_amount REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            part_id INTEGER,
            quantity INTEGER,
            amount REAL
        )
    """)

    conn.commit()

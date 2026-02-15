from database import cursor, conn
# We import calculate_job_total inside the function to avoid circular import issues
import invoices 

def add_part_to_job(job_id, part_id, quantity):
    # 1. Check current stock and get price
    cursor.execute("SELECT stock_qty, unit_price FROM parts WHERE part_id = ?", (part_id,))
    result = cursor.fetchone()
    
    if not result:
        raise ValueError("Part not found")

    current_stock = result["stock_qty"]
    unit_price = result["unit_price"]

    # 2. Validation: Do we have enough?
    if current_stock < quantity:
        raise ValueError(f"Not enough stock! Only {current_stock} left.")

    # 3. Calculate Amount
    amount = unit_price * quantity

    # 4. Add to Job
    cursor.execute("""
        INSERT INTO job_parts (job_id, part_id, quantity, amount)
        VALUES (?, ?, ?, ?)
    """, (job_id, part_id, quantity, amount))

    # 5. DEDUCT FROM INVENTORY
    cursor.execute("""
        UPDATE parts 
        SET stock_qty = stock_qty - ? 
        WHERE part_id = ?
    """, (quantity, part_id))

    conn.commit()

    # 6. AUTO-SYNC: Update Invoice Total if it exists
    cursor.execute("SELECT invoice_id FROM invoices WHERE job_id = ?", (job_id,))
    if cursor.fetchone():
        # Recalculate the new total
        new_total = invoices.calculate_job_total(job_id)
        
        # Update the invoices table
        cursor.execute("UPDATE invoices SET total_amount = ? WHERE job_id = ?", (new_total, job_id))
        conn.commit()
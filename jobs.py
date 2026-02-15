from database import cursor, conn

def create_job(vehicle_id, labor_cost):
    cursor.execute(
        "INSERT INTO jobs (vehicle_id, labor_cost) VALUES (?, ?)",
        (vehicle_id, labor_cost)
    )
    conn.commit()

def get_job_total(job_id):
    """Calculates Total = Labor + Parts. Used for internal sync."""
    # Get labor cost
    cursor.execute(
        "SELECT labor_cost FROM jobs WHERE job_id = ?",
        (job_id,)
    )
    labor_row = cursor.fetchone()
    labor = labor_row["labor_cost"] if labor_row else 0.0

    # Get parts total
    cursor.execute(
        "SELECT SUM(amount) AS total FROM job_parts WHERE job_id = ?",
        (job_id,)
    )
    result = cursor.fetchone()
    parts_total = result["total"] if result["total"] else 0.0

    return labor + parts_total

def get_all_jobs():
    """Fetches all jobs with their ID, vehicle plate, and customer name for dropdowns."""
    cursor.execute("""
        SELECT jobs.job_id, vehicles.plate_no, customers.name 
        FROM jobs
        JOIN vehicles ON jobs.vehicle_id = vehicles.vehicle_id
        JOIN customers ON vehicles.customer_id = customers.customer_id
    """)
    return cursor.fetchall()

def update_labor_cost(job_id, new_labor_cost):
    """Updates the labor cost AND automatically updates the invoice total."""
    
    # 1. Update the Labor Cost in jobs table
    cursor.execute(
        "UPDATE jobs SET labor_cost = ? WHERE job_id = ?", 
        (new_labor_cost, job_id)
    )
    conn.commit()

    # 2. Auto-Sync: Check if an invoice exists and update it
    cursor.execute("SELECT invoice_id FROM invoices WHERE job_id = ?", (job_id,))
    if cursor.fetchone():
        # Recalculate the new total using the function above
        new_total = get_job_total(job_id)
        
        # Update the invoices table with the new total
        cursor.execute("UPDATE invoices SET total_amount = ? WHERE job_id = ?", (new_total, job_id))
        conn.commit()
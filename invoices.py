import sqlite3
from database import conn, cursor

def calculate_job_total(job_id):
    """Calculates Total = Labor Cost + Sum of Spare Parts assigned to the job."""
    
    # 1. Get Labor Cost
    cursor.execute("SELECT labor_cost FROM jobs WHERE job_id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        return 0.0
    labor_cost = job["labor_cost"]

    # 2. Get Total Parts Cost
    cursor.execute("SELECT SUM(amount) as parts_total FROM job_parts WHERE job_id = ?", (job_id,))
    result = cursor.fetchone()
    parts_total = result["parts_total"] if result["parts_total"] else 0.0

    return labor_cost + parts_total

def create_invoice(job_id):
    """Calculates total, creates invoice if new, or updates it if exists."""
    
    total_amount = calculate_job_total(job_id)

    # Check if invoice already exists for this job
    cursor.execute("SELECT invoice_id FROM invoices WHERE job_id = ?", (job_id,))
    existing = cursor.fetchone()
    
    try:
        if existing:
            # UPDATE existing invoice (Sync)
            cursor.execute("UPDATE invoices SET total_amount = ? WHERE job_id = ?", 
                           (total_amount, job_id))
            conn.commit()
            return f"Invoice updated! New Total: ${total_amount:.2f}"
        else:
            # CREATE new invoice
            cursor.execute("INSERT INTO invoices (job_id, total_amount) VALUES (?, ?)", 
                           (job_id, total_amount))
            conn.commit()
            return f"Invoice created successfully! Total: ${total_amount:.2f}"
            
    except Exception as e:
        return f"Error: {e}"

def get_all_invoices():
    """Fetches invoices with Customer Name and Plate Number for display."""
    query = """
    SELECT 
        invoices.invoice_id,
        invoices.job_id,
        customers.name as customer_name,
        vehicles.plate_no,
        invoices.total_amount
    FROM invoices
    JOIN jobs ON invoices.job_id = jobs.job_id
    JOIN vehicles ON jobs.vehicle_id = vehicles.vehicle_id
    JOIN customers ON vehicles.customer_id = customers.customer_id
    ORDER BY invoices.invoice_id DESC
    """
    cursor.execute(query)
    return cursor.fetchall()

def get_invoice_details(invoice_id):
    """
    Fetches the breakdown (Labor + Parts) for a specific invoice.
    Returns a dictionary with labor cost and a list of parts.
    """
    # 1. Get Job ID and Labor Cost
    query_job = """
    SELECT jobs.job_id, jobs.labor_cost 
    FROM invoices 
    JOIN jobs ON invoices.job_id = jobs.job_id 
    WHERE invoices.invoice_id = ?
    """
    cursor.execute(query_job, (invoice_id,))
    job_data = cursor.fetchone()
    
    if not job_data:
        return None

    job_id = job_data["job_id"]
    labor_cost = job_data["labor_cost"]

    # 2. Get Parts Details
    query_parts = """
    SELECT parts.part_name, job_parts.quantity, job_parts.amount 
    FROM job_parts 
    JOIN parts ON job_parts.part_id = parts.part_id 
    WHERE job_parts.job_id = ?
    """
    cursor.execute(query_parts, (job_id,))
    parts_data = cursor.fetchall()

    return {
        "job_id": job_id,
        "labor_cost": labor_cost,
        "parts": parts_data
    }
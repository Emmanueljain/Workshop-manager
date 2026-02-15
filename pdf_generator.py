from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database import cursor
import os
import sys
import datetime

# --- NEW: PyInstaller hidden folder logic ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# (We still need this for the INVOICES folder so it saves next to the .exe)
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# --------------------------------------------

def generate_invoice_pdf(invoice_id):
    # 1. Fetch Full Invoice Data
    query = """
    SELECT 
        invoices.invoice_id, invoices.total_amount,
        customers.name, customers.phone,
        vehicles.plate_no, vehicles.make, vehicles.model,
        jobs.labor_cost, jobs.job_id
    FROM invoices
    JOIN jobs ON invoices.job_id = jobs.job_id
    JOIN vehicles ON jobs.vehicle_id = vehicles.vehicle_id
    JOIN customers ON vehicles.customer_id = customers.customer_id
    WHERE invoices.invoice_id = ?
    """
    cursor.execute(query, (invoice_id,))
    invoice = cursor.fetchone()
    
    if not invoice:
        return "Invoice not found"

    # 2. Fetch Parts for this Job
    cursor.execute("""
        SELECT parts.part_name, job_parts.quantity, job_parts.amount, parts.unit_price
        FROM job_parts
        JOIN parts ON job_parts.part_id = parts.part_id
        WHERE job_parts.job_id = ?
    """, (invoice['job_id'],))
    parts = cursor.fetchall()

    # 3. Create INVOICES Folder (Saves next to the actual .exe)
    folder_name = os.path.join(BASE_DIR, "INVOICES")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 4. Define File Path
    safe_name = invoice['name'].replace(" ", "_")
    filename = f"Invoice_{invoice_id}_{safe_name}.pdf"
    full_path = os.path.join(folder_name, filename)

    # 5. Generate PDF
    c = canvas.Canvas(full_path, pagesize=letter)
    width, height = letter

    # --- Header with Logo ---
    # NEW: Use the resource_path function to find the baked-in logo
    logo_path = resource_path("logo.png")
    
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 50, height - 90, width=70, height=70, preserveAspectRatio=True, mask='auto')
        text_x = 135  # Shifted right
    else:
        text_x = 50   # Default left position if no logo

    c.setFont("Helvetica-Bold", 20)
    c.drawString(text_x, height - 50, "Gulf Creativity") 

    c.setFont("Helvetica", 10)
    c.drawString(text_x, height - 70, "Mahboula Block No:1,Street No:125,Building No:46") 
    c.drawString(text_x, height - 85, "Phone: 965 65791777") 
    
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(width - 50, height - 50, "INVOICE")
    
    c.setFont("Helvetica", 12)
    c.drawRightString(width - 50, height - 70, f"#{invoice['invoice_id']}")
    c.drawRightString(width - 50, height - 85, datetime.date.today().strftime("%Y-%m-%d"))

    # --- Customer & Vehicle Details ---
    y = height - 130
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Bill To:")
    c.drawString(300, y, "Vehicle Details:")

    c.setFont("Helvetica", 12)
    y -= 20
    c.drawString(50, y, f"Customer: {invoice['name']}")
    c.drawString(300, y, f"Car: {invoice['make']} {invoice['model']}")
    
    y -= 20
    c.drawString(50, y, f"Phone: {invoice['phone']}")
    c.drawString(300, y, f"Plate: {invoice['plate_no']}")

    # --- Table Header ---
    y -= 50
    c.setLineWidth(1)
    c.line(50, y, width - 50, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Description")
    c.drawString(350, y, "Qty")
    c.drawString(420, y, "Unit Price")
    c.drawRightString(width - 50, y, "Amount")
    y -= 10
    c.line(50, y, width - 50, y)

    # --- Table Content ---
    y -= 20
    c.setFont("Helvetica", 12)
    
    # Labor
    c.drawString(50, y, "Labor Charges")
    c.drawString(350, y, "1")
    c.drawString(420, y, f"{invoice['labor_cost']:.2f}")
    c.drawRightString(width - 50, y, f"{invoice['labor_cost']:.2f}")
    y -= 20

    # Parts
    for part in parts:
        c.drawString(50, y, part['part_name'])
        c.drawString(350, y, str(part['quantity']))
        c.drawString(420, y, f"{part['unit_price']:.2f}")
        c.drawRightString(width - 50, y, f"{part['amount']:.2f}")
        y -= 20

    # --- Total ---
    y -= 20
    c.line(50, y, width - 50, y)
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(350, y, "TOTAL:")
    
    c.drawRightString(width - 50, y, f"KWD {invoice['total_amount']:.2f}")

    # --- Footer ---
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, 50, "Thank you! Please drive safely.")

    c.save()
    
    return f"PDF Saved: {full_path}"

import invoices
from tkinter import *
from tkinter import ttk, messagebox
import os  # Needed for opening the PDF automatically
from customers import add_customer
from vehicles import get_customers, add_vehicle, get_vehicles
from jobs import create_job, get_all_jobs, update_labor_cost
from inventory import add_part, get_parts
from job_parts import add_part_to_job
from pdf_generator import generate_invoice_pdf  # Import the PDF function

# ---------------- ADD CUSTOMER WINDOW ----------------
def open_add_customer():
    win = Toplevel()
    win.title("Add Customer")
    win.geometry("300x250")

    Label(win, text="Customer Name").pack(pady=5)
    name_entry = Entry(win, width=30)
    name_entry.pack()

    Label(win, text="Phone Number").pack(pady=5)
    phone_entry = Entry(win, width=30)
    phone_entry.pack()

    message = Label(win, text="")
    message.pack(pady=5)

    def save_customer():
        if name_entry.get() == "" or phone_entry.get() == "":
            message.config(text="All fields required", fg="red")
            return

        add_customer(name_entry.get(), phone_entry.get())
        message.config(text="Customer saved!", fg="green")

        name_entry.delete(0, END)
        phone_entry.delete(0, END)

    Button(win, text="Save Customer", command=save_customer).pack(pady=15)


# ---------------- ADD VEHICLE WINDOW ----------------
def open_add_vehicle():
    win = Toplevel()
    win.title("Add Vehicle")
    win.geometry("350x350")

    Label(win, text="Select Customer").pack(pady=5)

    customers = get_customers()
    customer_map = {
        f"{c['name']} (ID {c['customer_id']})": c['customer_id']
        for c in customers
    }

    customer_var = StringVar()
    if customer_map:
        customer_var.set(next(iter(customer_map)))

    OptionMenu(win, customer_var, *customer_map.keys()).pack()

    Label(win, text="Plate Number").pack(pady=5)
    plate_entry = Entry(win, width=30)
    plate_entry.pack()

    Label(win, text="Make").pack(pady=5)
    make_entry = Entry(win, width=30)
    make_entry.pack()

    Label(win, text="Model").pack(pady=5)
    model_entry = Entry(win, width=30)
    model_entry.pack()

    message = Label(win, text="")
    message.pack(pady=5)

    def save_vehicle():
        if customer_var.get() == "":
            message.config(text="Select a customer", fg="red")
            return

        add_vehicle(
            customer_map[customer_var.get()],
            plate_entry.get(),
            make_entry.get(),
            model_entry.get()
        )

        message.config(text="Vehicle saved!", fg="green")

        plate_entry.delete(0, END)
        make_entry.delete(0, END)
        model_entry.delete(0, END)

    Button(win, text="Save Vehicle", command=save_vehicle).pack(pady=15)


# ---------------- JOB CARD WINDOW ----------------
def open_job_card():
    win = Toplevel()
    win.title("Create Job Card")
    win.geometry("350x300")

    Label(win, text="Select Vehicle").pack(pady=5)

    vehicles = get_vehicles()
    vehicle_map = {
        f"{v['plate_no']} - {v['name']} (ID {v['vehicle_id']})": v['vehicle_id']
        for v in vehicles
    }

    vehicle_var = StringVar()
    if vehicle_map:
        vehicle_var.set(next(iter(vehicle_map)))

    OptionMenu(win, vehicle_var, *vehicle_map.keys()).pack()

    Label(win, text="Labor Cost").pack(pady=5)
    labor_entry = Entry(win, width=30)
    labor_entry.pack()

    message = Label(win, text="")
    message.pack(pady=5)

    def save_job():
        try:
            create_job(
                vehicle_map[vehicle_var.get()],
                float(labor_entry.get())
            )
            message.config(text="Job card created!", fg="green")
            labor_entry.delete(0, END)
        except:
            message.config(text="Invalid labor cost", fg="red")

    Button(win, text="Create Job", command=save_job).pack(pady=15)


# ---------------- INVENTORY WINDOW ----------------
def open_inventory():
    win = Toplevel()
    win.title("Inventory")
    win.geometry("350x300")

    Label(win, text="Inventory Module", font=("Arial", 14)).pack(pady=10)

    Label(win, text="Part Name").pack()
    part_entry = Entry(win, width=30)
    part_entry.pack()

    Label(win, text="Quantity").pack()
    qty_entry = Entry(win, width=30)
    qty_entry.pack()

    Label(win, text="Unit Price").pack()
    price_entry = Entry(win, width=30)
    price_entry.pack()

    message = Label(win, text="")
    message.pack(pady=5)

    def save_part():
        try:
            add_part(
                part_entry.get(),
                int(qty_entry.get()),
                float(price_entry.get())
            )
            message.config(text="Part added successfully!", fg="green")
            part_entry.delete(0, END)
            qty_entry.delete(0, END)
            price_entry.delete(0, END)
        except:
            message.config(text="Invalid input", fg="red")

    Button(win, text="Add Part", command=save_part).pack(pady=15)


# ---------------- INVOICE MANAGER WINDOW ----------------
def open_invoices():
    win = Toplevel()
    win.title("Invoice Management")
    win.geometry("700x550") # Larger size for list view and buttons

    Label(win, text="Invoice Management", font=("Arial", 16, "bold")).pack(pady=10)

    # --- Top Section: Generate New Invoice (UPDATED TO DROPDOWN) ---
    frame_gen = Frame(win, bd=2, relief=GROOVE)
    frame_gen.pack(fill=X, padx=10, pady=5)
    
    Label(frame_gen, text="Generate Invoice for Job:").pack(side=LEFT, padx=5, pady=10)

    # Fetch jobs to populate the dropdown
    jobs = get_all_jobs()
    job_var = StringVar()
    job_map = {}

    if not jobs:
        # If there are no jobs at all, show a disabled dropdown
        job_map = {"No jobs available": None}
        job_var.set("No jobs available")
        dropdown = OptionMenu(frame_gen, job_var, *job_map.keys())
        dropdown.config(state=DISABLED)
        dropdown.pack(side=LEFT, padx=5)
    else:
        # Map the readable string to the actual job_id
        job_map = {
            f"Job #{j['job_id']} - {j['plate_no']} ({j['name']})": j['job_id']
            for j in jobs
        }
        job_var.set(next(iter(job_map))) # Set default selection
        OptionMenu(frame_gen, job_var, *job_map.keys()).pack(side=LEFT, padx=5)

    def generate_handler():
        if not jobs or job_map.get(job_var.get()) is None:
            messagebox.showwarning("Error", "No valid job selected.")
            return
            
        # Get the actual integer Job ID from our dictionary map
        job_id = job_map[job_var.get()]
        
        # Call the logic from invoices.py
        msg = invoices.create_invoice(job_id)
        if "Error" in msg:
            messagebox.showerror("Failed", msg)
        else:
            messagebox.showinfo("Success", msg)
            refresh_list() # Update list immediately

    Button(frame_gen, text="Calculate & Generate", command=generate_handler, bg="#4CAF50", fg="white").pack(side=LEFT, padx=10)

    # --- Middle Section: Invoice List ---
    Label(win, text="Existing Invoices:", font=("Arial", 10, "bold")).pack(pady=(10, 0))

    columns = ("Inv ID", "Job ID", "Customer", "Plate No", "Total")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    
    tree.heading("Inv ID", text="Inv ID")
    tree.heading("Job ID", text="Job ID")
    tree.heading("Customer", text="Customer")
    tree.heading("Plate No", text="Plate No")
    tree.heading("Total", text="Total Amount")

    tree.column("Inv ID", width=50, anchor=CENTER)
    tree.column("Job ID", width=50, anchor=CENTER)
    tree.column("Customer", width=200)
    tree.column("Plate No", width=100)
    tree.column("Total", width=100, anchor=E)

    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # --- Bottom Section: Actions Frame ---
    frame_actions = Frame(win)
    frame_actions.pack(pady=5)

    # 1. VIEW DETAILS FUNCTION
    def view_details():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an invoice to view details.")
            return

        # Get Invoice ID from the selected row
        item_data = tree.item(selected_item)
        invoice_id = item_data['values'][0]

        # Fetch Data
        details = invoices.get_invoice_details(invoice_id)
        
        if not details:
            messagebox.showerror("Error", "Could not fetch details. Ensure invoices.py is updated.")
            return

        # --- Show Popup ---
        detail_win = Toplevel()
        detail_win.title(f"Invoice #{invoice_id} Details")
        detail_win.geometry("400x400")

        Label(detail_win, text=f"Invoice #{invoice_id} Breakdown", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Labor Section
        frame_labor = Frame(detail_win, bd=1, relief=SOLID, padx=10, pady=5)
        frame_labor.pack(fill=X, padx=20, pady=5)
        Label(frame_labor, text=f"Job ID: {details['job_id']}", font=("Arial", 10, "bold")).pack(anchor=W)
        Label(frame_labor, text=f"Labor Cost: KWD{details['labor_cost']:.2f}", fg="blue").pack(anchor=W)

        # Parts Section
        Label(detail_win, text="Spare Parts Used:", font=("Arial", 10, "bold")).pack(pady=(10,5))
        
        parts_frame = Frame(detail_win)
        parts_frame.pack(fill=BOTH, expand=True, padx=20)
        
        if not details['parts']:
            Label(parts_frame, text="No parts used for this job.", fg="gray").pack()
        else:
            Label(parts_frame, text=f"{'Part Name':<20} {'Qty':<5} {'Cost'}", font=("Courier", 10, "bold")).pack(anchor=W)
            Label(parts_frame, text="-"*40).pack(anchor=W)
            for part in details['parts']:
                row_text = f"{part['part_name']:<20} {part['quantity']:<5} KWD{part['amount']:.2f}"
                Label(parts_frame, text=row_text, font=("Courier", 10)).pack(anchor=W)

        Button(detail_win, text="Close", command=detail_win.destroy).pack(pady=10)

    # 2. EXPORT PDF FUNCTION
    def export_pdf():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an invoice to export.")
            return

        item_data = tree.item(selected_item)
        invoice_id = item_data['values'][0]

        try:
            msg = generate_invoice_pdf(invoice_id)
            messagebox.showinfo("PDF Export", msg)
            
            # Try to open the PDF automatically
            try:
                os.startfile(msg.replace("PDF Saved: ", "")) 
            except:
                pass 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {e}")

    # Add Buttons to Actions Frame
    Button(frame_actions, text="View Details", command=view_details, bg="#2196F3", fg="white", width=15).pack(side=LEFT, padx=10)
    Button(frame_actions, text="Export PDF", command=export_pdf, bg="#FF5722", fg="white", width=15).pack(side=LEFT, padx=10)


    def refresh_list():
        # Clear list
        for item in tree.get_children():
            tree.delete(item)
        
        # Fetch data
        rows = invoices.get_all_invoices()
        for row in rows:
            tree.insert("", END, values=(
                row["invoice_id"],
                row["job_id"],
                row["customer_name"],
                row["plate_no"],
                f"KWD {row['total_amount']:.2f}"
            ))

    # Load data when window opens
    refresh_list()

    # Close Button
    Button(win, text="Close", command=win.destroy).pack(pady=10)


# ---------------- ADD PARTS TO JOB WINDOW ----------------
def open_add_part_to_job():
    # 1. ERROR CHECK: Ensure jobs exist before opening
    jobs = get_all_jobs()
    if not jobs:
        messagebox.showerror("Error", "No active jobs found! Please create a Job Card first.")
        return

    win = Toplevel()
    win.title("Add Parts to Job")
    win.geometry("350x350")

    # 2. JOB DROPDOWN
    Label(win, text="Select Job").pack(pady=5)
    
    # Create a dictionary mapping "Job #1 - Plate (Name)" to the actual job_id
    job_map = {
        f"Job #{j['job_id']} - {j['plate_no']} ({j['name']})": j['job_id']
        for j in jobs
    }
    
    job_var = StringVar()
    job_var.set(next(iter(job_map))) # Set default value
    OptionMenu(win, job_var, *job_map.keys()).pack()

    # 3. PART DROPDOWN
    Label(win, text="Select Part").pack(pady=5)
    parts = get_parts()
    if not parts:
        messagebox.showerror("Error", "Inventory is empty! Add parts first.")
        win.destroy()
        return

    part_map = {
        f"{p['part_name']} (Stock {p['stock_qty']})": p['part_id']
        for p in parts
    }
    part_var = StringVar()
    part_var.set(next(iter(part_map)))
    OptionMenu(win, part_var, *part_map.keys()).pack()

    # 4. QUANTITY
    Label(win, text="Quantity").pack(pady=5)
    qty_entry = Entry(win, width=30)
    qty_entry.pack()

    message = Label(win, text="")
    message.pack(pady=5)

    def save_part():
        try:
            add_part_to_job(
                job_map[job_var.get()],  # Get actual Job ID from map
                part_map[part_var.get()], # Get actual Part ID from map
                int(qty_entry.get())
            )
            message.config(text="Part added to job!", fg="green")
            qty_entry.delete(0, END)
        except Exception as e:
            message.config(text=str(e), fg="red")

    Button(win, text="Add Part", command=save_part).pack(pady=15)

# ---------------- EDIT LABOR COST WINDOW ----------------
def open_edit_labor():
    jobs = get_all_jobs()
    if not jobs:
        messagebox.showerror("Error", "No jobs found to edit!")
        return

    win = Toplevel()
    win.title("Edit Labor Cost")
    win.geometry("350x250")

    Label(win, text="Select Job").pack(pady=5)
    
    job_map = {
        f"Job #{j['job_id']} - {j['plate_no']} ({j['name']})": j['job_id']
        for j in jobs
    }
    job_var = StringVar()
    job_var.set(next(iter(job_map)))
    OptionMenu(win, job_var, *job_map.keys()).pack()

    Label(win, text="New Labor Cost (KWD)").pack(pady=5)
    labor_entry = Entry(win, width=30)
    labor_entry.pack()

    message = Label(win, text="")
    message.pack(pady=5)

    def save_new_cost():
        try:
            new_cost = float(labor_entry.get())
            selected_job_id = job_map[job_var.get()]
            
            update_labor_cost(selected_job_id, new_cost)
            
            message.config(text="Labor cost updated successfully!", fg="green")
            labor_entry.delete(0, END)
        except ValueError:
            message.config(text="Please enter a valid number.", fg="red")

    Button(win, text="Update Cost", command=save_new_cost).pack(pady=15)


# ---------------- MAIN APPLICATION ENTRY POINT ----------------
def run_app():
    root = Tk()
    root.title("Workshop Management System")
    root.geometry("400x550") # Made the window slightly taller

    Label(root, text="Automotive Workshop", font=("Arial", 16, "bold")).pack(pady=20)

    # Menu Buttons
    Button(root, text="Add Customer", width=30, command=open_add_customer).pack(pady=5)
    Button(root, text="Add Vehicle", width=30, command=open_add_vehicle).pack(pady=5)
    Button(root, text="Create Job Card", width=30, command=open_job_card).pack(pady=5)
    
    # --- NEW BUTTON ADDED HERE ---
    Button(root, text="Edit Labor Cost", width=30, command=open_edit_labor).pack(pady=5)
    
    Button(root, text="Inventory (Parts)", width=30, command=open_inventory).pack(pady=5)
    Button(root, text="Add Parts to Job", width=30, command=open_add_part_to_job).pack(pady=5)
    Button(root, text="Manage Invoices", width=30, command=open_invoices).pack(pady=5)

    # Exit Button
    Button(root, text="Exit", width=30, command=root.destroy, bg="#ffdddd").pack(pady=20)

    root.mainloop()

# 🚗 Automotive Workshop Management System

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A lightweight, standalone desktop application designed to streamline daily operations for an automotive repair shop. Built entirely in Python, this system handles customer registration, vehicle tracking, inventory management, job card creation, and automated PDF invoice generation.

## ✨ Key Features

* **Customer & Vehicle Management:** Register new clients and link multiple vehicles (Make, Model, License Plate) to their profiles.
* **Job Cards:** Create active service jobs and assign labor costs to specific vehicles.
* **Inventory Tracking:** Manage spare parts with real-time stock levels. Parts added to a job are automatically deducted from the main inventory.
* **Automated Billing & Auto-Sync:** Dynamically calculates total costs (Labor + Parts). Updating a labor charge or adding a new part automatically synchronizes and updates the existing invoice.
* **PDF Generation:** Exports professional, itemized invoices as PDF documents (powered by `reportlab`), complete with shop branding, formatted tables, and localized currency.
* **Standalone Executable:** Fully packaged using `PyInstaller`, allowing the software to run on any Windows machine without requiring a Python installation.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Frontend / GUI:** Tkinter (Python's standard GUI library)
* **Database:** SQLite3 (Local, serverless relational database)
* **PDF Engine:** ReportLab
* **Packaging:** PyInstaller

## 📂 Project Architecture

The application follows a modular architecture, separating the graphical interface from the business logic and database management:

* `main.py` - Application entry point.
* `gui.py` - Contains all Tkinter UI elements, windows, and event handlers.
* `database.py` - Handles SQLite connection and table initialization.
* `customers.py`, `vehicles.py`, `jobs.py`, `inventory.py`, `job_parts.py`, `invoices.py` - Backend logic modules for database CRUD operations.
* `pdf_generator.py` - Programmatic PDF generation logic.

## 🚀 Getting Started (For Developers)

### Prerequisites
You need Python 3 installed on your machine.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/workshop-manager.git](https://github.com/yourusername/workshop-manager.git)
   cd workshop-manager

```

2. Install the required PDF library:
```bash
pip install reportlab

```


3. Run the application:
```bash
python main.py

```


*(Note: The `workshop.db` file and an `INVOICES` directory will be generated automatically upon the first run).*

## 📦 Building the Executable

To compile the application into a single, portable Windows `.exe` file:

1. Install PyInstaller:
```bash
pip install pyinstaller

```


2. Run the build command:
```bash
python -m PyInstaller --noconsole --onefile --name="WorkshopManager" main.py

```


3. The executable will be available in the newly created `dist/` folder.


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

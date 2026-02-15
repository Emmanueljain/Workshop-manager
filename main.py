from database import create_tables
import gui

# 1. Initialize Database
create_tables()

# 2. Launch the Application
gui.run_app()
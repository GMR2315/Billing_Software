# File: C:\Projects\BillingSoftware\src\scripts\init_db.py

from sqlalchemy import create_engine
from src.models import Base

# Create a SQLAlchemy engine
engine = create_engine('mysql+pymysql://EDITH:Edith1891@localhost/billing_system')

# Create tables
Base.metadata.drop_all(engine)  # Drop all tables
Base.metadata.create_all(engine)  # Recreate tables

print("Database reinitialized successfully.")



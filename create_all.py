# File: C:\Projects\BillingSoftware\create_all.py


import sys
import os
from sqlalchemy import create_engine
from src.models.base import Base
from src.models.shop import Shop
from src.models.product import Product
from src.models.user import User

# Update the Python path to include src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Database URL
DATABASE_URL = 'mysql+pymysql://EDITH:Edith1891@localhost/billing_system'

# Create the engine
engine = create_engine(DATABASE_URL)

# Try to create tables and handle any exceptions
try:
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")


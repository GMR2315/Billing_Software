# File: src/models/__init__.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy engine
engine = create_engine('mysql+pymysql://EDITH:Edith1891@localhost/billing_system')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a base class
Base = declarative_base()

# Import models here after Base is defined
from .user import User
from .shop import Shop
from .product import Product

# Create tables (or do this in a separate script like init_db.py)
# Base.metadata.create_all(engine)

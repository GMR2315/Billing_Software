from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from shop import Shop
from product import Product
from user import User

DATABASE_URL = "mysql+pymysql://EDITH:1891%40Edith@localhost/billing_system"

# Create an engine
engine = create_engine(DATABASE_URL)

# Base class for models
Base = declarative_base()

# Create tables
if __name__ == "__main__":
    Base.metadata.create_all(engine)

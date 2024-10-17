from sqlalchemy import create_engine
from src.models.base import Base

# Replace these values with your MySQL database credentials
USER = 'your_mysql_username'
PASSWORD = 'your_mysql_password'
HOST = 'localhost'  # or your MySQL server IP
DATABASE = 'billing_software_db'

# Create the MySQL engine
engine = create_engine(f'mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}')

# Create all tables
Base.metadata.create_all(engine)

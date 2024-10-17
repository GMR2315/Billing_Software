import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.base import Base
# Other imports here

import logging
from sqlalchemy.exc import SQLAlchemyError
from src.models import Base, engine  # Adjusted import based on your project structure
from models.base import Base
from models.product import Product
from models.shop import Shop
from models.user import User
from sqlalchemy import create_engine
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_tables():
    try:
        # Create all tables in the database
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
    except SQLAlchemyError as e:
        logger.error(f"Error creating tables: {e}")
        raise  # Re-raise the exception after logging

if __name__ == "__main__":
    create_tables()

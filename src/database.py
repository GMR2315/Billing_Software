from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL for MySQL (corrected for special characters)
DATABASE_URL = "mysql+mysqlconnector://EDITH:1891@Edith@localhost/billing_system"


# Create an engine that connects to the MySQL database
engine = create_engine(DATABASE_URL)

# Create a base class for our models
Base = declarative_base()

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new session instance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

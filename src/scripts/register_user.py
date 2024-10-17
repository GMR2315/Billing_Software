import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import User, Shop
import bcrypt
import pytz
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database setup
engine = create_engine('mysql+pymysql://EDITH:Edith1891@localhost/billing_system')
Session = sessionmaker(bind=engine)

def hash_password(password: str) -> str:
    """Hashes the password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

def is_valid_email(email: str) -> bool:
    """Validates the email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_password(password: str) -> bool:
    """Checks if the password meets length requirements."""
    return len(password) >= 8

def convert_to_user_timezone(dt: datetime, timezone_str: str) -> datetime:
    """Converts UTC datetime to user timezone."""
    user_tz = pytz.timezone(timezone_str)
    return dt.astimezone(user_tz)

def normalize_shop_name(shop_name: str) -> str:
    """Normalizes the shop name for consistency."""
    return shop_name.strip().lower()

def register_or_update_user(username: str, password: str, email: str, shop_name: str, shop_location: str, timezone: str):
    """Registers or updates a user in the database."""
    session = Session()
    try:
        # Validate email and password
        if not is_valid_email(email):
            raise ValueError("Invalid email address.")
        if not is_valid_password(password):
            raise ValueError("Password must be at least 8 characters long.")

        existing_user = session.query(User).filter_by(username=username).first()

        # Ensure timezone is valid, set a default if necessary
        if timezone not in pytz.all_timezones:
            logging.warning(f"Invalid timezone '{timezone}', defaulting to 'UTC'")
            timezone = 'UTC'

        utc_now = datetime.now(pytz.utc)
        user_created_at = convert_to_user_timezone(utc_now, timezone)

        # Normalize shop name to avoid case and space discrepancies
        normalized_shop_name = normalize_shop_name(shop_name)

        # Get or create the shop based on name and location
        shop = session.query(Shop).filter_by(shop_name=normalized_shop_name, location=shop_location).first()
        if not shop:
            logging.info(f"Shop '{normalized_shop_name}' at location '{shop_location}' does not exist. Adding new shop.")
            shop = Shop(shop_name=normalized_shop_name, location=shop_location)
            session.add(shop)
            session.commit()
            logging.info(f"Shop '{normalized_shop_name}' added successfully at location '{shop_location}'.")

        if existing_user:
            logging.info(f"User with username '{username}' already exists. Updating user details.")
            existing_user.email = email
            existing_user.password = hash_password(password)  # Update password
            existing_user.shop_id = shop.id
            existing_user.timezone = timezone
            existing_user.updated_at = datetime.now(pytz.utc)
        else:
            logging.info(f"Creating new user '{username}'.")
            hashed_password = hash_password(password)
            new_user = User(
                username=username,
                password=hashed_password,
                email=email,
                shop_id=shop.id,
                timezone=timezone,
                created_at=user_created_at,
                updated_at=user_created_at
            )
            session.add(new_user)

        session.commit()
        logging.info(f"User '{username}' processed successfully.")
    except Exception as e:
        logging.error(f"Error processing user '{username}': {e}")
        session.rollback()
    finally:
        session.close()

def main():
    """Main function to execute the registration."""
    logging.info(f"Arguments received: {sys.argv}")

    if len(sys.argv) != 7:
        print("Usage: python -m src.scripts.register_user <username> <password> <email> <shop_name> <shop_location> <timezone>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    email = sys.argv[3]
    shop_name = sys.argv[4]
    shop_location = sys.argv[5]
    timezone = sys.argv[6]

    register_or_update_user(username, password, email, shop_name, shop_location, timezone)

if __name__ == "__main__":
    main()

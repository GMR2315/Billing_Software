from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.shop import Shop
from src.models.user import User
from src.models.product import Product

engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Define shop_name to check for duplicates
shop_name = "Test Shop"

# Check if the shop already exists
existing_shop = session.query(Shop).filter_by(shop_name=shop_name).first()

if not existing_shop:
    # Create a new shop if it does not exist
    new_shop = Shop(shop_name=shop_name)
    session.add(new_shop)
    session.commit()
    print(f"Shop '{shop_name}' created.")
    shop_id = new_shop.id
else:
    print(f"Shop '{shop_name}' already exists.")
    shop_id = existing_shop.id

# Define username to check for duplicates
username = "testuser"

# Check if the user already exists
existing_user = session.query(User).filter_by(username=username).first()

if not existing_user:
    # Create a new user if they do not exist
    new_user = User(username=username, password="password", shop_id=shop_id)
    session.add(new_user)
    session.commit()
    print(f"User '{username}' created.")
else:
    print(f"User '{username}' already exists.")

# Query and print data for verification
shop = session.query(Shop).first()
user = session.query(User).first()

print(f"Shop: {shop.shop_name}")
print(f"User: {user.username}, Shop ID: {user.shop_id}")

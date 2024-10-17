# File: src/scripts/manage_shops.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.models import Shop  # Ensure correct import

# Database setup
engine = create_engine('mysql+pymysql://EDITH:Edith1891@localhost/billing_system')
Session = sessionmaker(bind=engine)
session = Session()

def add_or_update_shop(shop_name: str):
    existing_shop = session.query(Shop).filter_by(shop_name=shop_name).first()
    
    if existing_shop:
        print(f"Shop with name '{shop_name}' already exists.")
        # Optionally, update shop details if needed
    else:
        new_shop = Shop(shop_name=shop_name)
        session.add(new_shop)
        try:
            session.commit()
            print(f"Shop '{shop_name}' added successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m src.scripts.manage_shops <shop_name>")
    else:
        shop_name = sys.argv[1]
        add_or_update_shop(shop_name)

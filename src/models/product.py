# File: C:\Projects\BillingSoftware\src\models\product.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func  # Import func from sqlalchemy.sql
from . import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    shop_id = Column(Integer, ForeignKey('shops.id'))

    shop = relationship('Shop', back_populates='products', lazy=True)



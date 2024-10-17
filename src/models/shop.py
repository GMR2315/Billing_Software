# File: src/models/shop.py

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from . import Base

class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('shop_name', 'location', name='uix_shop_name_location'),
    )

    products = relationship('Product', back_populates='shop', lazy=True)
    users = relationship('User', back_populates='shop', lazy=True)


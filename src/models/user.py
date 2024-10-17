# File: C:\Projects\BillingSoftware\src\models\user.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean  # Added Boolean import
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)  # Ensure Boolean is imported
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    shop_id = Column(Integer, ForeignKey('shops.id'))  # Ensure this matches your schema
    timezone = Column(String(50), nullable=False)

    shop = relationship('Shop', back_populates='users', lazy=True)


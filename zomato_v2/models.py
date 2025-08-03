from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Time, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    cuisine_type = Column(String(50), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    rating = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship to menu items
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Restaurant(id={self.id}, name='{self.name}', cuisine_type='{self.cuisine_type}')>"

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  # Decimal with 2 decimal places
    category = Column(String(50), nullable=False, index=True)
    is_vegetarian = Column(Boolean, nullable=False, default=False, index=True)
    is_vegan = Column(Boolean, nullable=False, default=False, index=True)
    is_available = Column(Boolean, nullable=False, default=True, index=True)
    preparation_time = Column(Integer, nullable=False)  # in minutes
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship to restaurant
    restaurant = relationship("Restaurant", back_populates="menu_items")
    
    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', price={self.price}, restaurant_id={self.restaurant_id})>"

"""
Routes Package for Zomato V3
============================

This package contains all API route definitions for the complete food delivery system.

Modules:
- restaurants: Restaurant CRUD operations and analytics
- menu_items: Menu item management with restaurant relationships
- customers: Customer management, order history, and analytics  
- orders: Order management with complex workflow and status tracking
- reviews: Review system for completed orders

Each module provides RESTful endpoints with proper error handling,
validation, and relationship management.
"""

__all__ = [
    "restaurants",
    "menu_items", 
    "customers",
    "orders",
    "reviews"
]

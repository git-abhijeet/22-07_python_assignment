import re


class Product:
    """E-Commerce Product Management System with @property decorators and validation."""
    
    def __init__(self, name, base_price, discount_percent, stock_quantity, category):
        """Initialize product with validation."""
        self.name = name
        self.base_price = base_price
        self.discount_percent = discount_percent
        self.stock_quantity = stock_quantity
        self.category = category
    
    @property
    def name(self):
        """Get product name."""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set product name with validation."""
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Name must be 3-50 characters")
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value):
            raise ValueError("Name can only contain letters, numbers, spaces, and hyphens")
        self._name = value
    
    @property
    def base_price(self):
        """Get base price."""
        return self._base_price
    
    @base_price.setter
    def base_price(self, value):
        """Set base price with validation."""
        if not isinstance(value, (int, float)):
            raise ValueError("Base price must be a number")
        if value <= 0:
            raise ValueError("Base price must be positive")
        if value > 50000:
            raise ValueError("Base price cannot exceed $50,000")
        self._base_price = float(value)
    
    @property
    def discount_percent(self):
        """Get discount percentage."""
        return self._discount_percent
    
    @discount_percent.setter
    def discount_percent(self, value):
        """Set discount percentage with validation and rounding."""
        if not isinstance(value, (int, float)):
            raise ValueError("Discount percent must be a number")
        if value < 0 or value > 75:
            raise ValueError("Discount percent must be between 0-75%")
        self._discount_percent = round(float(value), 2)
    
    @property
    def stock_quantity(self):
        """Get stock quantity."""
        return self._stock_quantity
    
    @stock_quantity.setter
    def stock_quantity(self, value):
        """Set stock quantity with validation."""
        if not isinstance(value, int):
            raise ValueError("Stock quantity must be an integer")
        if value < 0:
            raise ValueError("Stock quantity must be non-negative")
        if value > 10000:
            raise ValueError("Stock quantity cannot exceed 10,000 units")
        self._stock_quantity = value
    
    @property
    def category(self):
        """Get product category."""
        return self._category
    
    @category.setter
    def category(self, value):
        """Set product category with validation."""
        valid_categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        if value not in valid_categories:
            raise ValueError(f"Category must be one of: {valid_categories}")
        self._category = value
    
    @property
    def final_price(self):
        """Calculate final price after discount."""
        discount_amount = self._base_price * (self._discount_percent / 100)
        return round(self._base_price - discount_amount, 2)
    
    @property
    def savings_amount(self):
        """Calculate amount saved due to discount."""
        return round(self._base_price * (self._discount_percent / 100), 2)
    
    @property
    def availability_status(self):
        """Get availability status based on stock quantity."""
        if self._stock_quantity == 0:
            return "Out of Stock"
        elif self._stock_quantity < 10:
            return "Low Stock"
        else:
            return "In Stock"
    
    @property
    def product_summary(self):
        """Get formatted product summary."""
        return (f"Product: {self._name}\n"
                f"Category: {self._category}\n"
                f"Base Price: ${self._base_price:.2f}\n"
                f"Discount: {self._discount_percent}%\n"
                f"Final Price: ${self.final_price:.2f}\n"
                f"Savings: ${self.savings_amount:.2f}\n"
                f"Stock: {self._stock_quantity} units\n"
                f"Status: {self.availability_status}")


if __name__ == "__main__":
    # Test Case 1: Valid product creation and automatic calculations
    product = Product("Gaming Laptop", 1299.99, 15.5, 25, "Electronics")
    assert product.name == "Gaming Laptop"
    assert product.base_price == 1299.99
    assert product.discount_percent == 15.5
    assert abs(product.final_price - 1098.49) < 0.01
    assert abs(product.savings_amount - 201.50) < 0.01
    assert product.availability_status == "In Stock"
    print("Test Case 1: PASSED")

    # Test Case 2: Property setters with automatic recalculation
    product.discount_percent = 20.567  # Should round to 20.57
    assert product.discount_percent == 20.57
    assert abs(product.final_price - 1032.58) < 0.01

    product.stock_quantity = 5
    assert product.availability_status == "Low Stock"
    print("Test Case 2: PASSED")

    # Test Case 3: Validation edge cases
    try:
        product.name = "AB"  # Too short
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "3-50 characters" in str(e)

    try:
        product.base_price = -100  # Negative price
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    try:
        product.category = "InvalidCategory"
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    print("Test Case 3: PASSED")

    # Test Case 4: Product summary formatting
    assert "Gaming Laptop" in product.product_summary
    assert "1299.99" in product.product_summary
    assert "Low Stock" in product.product_summary
    print("Test Case 4: PASSED")

    print("\nAll tests passed! Product class is working correctly.")
    print("\nProduct Summary:")
    print(product.product_summary)

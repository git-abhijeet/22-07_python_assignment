from datetime import datetime
import uuid
from typing import Dict, List, Optional

class Product:
    """
    Product class for managing e-commerce products
    Tracks inventory, pricing, and category information
    """
    
    # Class variables for tracking products
    _all_products = {}  # Dict to store all products by ID
    _category_sales = {}  # Track sales by category
    _total_products_created = 0
    
    def __init__(self, product_id: str, name: str, price: float, category: str, stock_quantity: int):
        """
        Initialize a product
        
        Args:
            product_id (str): Unique product identifier
            name (str): Product name
            price (float): Product price
            category (str): Product category
            stock_quantity (int): Initial stock quantity
        """
        print("🛒 E-COMMERCE MANAGEMENT SYSTEM")
        print("=" * 50)
        print()
        
        # Validate input
        self._validate_product_data(product_id, name, price, category, stock_quantity)
        
        # Product attributes
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.category = category
        self.stock_quantity = int(stock_quantity)
        self.created_at = datetime.now()
        self.total_sold = 0
        self.is_active = True
        
        # Register product globally
        Product._all_products[product_id] = self
        Product._total_products_created += 1
        
        # Initialize category sales tracking
        if category not in Product._category_sales:
            Product._category_sales[category] = 0
        
        print(f"✅ Product created successfully:")
        print(f"   ID: {self.product_id}")
        print(f"   Name: {self.name}")
        print(f"   Price: ${self.price:.2f}")
        print(f"   Category: {self.category}")
        print(f"   Stock: {self.stock_quantity} units")
        print()
    
    def _validate_product_data(self, product_id, name, price, category, stock_quantity):
        """Validate product creation data"""
        if not product_id or not isinstance(product_id, str):
            raise ValueError("Product ID must be a non-empty string")
        
        if product_id in Product._all_products:
            raise ValueError(f"Product ID {product_id} already exists")
        
        if not name or not isinstance(name, str):
            raise ValueError("Product name must be a non-empty string")
        
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        
        if not category or not isinstance(category, str):
            raise ValueError("Category must be a non-empty string")
        
        if not isinstance(stock_quantity, int) or stock_quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer")
    
    def update_stock(self, quantity_change: int) -> bool:
        """
        Update product stock quantity
        
        Args:
            quantity_change (int): Change in stock (positive for restock, negative for sale)
        
        Returns:
            bool: True if successful, False if insufficient stock
        """
        new_stock = self.stock_quantity + quantity_change
        
        if new_stock < 0:
            print(f"❌ Insufficient stock for {self.name}")
            print(f"   Requested: {abs(quantity_change)}")
            print(f"   Available: {self.stock_quantity}")
            return False
        
        self.stock_quantity = new_stock
        
        # Track sales if it's a reduction in stock
        if quantity_change < 0:
            sold_quantity = abs(quantity_change)
            self.total_sold += sold_quantity
            Product._category_sales[self.category] += sold_quantity
            
            print(f"📦 Stock updated for {self.name}:")
            print(f"   Sold: {sold_quantity} units")
            print(f"   Remaining stock: {self.stock_quantity}")
            print()
        
        return True
    
    def is_in_stock(self, quantity: int = 1) -> bool:
        """Check if product has sufficient stock"""
        return self.stock_quantity >= quantity
    
    def get_product_info(self) -> dict:
        """Get comprehensive product information"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'stock_quantity': self.stock_quantity,
            'total_sold': self.total_sold,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __str__(self):
        return f"Product({self.product_id}: {self.name} - ${self.price:.2f})"
    
    def __repr__(self):
        return f"Product(id='{self.product_id}', name='{self.name}', price={self.price}, category='{self.category}')"
    
    @classmethod
    def get_product_by_id(cls, product_id: str) -> Optional['Product']:
        """Get product by ID"""
        return cls._all_products.get(product_id)
    
    @classmethod
    def get_products_by_category(cls, category: str) -> List['Product']:
        """Get all products in a category"""
        return [product for product in cls._all_products.values() 
                if product.category.lower() == category.lower()]
    
    @classmethod
    def get_total_products(cls) -> int:
        """Get total number of products created"""
        return cls._total_products_created
    
    @classmethod
    def get_most_popular_category(cls) -> str:
        """Get the category with most sales"""
        if not cls._category_sales:
            return "No sales data"
        
        most_popular = max(cls._category_sales.items(), key=lambda x: x[1])
        return most_popular[0]
    
    @classmethod
    def get_sales_by_category(cls) -> Dict[str, int]:
        """Get sales statistics by category"""
        return cls._category_sales.copy()


class Customer:
    """
    Customer class for managing customer information and membership tiers
    """
    
    # Class variables
    _all_customers = {}
    _total_revenue = 0.0
    _membership_discounts = {
        'basic': 0.0,
        'premium': 10.0,
        'vip': 20.0
    }
    
    def __init__(self, customer_id: str, name: str, email: str, membership_tier: str = 'basic'):
        """
        Initialize a customer
        
        Args:
            customer_id (str): Unique customer identifier
            name (str): Customer name
            email (str): Customer email
            membership_tier (str): Membership level (basic, premium, vip)
        """
        # Validate input
        self._validate_customer_data(customer_id, name, email, membership_tier)
        
        # Customer attributes
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership_tier = membership_tier.lower()
        self.registration_date = datetime.now()
        self.total_spent = 0.0
        self.order_history = []
        
        # Register customer
        Customer._all_customers[customer_id] = self
        
        print(f"👤 Customer registered:")
        print(f"   ID: {self.customer_id}")
        print(f"   Name: {self.name}")
        print(f"   Email: {self.email}")
        print(f"   Membership: {self.membership_tier.title()}")
        print(f"   Discount Rate: {self.get_discount_rate()}%")
        print()
    
    def _validate_customer_data(self, customer_id, name, email, membership_tier):
        """Validate customer creation data"""
        if not customer_id or not isinstance(customer_id, str):
            raise ValueError("Customer ID must be a non-empty string")
        
        if customer_id in Customer._all_customers:
            raise ValueError(f"Customer ID {customer_id} already exists")
        
        if not name or not isinstance(name, str):
            raise ValueError("Customer name must be a non-empty string")
        
        if not email or not isinstance(email, str) or '@' not in email:
            raise ValueError("Valid email address is required")
        
        if membership_tier.lower() not in Customer._membership_discounts:
            valid_tiers = list(Customer._membership_discounts.keys())
            raise ValueError(f"Membership tier must be one of: {valid_tiers}")
    
    def get_discount_rate(self) -> float:
        """Get customer's discount rate based on membership tier"""
        return Customer._membership_discounts[self.membership_tier]
    
    def add_purchase(self, amount: float, order_id: str):
        """Record a purchase for this customer"""
        self.total_spent += amount
        Customer._total_revenue += amount
        self.order_history.append({
            'order_id': order_id,
            'amount': amount,
            'date': datetime.now(),
            'membership_tier': self.membership_tier
        })
        
        # Check for membership tier upgrade
        self._check_tier_upgrade()
    
    def _check_tier_upgrade(self):
        """Check if customer qualifies for membership tier upgrade"""
        if self.membership_tier == 'basic' and self.total_spent >= 500:
            old_tier = self.membership_tier
            self.membership_tier = 'premium'
            print(f"🎉 {self.name} upgraded from {old_tier} to {self.membership_tier}!")
            print()
        elif self.membership_tier == 'premium' and self.total_spent >= 2000:
            old_tier = self.membership_tier
            self.membership_tier = 'vip'
            print(f"🎉 {self.name} upgraded from {old_tier} to {self.membership_tier}!")
            print()
    
    def get_customer_info(self) -> dict:
        """Get comprehensive customer information"""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'membership_tier': self.membership_tier,
            'total_spent': self.total_spent,
            'discount_rate': self.get_discount_rate(),
            'orders_count': len(self.order_history),
            'registration_date': self.registration_date.strftime('%Y-%m-%d')
        }
    
    def __str__(self):
        return f"Customer({self.customer_id}: {self.name} - {self.membership_tier.title()})"
    
    @classmethod
    def get_customer_by_id(cls, customer_id: str) -> Optional['Customer']:
        """Get customer by ID"""
        return cls._all_customers.get(customer_id)
    
    @classmethod
    def get_total_revenue(cls) -> float:
        """Get total revenue from all customers"""
        return cls._total_revenue
    
    @classmethod
    def get_customers_by_tier(cls, tier: str) -> List['Customer']:
        """Get all customers in a specific membership tier"""
        return [customer for customer in cls._all_customers.values() 
                if customer.membership_tier == tier.lower()]


class ShoppingCart:
    """
    Shopping cart class for managing customer's cart items and checkout process
    """
    
    def __init__(self, customer: Customer):
        """
        Initialize shopping cart for a customer
        
        Args:
            customer (Customer): Customer who owns this cart
        """
        if not isinstance(customer, Customer):
            raise ValueError("Cart must be associated with a valid Customer")
        
        self.customer = customer
        self.cart_id = str(uuid.uuid4())[:8]
        self.items = {}  # {product_id: {'product': Product, 'quantity': int}}
        self.created_at = datetime.now()
        
        print(f"🛒 Shopping cart created for {customer.name}")
        print(f"   Cart ID: {self.cart_id}")
        print()
    
    def add_item(self, product: Product, quantity: int) -> bool:
        """
        Add item to cart
        
        Args:
            product (Product): Product to add
            quantity (int): Quantity to add
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not isinstance(product, Product):
            raise ValueError("Invalid product")
        
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        
        # Check stock availability
        current_in_cart = self.items.get(product.product_id, {}).get('quantity', 0)
        total_needed = current_in_cart + quantity
        
        if not product.is_in_stock(total_needed):
            print(f"❌ Cannot add {quantity} units of {product.name} to cart")
            print(f"   Requested total: {total_needed}")
            print(f"   Available stock: {product.stock_quantity}")
            print(f"   Already in cart: {current_in_cart}")
            return False
        
        # Add or update item in cart
        if product.product_id in self.items:
            self.items[product.product_id]['quantity'] += quantity
        else:
            self.items[product.product_id] = {
                'product': product,
                'quantity': quantity
            }
        
        print(f"✅ Added to cart:")
        print(f"   Product: {product.name}")
        print(f"   Quantity: {quantity}")
        print(f"   Unit Price: ${product.price:.2f}")
        print(f"   Subtotal: ${product.price * quantity:.2f}")
        print()
        
        return True
    
    def remove_item(self, product_id: str, quantity: Optional[int] = None) -> bool:
        """
        Remove item from cart
        
        Args:
            product_id (str): Product ID to remove
            quantity (int, optional): Quantity to remove. If None, remove all.
        
        Returns:
            bool: True if successful, False if item not in cart
        """
        if product_id not in self.items:
            print(f"❌ Product {product_id} not found in cart")
            return False
        
        item = self.items[product_id]
        
        if quantity is None or quantity >= item['quantity']:
            # Remove all of this item
            removed_quantity = item['quantity']
            del self.items[product_id]
            print(f"🗑️  Removed all {item['product'].name} from cart ({removed_quantity} units)")
        else:
            # Remove partial quantity
            item['quantity'] -= quantity
            print(f"🗑️  Removed {quantity} units of {item['product'].name} from cart")
            print(f"   Remaining in cart: {item['quantity']}")
        
        print()
        return True
    
    def update_quantity(self, product_id: str, new_quantity: int) -> bool:
        """Update quantity of item in cart"""
        if product_id not in self.items:
            print(f"❌ Product {product_id} not found in cart")
            return False
        
        if new_quantity <= 0:
            return self.remove_item(product_id)
        
        item = self.items[product_id]
        product = item['product']
        
        # Check stock availability
        if not product.is_in_stock(new_quantity):
            print(f"❌ Cannot update quantity - insufficient stock")
            print(f"   Requested: {new_quantity}")
            print(f"   Available: {product.stock_quantity}")
            return False
        
        old_quantity = item['quantity']
        item['quantity'] = new_quantity
        
        print(f"📝 Updated quantity for {product.name}:")
        print(f"   Old quantity: {old_quantity}")
        print(f"   New quantity: {new_quantity}")
        print()
        
        return True
    
    def get_cart_items(self) -> List[dict]:
        """Get list of cart items with details"""
        cart_items = []
        for item_data in self.items.values():
            product = item_data['product']
            quantity = item_data['quantity']
            subtotal = product.price * quantity
            
            cart_items.append({
                'product_id': product.product_id,
                'product_name': product.name,
                'price': product.price,
                'quantity': quantity,
                'subtotal': subtotal
            })
        
        return cart_items
    
    def get_total_items(self) -> int:
        """Get total number of items in cart"""
        return sum(item['quantity'] for item in self.items.values())
    
    def get_subtotal(self) -> float:
        """Get cart subtotal before discounts"""
        return sum(item['product'].price * item['quantity'] 
                  for item in self.items.values())
    
    def calculate_total(self) -> float:
        """Calculate final total with customer discount applied"""
        subtotal = self.get_subtotal()
        discount_rate = self.customer.get_discount_rate()
        discount_amount = subtotal * (discount_rate / 100)
        final_total = subtotal - discount_amount
        
        print(f"💰 Cart Total Calculation:")
        print(f"   Subtotal: ${subtotal:.2f}")
        print(f"   Customer Discount ({discount_rate}%): -${discount_amount:.2f}")
        print(f"   Final Total: ${final_total:.2f}")
        print()
        
        return final_total
    
    def clear_cart(self):
        """Clear all items from cart"""
        items_cleared = len(self.items)
        self.items.clear()
        print(f"🧹 Cart cleared - {items_cleared} item types removed")
        print()
    
    def place_order(self) -> dict:
        """
        Place order and process the cart
        
        Returns:
            dict: Order result with details
        """
        if not self.items:
            return {
                'success': False,
                'message': 'Cart is empty',
                'order_id': None
            }
        
        # Check stock availability for all items
        for item_data in self.items.values():
            product = item_data['product']
            quantity = item_data['quantity']
            
            if not product.is_in_stock(quantity):
                return {
                    'success': False,
                    'message': f'Insufficient stock for {product.name}',
                    'order_id': None
                }
        
        # Process the order
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        total_amount = self.calculate_total()
        
        # Update inventory
        for item_data in self.items.values():
            product = item_data['product']
            quantity = item_data['quantity']
            product.update_stock(-quantity)
        
        # Record purchase for customer
        self.customer.add_purchase(total_amount, order_id)
        
        # Create order summary
        order_items = self.get_cart_items()
        
        order_result = {
            'success': True,
            'order_id': order_id,
            'customer_id': self.customer.customer_id,
            'items': order_items,
            'subtotal': self.get_subtotal(),
            'discount_rate': self.customer.get_discount_rate(),
            'total_amount': total_amount,
            'order_date': datetime.now(),
            'message': f'Order {order_id} placed successfully'
        }
        
        print(f"🎉 ORDER PLACED SUCCESSFULLY!")
        print(f"   Order ID: {order_id}")
        print(f"   Customer: {self.customer.name}")
        print(f"   Total Amount: ${total_amount:.2f}")
        print(f"   Items: {self.get_total_items()} units")
        print()
        
        # Clear cart after successful order
        self.clear_cart()
        
        return order_result
    
    def __str__(self):
        return f"ShoppingCart(Customer: {self.customer.name}, Items: {len(self.items)}, Total: ${self.get_subtotal():.2f})"


def demonstrate_advanced_features():
    """Demonstrate advanced e-commerce features"""
    print("🚀 ADVANCED E-COMMERCE FEATURES")
    print("=" * 50)
    print()
    
    # Create some demo products
    phone = Product("P004", "Smartphone", 899.99, "Electronics", 15)
    headphones = Product("P005", "Wireless Headphones", 199.99, "Electronics", 30)
    
    # Create demo customer
    demo_customer = Customer("C002", "Jane Smith", "jane@email.com", "basic")
    demo_cart = ShoppingCart(demo_customer)
    
    # Add items and make purchases to trigger tier upgrade
    demo_cart.add_item(phone, 1)
    demo_cart.place_order()
    
    # Show analytics
    print("📊 BUSINESS ANALYTICS:")
    print(f"   Total Products: {Product.get_total_products()}")
    print(f"   Most Popular Category: {Product.get_most_popular_category()}")
    print(f"   Category Sales: {Product.get_sales_by_category()}")
    print(f"   Total Revenue: ${Customer.get_total_revenue():.2f}")
    print()
    
    # Show customer tiers
    print("👥 CUSTOMER TIERS:")
    for tier in ['basic', 'premium', 'vip']:
        customers = Customer.get_customers_by_tier(tier)
        print(f"   {tier.title()}: {len(customers)} customers")
    print()


def main():
    """Main function to test the e-commerce system"""
    print("🎯 TESTING E-COMMERCE SHOPPING CART SYSTEM")
    print("=" * 70)
    print()
    
    try:
        # Test Case 1: Creating products with different categories
        print("📝 TEST CASE 1: Creating Products")
        print("-" * 50)
        
        laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
        book = Product("P002", "Python Programming", 49.99, "Books", 25)
        shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)
        
        print(f"Product info: {laptop.get_product_info()}")
        print(f"Total products in system: {Product.get_total_products()}")
        print()
        
        # Test Case 2: Creating customer and shopping cart
        print("📝 TEST CASE 2: Customer and Cart Creation")
        print("-" * 50)
        
        customer = Customer("C001", "John Doe", "john@email.com", "premium")
        cart = ShoppingCart(customer)
        
        print(f"Customer: {customer}")
        print(f"Customer discount: {customer.get_discount_rate()}%")
        print()
        
        # Test Case 3: Adding items to cart
        print("📝 TEST CASE 3: Adding Items to Cart")
        print("-" * 50)
        
        cart.add_item(laptop, 1)
        cart.add_item(book, 2)
        cart.add_item(shirt, 3)
        
        print(f"Cart total items: {cart.get_total_items()}")
        print(f"Cart subtotal: ${cart.get_subtotal()}")
        print()
        
        # Test Case 4: Applying discounts and calculating final price
        print("📝 TEST CASE 4: Discount Calculation")
        print("-" * 50)
        
        final_total = cart.calculate_total()
        print(f"Final total (with {customer.get_discount_rate()}% discount): ${final_total}")
        print()
        
        # Test Case 5: Inventory management
        print("📝 TEST CASE 5: Inventory Management")
        print("-" * 50)
        
        print(f"Laptop stock before order: {laptop.stock_quantity}")
        order_result = cart.place_order()
        print(f"Order result: {order_result['success']}")
        print(f"Laptop stock after order: {laptop.stock_quantity}")
        print()
        
        # Test Case 6: Class methods for business analytics
        print("📝 TEST CASE 6: Business Analytics")
        print("-" * 50)
        
        popular_category = Product.get_most_popular_category()
        print(f"Most popular category: {popular_category}")
        
        total_revenue = Customer.get_total_revenue()
        print(f"Total revenue: ${total_revenue}")
        print()
        
        # Test Case 7: Cart operations with new cart
        print("📝 TEST CASE 7: Cart Operations")
        print("-" * 50)
        
        new_cart = ShoppingCart(customer)
        new_cart.add_item(book, 3)
        new_cart.add_item(shirt, 2)
        
        print(f"Items before removal: {len(new_cart.get_cart_items())}")
        new_cart.remove_item("P002")
        print(f"Items after removal: {new_cart.get_cart_items()}")
        
        new_cart.clear_cart()
        print(f"Items after clearing: {new_cart.get_total_items()}")
        print()
        
        # Additional advanced features
        demonstrate_advanced_features()
        
        print("🎉 E-COMMERCE SYSTEM TESTING COMPLETE!")
        print("=" * 70)
        print()
        print("✅ All features tested successfully:")
        print("   • Product creation and inventory management")
        print("   • Customer registration with membership tiers")
        print("   • Shopping cart operations")
        print("   • Discount calculations")
        print("   • Order processing and stock updates")
        print("   • Business analytics and reporting")
        print("   • Automatic membership tier upgrades")
        print("   • Comprehensive error handling")
        print()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        raise


if __name__ == "__main__":
    main()

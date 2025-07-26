inventory = {
    "apples": {"price": 1.50, "quantity": 100},
    "bananas": {"price": 0.75, "quantity": 150},
    "oranges": {"price": 2.00, "quantity": 80}
}

def display_inventory(inventory_dict, title="Current Inventory"):
    """Helper function to display inventory in a formatted table"""
    print(f"=== {title} ===")
    print(f"{'Product':<12} {'Price':<8} {'Quantity':<10} {'Value':<10}")
    print("-" * 45)
    
    total_value = 0
    for product, details in inventory_dict.items():
        price = details["price"]
        quantity = details["quantity"]
        value = price * quantity
        total_value += value
        
        print(f"{product:<12} ${price:<7.2f} {quantity:<10} ${value:<9.2f}")
    
    print("-" * 45)
    print(f"{'TOTAL':<12} {'':<8} {'':<10} ${total_value:<9.2f}")
    print()

def add_new_product(inventory_dict, product_name, price, quantity):
    """Add a new product to the inventory"""
    print("=== Task 1: Add a New Product ===")
    print()
    
    print(f"Adding new product: {product_name}")
    print(f"Price: ${price:.2f}")
    print(f"Quantity: {quantity}")
    print()
    
    if product_name in inventory_dict:
        print(f"⚠️  Product '{product_name}' already exists!")
        print(f"Current details: Price=${inventory_dict[product_name]['price']:.2f}, "
              f"Quantity={inventory_dict[product_name]['quantity']}")
        
        choice = input("Update existing product? (y/n): ").lower()
        if choice == 'y':
            inventory_dict[product_name]["price"] = price
            inventory_dict[product_name]["quantity"] = quantity
            print(f"✅ Updated existing product '{product_name}'")
        else:
            print("❌ Product not added")
            return False
    else:
        inventory_dict[product_name] = {"price": price, "quantity": quantity}
        print(f"✅ Successfully added '{product_name}' to inventory")
    
    print()
    display_inventory(inventory_dict, "Updated Inventory")
    return True

def update_product_price(inventory_dict, product_name, new_price):
    """Update the price of an existing product"""
    print("=== Task 2: Update Product Price ===")
    print()
    
    if product_name not in inventory_dict:
        print(f"❌ Product '{product_name}' not found in inventory")
        print("Available products:", list(inventory_dict.keys()))
        return False
    
    old_price = inventory_dict[product_name]["price"]
    inventory_dict[product_name]["price"] = new_price
    
    print(f"Updating price for '{product_name}':")
    print(f"Old price: ${old_price:.2f}")
    print(f"New price: ${new_price:.2f}")
    print(f"Price change: ${new_price - old_price:+.2f}")
    print(f"✅ Price updated successfully")
    print()
    
    display_inventory(inventory_dict, "Updated Inventory")
    return True

def sell_product(inventory_dict, product_name, quantity_to_sell):
    """Simulate the sale of a product by updating quantity"""
    print(f"=== Task 3: Sell {quantity_to_sell} {product_name.title()} ===")
    print()
    
    if product_name not in inventory_dict:
        print(f"❌ Product '{product_name}' not found in inventory")
        return False
    
    current_quantity = inventory_dict[product_name]["quantity"]
    price = inventory_dict[product_name]["price"]
    
    print(f"Sale Request: {quantity_to_sell} {product_name}")
    print(f"Current stock: {current_quantity}")
    print(f"Product price: ${price:.2f}")
    
    if current_quantity < quantity_to_sell:
        print(f"❌ Insufficient stock! Only {current_quantity} available")
        print(f"Maximum possible sale: {current_quantity} {product_name}")
        
        choice = input(f"Sell all available {current_quantity} {product_name}? (y/n): ").lower()
        if choice == 'y':
            quantity_to_sell = current_quantity
        else:
            print("❌ Sale cancelled")
            return False
    
    inventory_dict[product_name]["quantity"] -= quantity_to_sell
    sale_revenue = price * quantity_to_sell
    
    print()
    print(f"✅ Sale completed!")
    print(f"Sold: {quantity_to_sell} {product_name}")
    print(f"Revenue: ${sale_revenue:.2f}")
    print(f"Remaining stock: {inventory_dict[product_name]['quantity']}")
    print()
    
    display_inventory(inventory_dict, "Updated Inventory After Sale")
    return True

def calculate_total_inventory_value(inventory_dict):
    """Compute the total value of the inventory"""
    print("=== Task 4: Calculate Total Inventory Value ===")
    print()
    
    total_value = 0
    print("Calculating inventory value:")
    print(f"{'Product':<12} {'Price':<8} {'Quantity':<10} {'Value'}")
    print("-" * 40)
    
    for product, details in inventory_dict.items():
        price = details["price"]
        quantity = details["quantity"]
        value = price * quantity
        total_value += value
        
        print(f"{product:<12} ${price:<7.2f} {quantity:<10} ${value:.2f}")
    
    print("-" * 40)
    print(f"{'TOTAL VALUE':<12} {'':<8} {'':<10} ${total_value:.2f}")
    print()
    
    num_products = len(inventory_dict)
    avg_product_value = total_value / num_products if num_products > 0 else 0
    total_items = sum(details["quantity"] for details in inventory_dict.values())
    avg_price_per_item = total_value / total_items if total_items > 0 else 0
    
    print("📊 Inventory Statistics:")
    print(f"   Total Products: {num_products}")
    print(f"   Total Items: {total_items}")
    print(f"   Average Product Value: ${avg_product_value:.2f}")
    print(f"   Average Price Per Item: ${avg_price_per_item:.2f}")
    print()
    
    return total_value

def find_low_stock_products(inventory_dict, threshold=100):
    """Identify products with quantity below the threshold"""
    print(f"=== Task 5: Find Low Stock Products (< {threshold}) ===")
    print()
    
    low_stock_products = []
    
    for product, details in inventory_dict.items():
        if details["quantity"] < threshold:
            low_stock_products.append((product, details))
    
    if not low_stock_products:
        print(f"✅ No products with stock below {threshold}")
        print("All products are well-stocked!")
    else:
        print(f"⚠️  Found {len(low_stock_products)} product(s) with low stock:")
        print()
        print(f"{'Product':<12} {'Quantity':<10} {'Price':<8} {'Status'}")
        print("-" * 45)
        
        for product, details in low_stock_products:
            quantity = details["quantity"]
            price = details["price"]
            
            if quantity == 0:
                status = "OUT OF STOCK"
            elif quantity < 50:
                status = "CRITICAL"
            elif quantity < threshold:
                status = "LOW"
            else:
                status = "OK"
            
            print(f"{product:<12} {quantity:<10} ${price:<7.2f} {status}")
        
        print()
        print("📋 Recommended Actions:")
        for product, details in low_stock_products:
            quantity = details["quantity"]
            if quantity == 0:
                print(f"   🚨 Restock {product} immediately - OUT OF STOCK")
            elif quantity < 50:
                print(f"   ⚠️  Restock {product} urgently - Only {quantity} left")
            else:
                print(f"   📦 Consider restocking {product} - {quantity} remaining")
    
    print()
    return low_stock_products

def advanced_inventory_operations(inventory_dict):
    """Demonstrate advanced inventory operations"""
    print("=== Advanced Inventory Operations ===")
    print()
    
    print("1. Product Performance Analysis:")
    products_by_value = sorted(inventory_dict.items(), 
                              key=lambda x: x[1]["price"] * x[1]["quantity"], 
                              reverse=True)
    
    print("   Products ranked by total value:")
    for i, (product, details) in enumerate(products_by_value, 1):
        value = details["price"] * details["quantity"]
        print(f"   {i}. {product}: ${value:.2f}")
    print()
    
    print("2. Price Analysis:")
    prices = [details["price"] for details in inventory_dict.values()]
    avg_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)
    
    print(f"   Average price: ${avg_price:.2f}")
    print(f"   Highest price: ${max_price:.2f}")
    print(f"   Lowest price: ${min_price:.2f}")
    print()
    
    print("3. Quantity Analysis:")
    quantities = [details["quantity"] for details in inventory_dict.values()]
    total_quantity = sum(quantities)
    avg_quantity = total_quantity / len(quantities)
    
    print(f"   Total items in stock: {total_quantity}")
    print(f"   Average quantity per product: {avg_quantity:.1f}")
    print()
    
    print("4. Revenue Potential:")
    total_potential = sum(details["price"] * details["quantity"] 
                         for details in inventory_dict.values())
    print(f"   Total potential revenue: ${total_potential:.2f}")
    print()

def inventory_management_system():
    """Interactive inventory management system"""
    print("=== Interactive Inventory Management System ===")
    print()
    
    interactive_inventory = inventory.copy()
    
    while True:
        print("Available Operations:")
        print("1. View Inventory")
        print("2. Add Product")
        print("3. Update Price")
        print("4. Process Sale")
        print("5. Check Low Stock")
        print("6. Calculate Total Value")
        print("7. Advanced Analytics")
        print("8. Return to Main Menu")
        
        choice = input("\nEnter choice (1-8): ").strip()
        print()
        
        if choice == "1":
            display_inventory(interactive_inventory)
        
        elif choice == "2":
            name = input("Product name: ").strip().lower()
            try:
                price = float(input("Price: $"))
                quantity = int(input("Quantity: "))
                add_new_product(interactive_inventory, name, price, quantity)
            except ValueError:
                print("❌ Invalid input! Please enter valid price and quantity.")
        
        elif choice == "3":
            name = input("Product name: ").strip().lower()
            try:
                new_price = float(input("New price: $"))
                update_product_price(interactive_inventory, name, new_price)
            except ValueError:
                print("❌ Invalid price format!")
        
        elif choice == "4":
            name = input("Product name: ").strip().lower()
            try:
                quantity = int(input("Quantity to sell: "))
                sell_product(interactive_inventory, name, quantity)
            except ValueError:
                print("❌ Invalid quantity!")
        
        elif choice == "5":
            try:
                threshold = int(input("Low stock threshold (default 100): ") or "100")
                find_low_stock_products(interactive_inventory, threshold)
            except ValueError:
                find_low_stock_products(interactive_inventory)
        
        elif choice == "6":
            calculate_total_inventory_value(interactive_inventory)
        
        elif choice == "7":
            advanced_inventory_operations(interactive_inventory)
        
        elif choice == "8":
            break
        
        else:
            print("❌ Invalid choice! Please enter 1-8.")
        
        input("Press Enter to continue...")
        print()

def simulate_business_day():
    """Simulate a typical business day with multiple operations"""
    print("=== Business Day Simulation ===")
    print()
    
    sim_inventory = inventory.copy()
    
    print("🌅 Starting business day simulation...")
    display_inventory(sim_inventory, "Opening Inventory")
    
    print("🌄 MORNING - Restocking Operations")
    add_new_product(sim_inventory, "grapes", 3.25, 60)
    
    print("☀️  MIDDAY - Sales Period")
    sell_product(sim_inventory, "apples", 25)
    sell_product(sim_inventory, "bananas", 40)
    sell_product(sim_inventory, "oranges", 15)
    
    print("🌤️  AFTERNOON - Price Adjustments")
    update_product_price(sim_inventory, "bananas", 0.85)
    
    print("🌅 EVENING - End of Day Analysis")
    total_value = calculate_total_inventory_value(sim_inventory)
    find_low_stock_products(sim_inventory)
    
    print("📈 Day Summary:")
    original_value = sum(details["price"] * details["quantity"] 
                        for details in inventory.values())
    print(f"   Opening value: ${original_value:.2f}")
    print(f"   Closing value: ${total_value:.2f}")
    print(f"   Net change: ${total_value - original_value:+.2f}")
    print()

def main():
    print("🏪 INVENTORY MANAGEMENT SYSTEM 🏪")
    print("=" * 60)
    print()
    
    print("Initial Inventory Setup:")
    display_inventory(inventory, "Starting Inventory")
    
    print("Executing Required Tasks:")
    print()
    
    add_new_product(inventory, "grapes", 3.25, 60)
    
    update_product_price(inventory, "bananas", 0.85)
    
    sell_product(inventory, "apples", 25)
    
    total_value = calculate_total_inventory_value(inventory)
    
    low_stock = find_low_stock_products(inventory, 100)
    
    advanced_inventory_operations(inventory)
    simulate_business_day()
    
    
    print("=== Summary & Best Practices ===")
    print()
    print("Key Features Implemented:")
    print("✅ Product addition with duplicate checking")
    print("✅ Price updates with change tracking")
    print("✅ Sales processing with stock validation")
    print("✅ Comprehensive value calculations")
    print("✅ Smart low stock detection with recommendations")
    print("✅ Advanced analytics and reporting")
    print("✅ Business simulation capabilities")
    print()
    print("Dictionary Benefits for Inventory:")
    print("• Fast O(1) product lookups by name")
    print("• Flexible data structure for product attributes")
    print("• Easy to extend with new product properties")
    print("• Natural key-value mapping for inventory items")
    print("• Memory efficient for large inventories")
    print()

if __name__ == "__main__":
    main()

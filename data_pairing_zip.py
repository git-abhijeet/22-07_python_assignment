products = ["Laptop", "Mouse", "Keyboard", "Monitor"]
prices = [999.99, 25.50, 75.00, 299.99]
quantities = [5, 20, 15, 8]

def display_initial_data():
    """Display the initial parallel lists"""
    print("=== Initial Data ===")
    print()
    print("Parallel Lists:")
    print(f"Products:   {products}")
    print(f"Prices:     {prices}")
    print(f"Quantities: {quantities}")
    print()
    
    lengths = [len(products), len(prices), len(quantities)]
    if len(set(lengths)) == 1:
        print(f"✅ All lists have the same length: {lengths[0]} items")
    else:
        print(f"⚠️  Warning: Lists have different lengths: {lengths}")
    print()

def create_product_price_pairs():
    """Use zip() to pair each product with its corresponding price"""
    print("=== Task 1: Create Product-Price Pairs ===")
    print()
    
    print("Method 1 - Basic zip() usage:")
    product_price_pairs = list(zip(products, prices))
    print(f"Product-Price pairs: {product_price_pairs}")
    print()
    
    print("Method 2 - Formatted display:")
    for product, price in zip(products, prices):
        print(f"  📦 {product}: ${price:.2f}")
    print()
    
    print("Method 3 - With index numbers:")
    for i, (product, price) in enumerate(zip(products, prices), 1):
        print(f"  {i}. {product}: ${price:.2f}")
    print()
    
    print("Method 4 - Different data structures:")
    
    pairs_list = list(zip(products, prices))
    print(f"  As list of tuples: {pairs_list}")
    
    price_dict = dict(zip(products, prices))
    print(f"  As dictionary: {price_dict}")
    
    unzipped_products, unzipped_prices = zip(*product_price_pairs)
    print(f"  Unzipped products: {list(unzipped_products)}")
    print(f"  Unzipped prices: {list(unzipped_prices)}")
    print()
    
    return product_price_pairs

def calculate_total_values():
    """Calculate the total inventory value for each product using price × quantity"""
    print("=== Task 2: Calculate Total Value for Each Product ===")
    print()
    
    print("Inventory Value Calculation (Price × Quantity):")
    print(f"{'Product':<12} {'Price':<10} {'Quantity':<10} {'Total Value'}")
    print("-" * 50)
    
    total_inventory_value = 0
    product_values = []
    
    for product, price, quantity in zip(products, prices, quantities):
        total_value = price * quantity
        total_inventory_value += total_value
        product_values.append((product, total_value))
        
        print(f"{product:<12} ${price:<9.2f} {quantity:<10} ${total_value:<10.2f}")
    
    print("-" * 50)
    print(f"{'TOTAL':<32} ${total_inventory_value:<10.2f}")
    print()
    
    print("Value Analysis:")
    
    max_value_product = max(product_values, key=lambda x: x[1])
    min_value_product = min(product_values, key=lambda x: x[1])
    
    print(f"  💰 Highest value: {max_value_product[0]} (${max_value_product[1]:.2f})")
    print(f"  💸 Lowest value: {min_value_product[0]} (${min_value_product[1]:.2f})")
    
    avg_value = total_inventory_value / len(product_values)
    print(f"  📊 Average value per product: ${avg_value:.2f}")
    print()
    
    print("Products ranked by total value:")
    sorted_by_value = sorted(product_values, key=lambda x: x[1], reverse=True)
    for rank, (product, value) in enumerate(sorted_by_value, 1):
        print(f"  {rank}. {product}: ${value:.2f}")
    print()
    
    return product_values, total_inventory_value

def build_product_catalog():
    """Create a comprehensive product catalog dictionary"""
    print("=== Task 3: Build a Product Catalog Dictionary ===")
    print()
    
    print("Method 1 - Dictionary comprehension with zip():")
    catalog = {
        product: {"price": price, "quantity": quantity}
        for product, price, quantity in zip(products, prices, quantities)
    }
    
    print("Product Catalog:")
    for product, details in catalog.items():
        print(f"  {product}:")
        print(f"    Price: ${details['price']:.2f}")
        print(f"    Quantity: {details['quantity']}")
        print(f"    Total Value: ${details['price'] * details['quantity']:.2f}")
    print()
    
    print("Method 2 - Manual construction:")
    catalog_manual = {}
    for product, price, quantity in zip(products, prices, quantities):
        catalog_manual[product] = {
            "price": price,
            "quantity": quantity,
            "total_value": price * quantity
        }
    
    print("Enhanced catalog with calculated total values:")
    for product, details in catalog_manual.items():
        print(f"  📦 {product}: ${details['price']:.2f} × {details['quantity']} = ${details['total_value']:.2f}")
    print()
    
    print("Method 3 - Extended catalog with analytics:")
    
    def get_category(price):
        if price >= 500:
            return "Premium"
        elif price >= 100:
            return "Mid-range"
        else:
            return "Budget"
    
    def get_stock_status(quantity):
        if quantity >= 15:
            return "Well Stocked"
        elif quantity >= 10:
            return "Adequate"
        elif quantity >= 5:
            return "Low Stock"
        else:
            return "Critical Stock"
    
    extended_catalog = {}
    for product, price, quantity in zip(products, prices, quantities):
        extended_catalog[product] = {
            "price": price,
            "quantity": quantity,
            "total_value": price * quantity,
            "category": get_category(price),
            "stock_status": get_stock_status(quantity),
            "per_unit_value": price,
            "reorder_needed": quantity < 10
        }
    
    print("Extended Product Catalog:")
    print(f"{'Product':<12} {'Price':<8} {'Qty':<5} {'Category':<10} {'Stock Status':<15} {'Reorder?'}")
    print("-" * 75)
    
    for product, details in extended_catalog.items():
        reorder = "Yes" if details['reorder_needed'] else "No"
        print(f"{product:<12} ${details['price']:<7.2f} {details['quantity']:<5} "
              f"{details['category']:<10} {details['stock_status']:<15} {reorder}")
    
    print()
    return catalog, extended_catalog

def find_low_stock_products():
    """Identify and print products with quantity less than 10"""
    print("=== Task 4: Find Low Stock Products ===")
    print()
    
    low_stock_threshold = 10
    print(f"Finding products with quantity < {low_stock_threshold}:")
    print()
    
    low_stock_products = []
    for product, price, quantity in zip(products, prices, quantities):
        if quantity < low_stock_threshold:
            low_stock_products.append((product, quantity, price))
    
    if low_stock_products:
        print(f"⚠️  Found {len(low_stock_products)} low stock product(s):")
        print(f"{'Product':<12} {'Quantity':<10} {'Price':<10} {'Value at Risk'}")
        print("-" * 50)
        
        total_at_risk = 0
        for product, quantity, price in low_stock_products:
            value_at_risk = price * quantity
            total_at_risk += value_at_risk
            print(f"{product:<12} {quantity:<10} ${price:<9.2f} ${value_at_risk:.2f}")
        
        print("-" * 50)
        print(f"Total value at risk: ${total_at_risk:.2f}")
        print()
        
        print("📋 Restock Recommendations:")
        for product, quantity, price in low_stock_products:
            recommended_order = max(20 - quantity, 10)  # Bring to at least 20, minimum order 10
            order_cost = price * recommended_order
            print(f"  • {product}: Order {recommended_order} units (Cost: ${order_cost:.2f})")
    else:
        print("✅ All products are well stocked (quantity >= 10)")
    
    print()
    
    print("Complete Stock Analysis:")
    stock_categories = {
        "Critical (< 5)": [],
        "Low (5-9)": [],
        "Adequate (10-14)": [],
        "Well Stocked (15+)": []
    }
    
    for product, price, quantity in zip(products, prices, quantities):
        if quantity < 5:
            stock_categories["Critical (< 5)"].append((product, quantity))
        elif quantity < 10:
            stock_categories["Low (5-9)"].append((product, quantity))
        elif quantity < 15:
            stock_categories["Adequate (10-14)"].append((product, quantity))
        else:
            stock_categories["Well Stocked (15+)"].append((product, quantity))
    
    for category, items in stock_categories.items():
        print(f"  {category}: {len(items)} products")
        for product, quantity in items:
            print(f"    - {product}: {quantity} units")
    
    print()
    return low_stock_products

def advanced_zip_operations():
    """Demonstrate advanced zip() operations and techniques"""
    print("=== Advanced zip() Operations ===")
    print()
    
    print("1. Handling Different Length Lists:")
    short_list = ["A", "B"]
    long_list = [1, 2, 3, 4, 5]
    
    print(f"  Short list: {short_list}")
    print(f"  Long list: {long_list}")
    print(f"  zip() result: {list(zip(short_list, long_list))}")
    print("  Note: zip() stops at the shortest list")
    print()
    
    from itertools import zip_longest
    print("2. Using itertools.zip_longest:")
    result_longest = list(zip_longest(short_list, long_list, fillvalue="N/A"))
    print(f"  zip_longest result: {result_longest}")
    print("  Note: zip_longest continues to the longest list")
    print()
    
    print("3. Unzipping Data:")
    paired_data = list(zip(products, prices, quantities))
    print(f"  Original paired data: {paired_data[:2]}...")  # Show first 2
    
    unzipped_products, unzipped_prices, unzipped_quantities = zip(*paired_data)
    print(f"  Unzipped products: {list(unzipped_products)}")
    print(f"  Unzipped prices: {list(unzipped_prices)}")
    print(f"  Unzipped quantities: {list(unzipped_quantities)}")
    print()
    
    print("4. Multiple List Processing:")
    
    costs = [price * 0.6 for price in prices]
    profits = [price - cost for price, cost in zip(prices, costs)]
    
    print("Profit Analysis:")
    print(f"{'Product':<12} {'Price':<8} {'Cost':<8} {'Profit':<8} {'Margin %'}")
    print("-" * 55)
    
    for product, price, cost, profit in zip(products, prices, costs, profits):
        margin_percent = (profit / price) * 100
        print(f"{product:<12} ${price:<7.2f} ${cost:<7.2f} ${profit:<7.2f} {margin_percent:<7.1f}%")
    print()
    
    print("5. Conditional Processing with zip():")
    
    premium_items = [(product, price, quantity) 
                    for product, price, quantity in zip(products, prices, quantities)
                    if price > 100]
    
    print("Premium items (price > $100):")
    for product, price, quantity in premium_items:
        print(f"  {product}: ${price:.2f} (Qty: {quantity})")
    print()

def practical_applications():
    """Show practical applications of zip() in real scenarios"""
    print("=== Practical Applications ===")
    print()
    
    print("1. Sales Reporting Simulation:")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    laptop_sales = [2, 1, 3, 2, 4, 5, 3]
    mouse_sales = [8, 6, 10, 7, 12, 15, 9]
    
    print("Weekly Sales Report:")
    print(f"{'Day':<12} {'Laptops':<8} {'Mice':<8} {'Total Units'}")
    print("-" * 40)
    
    weekly_total = 0
    for day, laptops, mice in zip(days, laptop_sales, mouse_sales):
        daily_total = laptops + mice
        weekly_total += daily_total
        print(f"{day:<12} {laptops:<8} {mice:<8} {daily_total}")
    
    print("-" * 40)
    print(f"{'TOTAL':<12} {sum(laptop_sales):<8} {sum(mouse_sales):<8} {weekly_total}")
    print()
    
    print("2. Price Comparison Analysis:")
    
    competitor_prices = [949.99, 29.99, 79.99, 279.99]
    
    print("Price Comparison with Competitors:")
    print(f"{'Product':<12} {'Our Price':<10} {'Competitor':<12} {'Difference':<12} {'Status'}")
    print("-" * 65)
    
    for product, our_price, comp_price in zip(products, prices, competitor_prices):
        difference = our_price - comp_price
        status = "Higher" if difference > 0 else "Lower" if difference < 0 else "Same"
        print(f"{product:<12} ${our_price:<9.2f} ${comp_price:<11.2f} ${difference:<+11.2f} {status}")
    print()
    
    print("3. Inventory Tracking Over Time:")
    
    initial_stock = quantities.copy()
    sales_this_week = [2, 5, 3, 1]
    restocks = [0, 10, 0, 5]
    
    print("Inventory Changes This Week:")
    print(f"{'Product':<12} {'Initial':<8} {'Sales':<8} {'Restock':<8} {'Final':<8} {'Change'}")
    print("-" * 60)
    
    for product, initial, sales, restock in zip(products, initial_stock, sales_this_week, restocks):
        final_stock = initial - sales + restock
        change = final_stock - initial
        change_str = f"{change:+d}"
        print(f"{product:<12} {initial:<8} {sales:<8} {restock:<8} {final_stock:<8} {change_str}")
    print()

def main():
    print("🔗 DATA PAIRING WITH ZIP() 🔗")
    print("=" * 60)
    print()
    
    display_initial_data()
    
    print("Executing Required Tasks:")
    print()
    
    product_price_pairs = create_product_price_pairs()
    
    product_values, total_inventory_value = calculate_total_values()
    
    catalog, extended_catalog = build_product_catalog()
    
    low_stock_products = find_low_stock_products()
    
    advanced_zip_operations()
    practical_applications()
    
    print("=== Summary & Key Concepts ===")
    print()
    print("✅ Completed Tasks:")
    print("   1. ✅ Created product-price pairs using zip()")
    print("   2. ✅ Calculated total inventory values")
    print("   3. ✅ Built comprehensive product catalog dictionary")
    print("   4. ✅ Identified low stock products")
    print()
    print("🔧 zip() Functions Demonstrated:")
    print("   • Basic pairing of parallel lists")
    print("   • Multi-list processing (3+ lists)")
    print("   • Dictionary creation from lists")
    print("   • Data unpacking and restructuring")
    print("   • Conditional processing with zip()")
    print("   • zip_longest for different length lists")
    print()
    print("📊 Key Results:")
    print(f"   • Total inventory value: ${total_inventory_value:.2f}")
    print(f"   • Products tracked: {len(products)}")
    print(f"   • Low stock alerts: {len(low_stock_products)}")
    print(f"   • Catalog entries: {len(catalog)}")
    print()
    print("💡 zip() Benefits:")
    print("   • Elegant parallel list processing")
    print("   • Reduces complex indexing")
    print("   • Memory efficient iteration")
    print("   • Natural data pairing")
    print("   • Pythonic and readable code")
    print()

if __name__ == "__main__":
    main()

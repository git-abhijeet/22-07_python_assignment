# Simple Shopping Calculator
# This program calculates subtotal, tax, and total for three items

def main():
    """Main function to calculate shopping totals with tax"""
    
    print("=== Simple Shopping Calculator ===")
    print()
    
    # Initialize variables
    items = []  # Store item details for receipt
    tax_rate = 0.085  # 8.5% tax rate
    
    # Collect information for 3 items
    for i in range(1, 4):
        price = float(input(f"Enter price of item {i}: "))
        quantity = int(input(f"Enter quantity of item {i}: "))
        
        # Calculate item total and store details
        item_total = price * quantity
        items.append({
            'price': price,
            'quantity': quantity,
            'total': item_total
        })
    
    # Calculate subtotal
    subtotal = sum(item['total'] for item in items)
    
    # Calculate tax and final total
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    
    # Display itemized receipt
    print()
    print("=== Receipt ===")
    
    # Display each item
    for i, item in enumerate(items, 1):
        price = item['price']
        quantity = item['quantity']
        item_total = item['total']
        print(f"Item {i}: {price:.0f} x {quantity} = {item_total:.0f}")
    
    # Display totals
    print(f"Subtotal: {subtotal:.0f}")
    print(f"Tax (8.5%): {tax_amount:.2f}")
    print(f"Total: {total:.2f}")

if __name__ == "__main__":
    main()
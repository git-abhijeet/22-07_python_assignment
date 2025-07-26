
def main():
    """Main function to calculate shopping totals with tax"""
    
    print("=== Simple Shopping Calculator ===")
    print()
    
    items = []  # Store item details for receipt
    tax_rate = 0.085  # 8.5% tax rate
    
    for i in range(1, 4):
        price = float(input(f"Enter price of item {i}: "))
        quantity = int(input(f"Enter quantity of item {i}: "))
        
        item_total = price * quantity
        items.append({
            'price': price,
            'quantity': quantity,
            'total': item_total
        })
    
    subtotal = sum(item['total'] for item in items)
    
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    
    print()
    print("=== Receipt ===")
    
    for i, item in enumerate(items, 1):
        price = item['price']
        quantity = item['quantity']
        item_total = item['total']
        print(f"Item {i}: {price:.0f} x {quantity} = {item_total:.0f}")
    
    print(f"Subtotal: {subtotal:.0f}")
    print(f"Tax (8.5%): {tax_amount:.2f}")
    print(f"Total: {total:.2f}")

if __name__ == "__main__":
    main()
class ShoppingCartManager:
    """A comprehensive shopping cart management system"""
    
    def __init__(self):
        self.cart = []
        self.history = []  # Track all operations for history
    
    def add_item(self, item):
        """Add an item to the cart"""
        if item:
            self.cart.append(item)
            self.history.append(f"Added '{item}' to cart")
            print(f"✅ Added '{item}' to your cart")
        else:
            print("❌ Cannot add empty item")
    
    def remove_specific_item(self, item):
        """Remove a user-specified item if it exists in the cart"""
        if item in self.cart:
            self.cart.remove(item)
            self.history.append(f"Removed '{item}' from cart")
            print(f"✅ Removed '{item}' from your cart")
            return True
        else:
            print(f"❌ '{item}' not found in cart")
            return False
    
    def remove_last_item(self):
        """Remove the most recently added item using pop()"""
        if self.cart:
            removed_item = self.cart.pop()
            self.history.append(f"Removed last item '{removed_item}' from cart")
            print(f"✅ Removed last item '{removed_item}' from your cart")
            return removed_item
        else:
            print("❌ Cart is empty, nothing to remove")
            return None
    
    def display_sorted_items(self):
        """Display all items in alphabetical order"""
        if self.cart:
            sorted_items = sorted(self.cart)
            print("📋 Items in alphabetical order:")
            for item in sorted_items:
                print(f"   • {item}")
        else:
            print("📋 Cart is empty")
    
    def display_cart_with_indices(self):
        """Display current cart contents with index numbers"""
        if self.cart:
            print("🛒 Current cart contents:")
            for index, item in enumerate(self.cart):
                print(f"   {index}: {item}")
        else:
            print("🛒 Cart is empty")
    
    def display_cart_info(self):
        """Display comprehensive cart information"""
        print(f"\n📊 Cart Summary:")
        print(f"   Total items: {len(self.cart)}")
        if self.cart:
            print(f"   Items: {', '.join(self.cart)}")
            unique_items = len(set(self.cart))
            print(f"   Unique items: {unique_items}")
            if unique_items != len(self.cart):
                duplicates = len(self.cart) - unique_items
                print(f"   Duplicates: {duplicates}")
        print()
    
    def get_cart_copy(self):
        """Return a copy of the current cart"""
        return self.cart.copy()
    
    def clear_cart(self):
        """Clear all items from the cart"""
        if self.cart:
            cleared_count = len(self.cart)
            self.cart.clear()
            self.history.append(f"Cleared cart ({cleared_count} items)")
            print(f"✅ Cleared cart ({cleared_count} items removed)")
        else:
            print("❌ Cart is already empty")
    
    def count_item(self, item):
        """Count how many times an item appears in the cart"""
        count = self.cart.count(item)
        if count > 0:
            print(f"📊 '{item}' appears {count} time(s) in your cart")
        else:
            print(f"📊 '{item}' is not in your cart")
        return count
    
    def get_history(self):
        """Display the history of all operations"""
        if self.history:
            print("📜 Operation History:")
            for i, operation in enumerate(self.history, 1):
                print(f"   {i}. {operation}")
        else:
            print("📜 No operations performed yet")
    
    def search_items(self, search_term):
        """Search for items containing the search term"""
        found_items = [item for item in self.cart if search_term.lower() in item.lower()]
        if found_items:
            print(f"🔍 Found {len(found_items)} item(s) containing '{search_term}':")
            for item in found_items:
                print(f"   • {item}")
        else:
            print(f"🔍 No items found containing '{search_term}'")
        return found_items

def demonstrate_sample_operations():
    """Demonstrate the sample operations requested"""
    print("🛒 SHOPPING CART MANAGER - SAMPLE OPERATIONS 🛒")
    print("=" * 60)
    print()
    
    cart_manager = ShoppingCartManager()
    
    print("1. Starting with an empty cart")
    cart_manager.display_cart_with_indices()
    print()
    
    print("2. Adding items: 'apples', 'bread', 'milk', 'eggs'")
    items_to_add = ["apples", "bread", "milk", "eggs"]
    for item in items_to_add:
        cart_manager.add_item(item)
    
    print("\nCurrent cart after adding items:")
    cart_manager.display_cart_with_indices()
    cart_manager.display_cart_info()
    
    print("3. Removing 'bread'")
    cart_manager.remove_specific_item("bread")
    
    print("\nCart after removing 'bread':")
    cart_manager.display_cart_with_indices()
    print()
    
    print("4. Removing the last added item")
    cart_manager.remove_last_item()
    
    print("\nCart after removing last item:")
    cart_manager.display_cart_with_indices()
    print()
    
    print("5. Displaying items in alphabetical order")
    cart_manager.display_sorted_items()
    print()
    
    print("6. Final cart contents with index numbers:")
    cart_manager.display_cart_with_indices()
    cart_manager.display_cart_info()
    
    return cart_manager

def interactive_cart_manager():
    """Interactive shopping cart manager"""
    print("\n🛒 INTERACTIVE SHOPPING CART MANAGER 🛒")
    print("=" * 60)
    
    cart_manager = ShoppingCartManager()
    
    while True:
        print("\nAvailable Operations:")
        print("1. Add item")
        print("2. Remove specific item")
        print("3. Remove last item")
        print("4. Display items alphabetically")
        print("5. Display cart with indices")
        print("6. Display cart summary")
        print("7. Count specific item")
        print("8. Search items")
        print("9. Clear cart")
        print("10. View operation history")
        print("11. Exit")
        
        try:
            choice = input("\nEnter your choice (1-11): ").strip()
            
            if choice == "1":
                item = input("Enter item to add: ").strip()
                cart_manager.add_item(item)
            
            elif choice == "2":
                if not cart_manager.cart:
                    print("❌ Cart is empty")
                else:
                    print("Current items:", ", ".join(cart_manager.cart))
                    item = input("Enter item to remove: ").strip()
                    cart_manager.remove_specific_item(item)
            
            elif choice == "3":
                cart_manager.remove_last_item()
            
            elif choice == "4":
                cart_manager.display_sorted_items()
            
            elif choice == "5":
                cart_manager.display_cart_with_indices()
            
            elif choice == "6":
                cart_manager.display_cart_info()
            
            elif choice == "7":
                if not cart_manager.cart:
                    print("❌ Cart is empty")
                else:
                    item = input("Enter item to count: ").strip()
                    cart_manager.count_item(item)
            
            elif choice == "8":
                if not cart_manager.cart:
                    print("❌ Cart is empty")
                else:
                    search_term = input("Enter search term: ").strip()
                    cart_manager.search_items(search_term)
            
            elif choice == "9":
                cart_manager.clear_cart()
            
            elif choice == "10":
                cart_manager.get_history()
            
            elif choice == "11":
                print("👋 Thank you for using Shopping Cart Manager!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-11.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def advanced_cart_operations():
    """Demonstrate advanced cart operations"""
    print("\n🔧 ADVANCED CART OPERATIONS 🔧")
    print("=" * 60)
    
    cart_manager = ShoppingCartManager()
    
    print("1. Adding items with duplicates:")
    items = ["apples", "bananas", "apples", "oranges", "bananas", "grapes", "apples"]
    for item in items:
        cart_manager.add_item(item)
    
    cart_manager.display_cart_with_indices()
    cart_manager.display_cart_info()
    
    print("2. Counting specific items:")
    cart_manager.count_item("apples")
    cart_manager.count_item("bananas")
    cart_manager.count_item("watermelon")
    print()
    
    print("3. Search functionality:")
    cart_manager.search_items("apple")
    cart_manager.search_items("grape")
    cart_manager.search_items("berry")
    print()
    
    print("4. Remove operations:")
    print("Removing one 'apples':")
    cart_manager.remove_specific_item("apples")
    cart_manager.display_cart_with_indices()
    
    print("\nRemoving last item:")
    cart_manager.remove_last_item()
    cart_manager.display_cart_with_indices()
    print()
    
    print("5. Final sorted display:")
    cart_manager.display_sorted_items()
    
    print("\n6. Operation history:")
    cart_manager.get_history()
    
    return cart_manager

def cart_comparison_demo():
    """Demonstrate cart comparison and manipulation"""
    print("\n📊 CART COMPARISON & MANIPULATION 📊")
    print("=" * 60)
    
    cart1 = ShoppingCartManager()
    cart2 = ShoppingCartManager()
    
    print("Creating two different carts:")
    
    print("\nCart 1 - Grocery items:")
    grocery_items = ["milk", "bread", "eggs", "butter", "cheese"]
    for item in grocery_items:
        cart1.add_item(item)
    cart1.display_cart_with_indices()
    
    print("\nCart 2 - Fruit items:")
    fruit_items = ["apples", "bananas", "oranges", "grapes"]
    for item in fruit_items:
        cart2.add_item(item)
    cart2.display_cart_with_indices()
    
    print("\nCart comparison:")
    cart1_items = set(cart1.get_cart_copy())
    cart2_items = set(cart2.get_cart_copy())
    
    common_items = cart1_items & cart2_items
    cart1_only = cart1_items - cart2_items
    cart2_only = cart2_items - cart1_items
    
    print(f"   Items in both carts: {list(common_items) if common_items else 'None'}")
    print(f"   Items only in Cart 1: {list(cart1_only)}")
    print(f"   Items only in Cart 2: {list(cart2_only)}")
    
    print("\nMerging carts (Cart 1 + Cart 2):")
    merged_cart = ShoppingCartManager()
    all_items = cart1.get_cart_copy() + cart2.get_cart_copy()
    for item in all_items:
        merged_cart.add_item(item)
    
    merged_cart.display_cart_with_indices()
    merged_cart.display_sorted_items()
    merged_cart.display_cart_info()

def performance_testing():
    """Test performance with large cart operations"""
    print("\n⚡ PERFORMANCE TESTING ⚡")
    print("=" * 60)
    
    import time
    
    cart_manager = ShoppingCartManager()
    
    print("Testing performance with 1000 items...")
    start_time = time.time()
    
    for i in range(1000):
        cart_manager.add_item(f"item_{i:04d}")
    
    add_time = time.time() - start_time
    print(f"✅ Added 1000 items in {add_time:.4f} seconds")
    
    start_time = time.time()
    search_results = cart_manager.search_items("item_05")
    search_time = time.time() - start_time
    print(f"✅ Search completed in {search_time:.4f} seconds, found {len(search_results)} items")
    
    start_time = time.time()
    cart_manager.display_sorted_items()
    sort_time = time.time() - start_time
    print(f"✅ Sorted 1000 items in {sort_time:.4f} seconds")
    
    start_time = time.time()
    for _ in range(100):
        cart_manager.remove_last_item()
    remove_time = time.time() - start_time
    print(f"✅ Removed 100 items in {remove_time:.4f} seconds")
    
    print(f"\nFinal cart size: {len(cart_manager.cart)} items")

def main():
    """Main function to demonstrate all shopping cart functionality"""
    print("🛒 SHOPPING CART MANAGER SYSTEM 🛒")
    print("=" * 70)
    print()
    
    sample_cart = demonstrate_sample_operations()
    
    advanced_cart = advanced_cart_operations()
    
    cart_comparison_demo()
    
    performance_testing()
    
    print("\n" + "="*70)
    print("💡 INTERACTIVE MODE AVAILABLE")
    print("="*70)
    print("To run interactive mode, uncomment the line below in main()")
    print("Interactive mode allows you to manually manage your cart!")
    
    print("\n" + "="*70)
    print("📋 SUMMARY & FEATURES")
    print("="*70)
    print()
    print("✅ Core Features Implemented:")
    print("   • Add items to cart")
    print("   • Remove specific items")
    print("   • Remove last added item")
    print("   • Display items alphabetically")
    print("   • Display cart with indices")
    print()
    print("🚀 Advanced Features:")
    print("   • Item counting and search")
    print("   • Operation history tracking")
    print("   • Cart comparison and merging")
    print("   • Performance testing")
    print("   • Interactive management mode")
    print("   • Comprehensive error handling")
    print()
    print("🎯 Sample Operations Completed:")
    print("   1. ✅ Started with empty cart")
    print("   2. ✅ Added: apples, bread, milk, eggs")
    print("   3. ✅ Removed: bread")
    print("   4. ✅ Removed last item (eggs)")
    print("   5. ✅ Displayed items alphabetically")
    print("   6. ✅ Showed final cart with indices")
    print()

if __name__ == "__main__":
    main()

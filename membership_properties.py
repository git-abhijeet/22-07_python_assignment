fruits_list = ["apple", "banana", "orange", "apple", "grape"]
fruits_tuple = ("apple", "banana", "orange")
fruits_set = {"apple", "banana", "orange", "grape"}
fruits_dict = {"apple": 5, "banana": 3, "orange": 8, "grape": 2}

def check_membership():
    """Test whether 'apple' is present in each data structure"""
    print("=== Task 1: Check for Membership ===")
    print("Testing if 'apple' is present in each data structure:")
    print()
    
    apple_in_list = "apple" in fruits_list
    print(f"'apple' in fruits_list: {apple_in_list}")
    print(f"   List: {fruits_list}")
    
    apple_in_tuple = "apple" in fruits_tuple
    print(f"'apple' in fruits_tuple: {apple_in_tuple}")
    print(f"   Tuple: {fruits_tuple}")
    
    apple_in_set = "apple" in fruits_set
    print(f"'apple' in fruits_set: {apple_in_set}")
    print(f"   Set: {fruits_set}")
    
    apple_in_dict = "apple" in fruits_dict
    print(f"'apple' in fruits_dict: {apple_in_dict}")
    print(f"   Dict: {fruits_dict}")
    print()
    
    print("Additional membership tests:")
    test_items = ["apple", "mango", "banana", "kiwi"]
    
    for item in test_items:
        print(f"Testing '{item}':")
        print(f"   In list: {item in fruits_list}")
        print(f"   In tuple: {item in fruits_tuple}")
        print(f"   In set: {item in fruits_set}")
        print(f"   In dict (keys): {item in fruits_dict}")
        if item in fruits_dict:
            print(f"   Dict value: {fruits_dict[item]}")
        print()

def find_lengths():
    """Display the number of elements in each structure using len()"""
    print("=== Task 2: Find Length ===")
    print("Number of elements in each data structure:")
    print()
    
    list_length = len(fruits_list)
    tuple_length = len(fruits_tuple)
    set_length = len(fruits_set)
    dict_length = len(fruits_dict)
    
    print(f"len(fruits_list): {list_length}")
    print(f"   Content: {fruits_list}")
    print(f"   Note: Lists can contain duplicates ('apple' appears twice)")
    print()
    
    print(f"len(fruits_tuple): {tuple_length}")
    print(f"   Content: {fruits_tuple}")
    print(f"   Note: Tuples are immutable and can contain duplicates")
    print()
    
    print(f"len(fruits_set): {set_length}")
    print(f"   Content: {fruits_set}")
    print(f"   Note: Sets automatically remove duplicates")
    print()
    
    print(f"len(fruits_dict): {dict_length}")
    print(f"   Content: {fruits_dict}")
    print(f"   Note: Dictionary length is the number of key-value pairs")
    print()
    
    print("Length Comparison Summary:")
    print(f"   List: {list_length} (includes duplicates)")
    print(f"   Tuple: {tuple_length} (no duplicates in this example)")
    print(f"   Set: {set_length} (duplicates automatically removed)")
    print(f"   Dict: {dict_length} (unique keys only)")
    print()

def iterate_and_print():
    """Loop through each structure and print its contents"""
    print("=== Task 3: Iterate and Print Elements ===")
    print()
    
    print("1. Iterating through fruits_list:")
    for index, fruit in enumerate(fruits_list):
        print(f"   Index {index}: {fruit}")
    print()
    
    print("2. Iterating through fruits_tuple:")
    for index, fruit in enumerate(fruits_tuple):
        print(f"   Index {index}: {fruit}")
    print()
    
    print("3. Iterating through fruits_set:")
    print("   Note: Sets are unordered, so iteration order may vary")
    for fruit in fruits_set:
        print(f"   {fruit}")
    print()
    
    print("4. Iterating through fruits_dict:")
    
    print("   a) Keys only:")
    for key in fruits_dict:
        print(f"      {key}")
    
    print("   b) Values only:")
    for value in fruits_dict.values():
        print(f"      {value}")
    
    print("   c) Key-value pairs:")
    for key, value in fruits_dict.items():
        print(f"      {key}: {value}")
    
    print("   d) Keys explicitly:")
    for key in fruits_dict.keys():
        print(f"      Key: {key}")
    print()

def compare_membership_performance():
    """Compare membership testing performance across data structures"""
    print("=== Task 4: Compare Membership Testing Performance ===")
    print()
    
    import time
    
    large_list = list(range(10000)) + ["target"]
    large_tuple = tuple(range(10000)) + ("target",)
    large_set = set(range(10000)) | {"target"}
    large_dict = {i: f"value_{i}" for i in range(10000)}
    large_dict["target"] = "target_value"
    
    test_item = "target"
    iterations = 1000
    
    print(f"Performance test: Finding '{test_item}' in structures with 10,001 elements")
    print(f"Number of iterations: {iterations}")
    print()
    
    start_time = time.time()
    for _ in range(iterations):
        test_item in large_list
    list_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(iterations):
        test_item in large_tuple
    tuple_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(iterations):
        test_item in large_set
    set_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(iterations):
        test_item in large_dict
    dict_time = time.time() - start_time
    
    print("Performance Results:")
    print(f"   List:  {list_time:.6f} seconds (O(n) - linear search)")
    print(f"   Tuple: {tuple_time:.6f} seconds (O(n) - linear search)")
    print(f"   Set:   {set_time:.6f} seconds (O(1) - hash lookup)")
    print(f"   Dict:  {dict_time:.6f} seconds (O(1) - hash lookup)")
    print()
    
    times = [
        ("List", list_time),
        ("Tuple", tuple_time),
        ("Set", set_time),
        ("Dict", dict_time)
    ]
    times.sort(key=lambda x: x[1])
    
    print("Performance Ranking (fastest to slowest):")
    for rank, (data_type, time_taken) in enumerate(times, 1):
        print(f"   {rank}. {data_type}: {time_taken:.6f} seconds")
    print()
    
    print("Explanation:")
    print("• Lists and Tuples: O(n) time complexity")
    print("  - Must check each element sequentially until found")
    print("  - Performance degrades linearly with size")
    print("  - Tuples may be slightly faster due to optimization")
    print()
    print("• Sets and Dictionaries: O(1) average time complexity")
    print("  - Use hash tables for instant lookup")
    print("  - Performance remains constant regardless of size")
    print("  - Best choice for frequent membership testing")
    print()
    print("Recommendation: Use sets or dictionaries for membership testing!")
    print()

def demonstrate_iteration_patterns():
    """Use appropriate iteration patterns for each structure"""
    print("=== Task 5: Demonstrate Different Iteration Patterns ===")
    print()
    
    print("1. List Iteration Patterns:")
    print("   a) Basic iteration:")
    for fruit in fruits_list:
        print(f"      {fruit}")
    
    print("   b) With index using enumerate:")
    for i, fruit in enumerate(fruits_list):
        print(f"      {i}: {fruit}")
    
    print("   c) With index using range:")
    for i in range(len(fruits_list)):
        print(f"      {i}: {fruits_list[i]}")
    
    print("   d) Reverse iteration:")
    for fruit in reversed(fruits_list):
        print(f"      {fruit}")
    print()
    
    print("2. Tuple Iteration Patterns:")
    print("   a) Basic iteration:")
    for fruit in fruits_tuple:
        print(f"      {fruit}")
    
    print("   b) Unpacking (if known length):")
    fruit1, fruit2, fruit3 = fruits_tuple
    print(f"      First: {fruit1}, Second: {fruit2}, Third: {fruit3}")
    
    print("   c) With enumerate:")
    for i, fruit in enumerate(fruits_tuple):
        print(f"      Position {i}: {fruit}")
    print()
    
    print("3. Set Iteration Patterns:")
    print("   a) Basic iteration (unordered):")
    for fruit in fruits_set:
        print(f"      {fruit}")
    
    print("   b) Sorted iteration:")
    for fruit in sorted(fruits_set):
        print(f"      {fruit}")
    
    print("   c) Conditional iteration:")
    for fruit in fruits_set:
        if len(fruit) > 5:
            print(f"      Long name: {fruit}")
    print()
    
    print("4. Dictionary Iteration Patterns:")
    print("   a) Keys only (default):")
    for key in fruits_dict:
        print(f"      {key}")
    
    print("   b) Values only:")
    for value in fruits_dict.values():
        print(f"      {value}")
    
    print("   c) Key-value pairs:")
    for key, value in fruits_dict.items():
        print(f"      {key}: {value}")
    
    print("   d) Keys explicitly:")
    for key in fruits_dict.keys():
        print(f"      Key: {key}")
    
    print("   e) Sorted by keys:")
    for key in sorted(fruits_dict.keys()):
        print(f"      {key}: {fruits_dict[key]}")
    
    print("   f) Sorted by values:")
    for key, value in sorted(fruits_dict.items(), key=lambda x: x[1]):
        print(f"      {key}: {value}")
    
    print("   g) Filtered iteration:")
    for key, value in fruits_dict.items():
        if value > 5:
            print(f"      High count: {key} = {value}")
    print()

def advanced_membership_operations():
    """Demonstrate advanced membership operations"""
    print("=== Advanced Membership Operations ===")
    print()
    
    print("1. Set Operations:")
    tropical_fruits = {"mango", "pineapple", "banana", "orange"}
    print(f"   Our fruits: {fruits_set}")
    print(f"   Tropical fruits: {tropical_fruits}")
    
    common = fruits_set & tropical_fruits
    print(f"   Common fruits: {common}")
    
    all_fruits = fruits_set | tropical_fruits
    print(f"   All fruits: {all_fruits}")
    
    only_ours = fruits_set - tropical_fruits
    print(f"   Only in our set: {only_ours}")
    
    exclusive = fruits_set ^ tropical_fruits
    print(f"   Exclusive to each: {exclusive}")
    print()
    
    print("2. Dictionary Membership Variations:")
    print(f"   Dict: {fruits_dict}")
    
    print(f"   'apple' in keys: {'apple' in fruits_dict}")
    print(f"   'mango' in keys: {'mango' in fruits_dict}")
    
    print(f"   5 in values: {5 in fruits_dict.values()}")
    print(f"   10 in values: {10 in fruits_dict.values()}")
    
    print(f"   ('apple', 5) in items: {('apple', 5) in fruits_dict.items()}")
    print(f"   ('apple', 10) in items: {('apple', 10) in fruits_dict.items()}")
    print()
    
    print("3. List Comprehensions with Membership:")
    
    available_fruits = [fruit for fruit in ["apple", "mango", "banana", "kiwi"] if fruit in fruits_set]
    print(f"   Available from wishlist: {available_fruits}")
    
    high_count_fruits = [fruit for fruit, count in fruits_dict.items() if count > 4]
    print(f"   High count fruits: {high_count_fruits}")
    
    test_fruits = ["apple", "mango", "grape", "kiwi"]
    membership_results = [fruit in fruits_set for fruit in test_fruits]
    print(f"   Membership test results: {list(zip(test_fruits, membership_results))}")
    print()

def practical_applications():
    """Show practical applications of membership testing"""
    print("=== Practical Applications ===")
    print()
    
    print("1. User Permission System:")
    admin_users = {"alice", "bob"}
    regular_users = {"charlie", "diana", "eve"}
    current_user = "alice"
    
    if current_user in admin_users:
        print(f"   {current_user} has admin access")
    elif current_user in regular_users:
        print(f"   {current_user} has regular access")
    else:
        print(f"   {current_user} access denied")
    print()
    
    print("2. Inventory Management:")
    inventory = fruits_dict.copy()
    orders = [("apple", 2), ("banana", 1), ("mango", 3)]
    
    for item, quantity in orders:
        if item in inventory:
            if inventory[item] >= quantity:
                inventory[item] -= quantity
                print(f"   Order fulfilled: {quantity} {item}")
            else:
                print(f"   Insufficient stock: {item} (need {quantity}, have {inventory[item]})")
        else:
            print(f"   Item not in inventory: {item}")
    
    print(f"   Updated inventory: {inventory}")
    print()
    
    print("3. Configuration Validation:")
    required_settings = {"database_url", "api_key", "debug_mode"}
    user_config = {"database_url": "localhost", "api_key": "secret", "theme": "dark"}
    
    missing_settings = required_settings - set(user_config.keys())
    if missing_settings:
        print(f"   Missing required settings: {missing_settings}")
    else:
        print("   All required settings present")
    
    extra_settings = set(user_config.keys()) - required_settings
    if extra_settings:
        print(f"   Extra settings found: {extra_settings}")
    print()

def main():
    print("🍎 MEMBERSHIP PROPERTIES & PERFORMANCE 🍎")
    print("=" * 60)
    print()
    
    print("Initial Data Structures:")
    print(f"fruits_list = {fruits_list}")
    print(f"fruits_tuple = {fruits_tuple}")
    print(f"fruits_set = {fruits_set}")
    print(f"fruits_dict = {fruits_dict}")
    print()
    
    check_membership()
    find_lengths()
    iterate_and_print()
    compare_membership_performance()
    demonstrate_iteration_patterns()
    advanced_membership_operations()
    practical_applications()
    
    print("=== Summary & Best Practices ===")
    print()
    print("Key Takeaways:")
    print("1. Membership Testing Performance:")
    print("   • Sets & Dictionaries: O(1) - Use for frequent lookups")
    print("   • Lists & Tuples: O(n) - Avoid for large datasets")
    print()
    print("2. When to Use Each Structure:")
    print("   • List: Ordered, mutable, allows duplicates")
    print("   • Tuple: Ordered, immutable, allows duplicates")
    print("   • Set: Unordered, mutable, unique elements only")
    print("   • Dict: Key-value pairs, fast lookups, unique keys")
    print()
    print("3. Iteration Best Practices:")
    print("   • Use enumerate() when you need indices")
    print("   • Use .items() for dictionaries when you need both key and value")
    print("   • Use sorted() when you need ordered iteration of sets")
    print("   • Consider list comprehensions for filtering during iteration")
    print()

if __name__ == "__main__":
    main()

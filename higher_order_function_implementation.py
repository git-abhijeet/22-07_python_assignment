def demonstrate_basic_examples():
    
    print("=== Basic Examples from Requirements ===")
    
    def custom_map(func, iterable):
        return [func(x) for x in iterable]
    
    def custom_filter(func, iterable):
        return [x for x in iterable if func(x)]
    
    def custom_reduce(func, iterable):
        result = iterable[0]
        for x in iterable[1:]:
            result = func(result, x)
        return result
    
    print("1. Custom Map Function:")
    print("   def custom_map(func, iterable):")
    print("       return [func(x) for x in iterable]")
    print()
    result1 = custom_map(lambda x: x * 2, [1, 2, 3])
    print(f"   custom_map(lambda x: x * 2, [1, 2, 3]) = {result1}")
    print()
    
    print("2. Custom Filter Function:")
    print("   def custom_filter(func, iterable):")
    print("       return [x for x in iterable if func(x)]")
    print()
    result2 = custom_filter(lambda x: x % 2 == 0, [1, 2, 3, 4])
    print(f"   custom_filter(lambda x: x % 2 == 0, [1, 2, 3, 4]) = {result2}")
    print()
    
    print("3. Custom Reduce Function:")
    print("   def custom_reduce(func, iterable):")
    print("       result = iterable[0]")
    print("       for x in iterable[1:]:")
    print("           result = func(result, x)")
    print("       return result")
    print()
    result3 = custom_reduce(lambda x, y: x + y, [1, 2, 3, 4])
    print(f"   custom_reduce(lambda x, y: x + y, [1, 2, 3, 4]) = {result3}")
    print()

def implement_enhanced_functions():
    
    print("=== Enhanced Higher-Order Functions ===")
    
    def enhanced_map(func, *iterables):
        if len(iterables) == 1:
            return [func(x) for x in iterables[0]]
        else:
            min_length = min(len(iterable) for iterable in iterables)
            return [func(*args) for args in zip(*iterables)]
    
    def enhanced_filter(func, iterable):
        if func is None:
            return [x for x in iterable if x]
        return [x for x in iterable if func(x)]
    
    def enhanced_reduce(func, iterable, initializer=None):
        if not iterable and initializer is None:
            raise TypeError("reduce() of empty sequence with no initial value")
        
        if initializer is not None:
            result = initializer
            start_index = 0
        else:
            result = iterable[0]
            start_index = 1
        
        for x in iterable[start_index:]:
            result = func(result, x)
        return result
    
    print("1. Enhanced Map (multiple iterables):")
    print("   enhanced_map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6])")
    result1 = enhanced_map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6])
    print(f"   Result: {result1}")
    print()
    
    print("2. Enhanced Filter (None handling):")
    print("   enhanced_filter(None, [0, 1, '', 'hello', False, True])")
    result2 = enhanced_filter(None, [0, 1, '', 'hello', False, True])
    print(f"   Result: {result2}")
    print()
    
    print("3. Enhanced Reduce (with initializer):")
    print("   enhanced_reduce(lambda x, y: x * y, [1, 2, 3, 4], 10)")
    result3 = enhanced_reduce(lambda x, y: x * y, [1, 2, 3, 4], 10)
    print(f"   Result: {result3}")
    print()

def implement_generator_versions():
    
    print("=== Generator-Based Implementations ===")
    
    def generator_map(func, iterable):
        for item in iterable:
            yield func(item)
    
    def generator_filter(func, iterable):
        for item in iterable:
            if func is None:
                if item:
                    yield item
            elif func(item):
                yield item
    
    def generator_reduce(func, iterable, initializer=None):
        iterator = iter(iterable)
        
        if initializer is None:
            try:
                result = next(iterator)
            except StopIteration:
                raise TypeError("reduce() of empty sequence with no initial value")
        else:
            result = initializer
        
        for item in iterator:
            result = func(result, item)
        return result
    
    print("1. Generator Map:")
    print("   generator_map(lambda x: x ** 2, range(5))")
    result1 = list(generator_map(lambda x: x ** 2, range(5)))
    print(f"   Result: {result1}")
    print()
    
    print("2. Generator Filter:")
    print("   generator_filter(lambda x: x > 5, range(10))")
    result2 = list(generator_filter(lambda x: x > 5, range(10)))
    print(f"   Result: {result2}")
    print()
    
    print("3. Generator Reduce:")
    print("   generator_reduce(lambda x, y: x + y, generator_map(lambda x: x ** 2, range(5)))")
    squares_gen = generator_map(lambda x: x ** 2, range(5))
    result3 = generator_reduce(lambda x, y: x + y, squares_gen)
    print(f"   Result: {result3}")
    print()

def implement_advanced_functions():
    
    print("=== Advanced Higher-Order Functions ===")
    
    def custom_any(predicate, iterable):
        for item in iterable:
            if predicate(item):
                return True
        return False
    
    def custom_all(predicate, iterable):
        for item in iterable:
            if not predicate(item):
                return False
        return True
    
    def custom_partition(predicate, iterable):
        true_items = []
        false_items = []
        for item in iterable:
            if predicate(item):
                true_items.append(item)
            else:
                false_items.append(item)
        return true_items, false_items
    
    def custom_group_by(key_func, iterable):
        groups = {}
        for item in iterable:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    
    def custom_zip_with(func, *iterables):
        return [func(*args) for args in zip(*iterables)]
    
    def custom_compose(*functions):
        def composed(x):
            result = x
            for func in reversed(functions):
                result = func(result)
            return result
        return composed
    
    print("1. Custom Any:")
    print("   custom_any(lambda x: x > 5, [1, 2, 3, 6, 4])")
    result1 = custom_any(lambda x: x > 5, [1, 2, 3, 6, 4])
    print(f"   Result: {result1}")
    print()
    
    print("2. Custom All:")
    print("   custom_all(lambda x: x > 0, [1, 2, 3, 4, 5])")
    result2 = custom_all(lambda x: x > 0, [1, 2, 3, 4, 5])
    print(f"   Result: {result2}")
    print()
    
    print("3. Custom Partition:")
    print("   custom_partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])")
    evens, odds = custom_partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])
    print(f"   Result: (evens={evens}, odds={odds})")
    print()
    
    print("4. Custom Group By:")
    print("   custom_group_by(lambda x: x[0], ['apple', 'banana', 'apricot', 'cherry'])")
    result4 = custom_group_by(lambda x: x[0], ['apple', 'banana', 'apricot', 'cherry'])
    print(f"   Result: {result4}")
    print()
    
    print("5. Custom Zip With:")
    print("   custom_zip_with(lambda x, y: x * y, [1, 2, 3], [4, 5, 6])")
    result5 = custom_zip_with(lambda x, y: x * y, [1, 2, 3], [4, 5, 6])
    print(f"   Result: {result5}")
    print()
    
    print("6. Custom Compose:")
    print("   composed = custom_compose(lambda x: x * 2, lambda x: x + 1)")
    print("   composed(5)")
    composed = custom_compose(lambda x: x * 2, lambda x: x + 1)
    result6 = composed(5)
    print(f"   Result: {result6} (first add 1, then multiply by 2)")
    print()

def demonstrate_practical_applications():
    
    print("=== Practical Applications ===")
    
    def custom_map(func, iterable):
        return [func(x) for x in iterable]
    
    def custom_filter(func, iterable):
        return [x for x in iterable if func(x)]
    
    def custom_reduce(func, iterable, initializer=None):
        if initializer is not None:
            result = initializer
            start_index = 0
        else:
            result = iterable[0]
            start_index = 1
        
        for x in iterable[start_index:]:
            result = func(result, x)
        return result
    
    students = [
        {'name': 'Alice', 'age': 20, 'grade': 85},
        {'name': 'Bob', 'age': 22, 'grade': 92},
        {'name': 'Charlie', 'age': 19, 'grade': 78},
        {'name': 'Diana', 'age': 21, 'grade': 96}
    ]
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("1. Data Processing Pipeline:")
    print("   Input numbers:", numbers)
    
    # Step 1: Filter even numbers
    evens = custom_filter(lambda x: x % 2 == 0, numbers)
    print(f"   Step 1 - Filter evens: {evens}")
    
    # Step 2: Square the even numbers
    squared_evens = custom_map(lambda x: x ** 2, evens)
    print(f"   Step 2 - Square evens: {squared_evens}")
    
    # Step 3: Sum all squared evens
    total = custom_reduce(lambda x, y: x + y, squared_evens)
    print(f"   Step 3 - Sum all: {total}")
    print()
    
    print("2. Student Data Analysis:")
    print("   Students data:", students)
    
    # Extract names
    names = custom_map(lambda s: s['name'], students)
    print(f"   Names: {names}")
    
    high_performers = custom_filter(lambda s: s['grade'] >= 90, students)
    high_performer_names = custom_map(lambda s: s['name'], high_performers)
    print(f"   High performers: {high_performer_names}")
    
    grades = custom_map(lambda s: s['grade'], students)
    average_grade = custom_reduce(lambda x, y: x + y, grades) / len(grades)
    print(f"   Average grade: {average_grade:.1f}")
    
    oldest = custom_reduce(lambda x, y: x if x['age'] > y['age'] else y, students)
    print(f"   Oldest student: {oldest['name']} ({oldest['age']} years)")
    print()
    
    print("3. String Processing:")
    words = ['hello', 'world', 'python', 'programming', 'is', 'fun']
    print(f"   Words: {words}")
    
    uppercase_words = custom_map(lambda w: w.upper(), words)
    print(f"   Uppercase: {uppercase_words}")
    
    long_words = custom_filter(lambda w: len(w) > 5, words)
    print(f"   Long words: {long_words}")
    
    sentence = custom_reduce(lambda x, y: x + ' ' + y, words)
    print(f"   Sentence: '{sentence}'")
    print()

def performance_comparison():
    
    print("=== Performance Comparison ===")
    
    import time
    from functools import reduce
    
    # Custom implementations
    def custom_map(func, iterable):
        return [func(x) for x in iterable]
    
    def custom_filter(func, iterable):
        return [x for x in iterable if func(x)]
    
    def custom_reduce(func, iterable):
        result = iterable[0]
        for x in iterable[1:]:
            result = func(result, x)
        return result
    
    # Test data
    large_list = list(range(100000))
    
    print(f"Testing with {len(large_list):,} elements...")
    print()
    
    # Map performance test
    print("1. Map Performance (square all numbers):")
    
    start_time = time.time()
    result1 = list(map(lambda x: x ** 2, large_list))
    builtin_map_time = time.time() - start_time
    
    start_time = time.time()
    result2 = custom_map(lambda x: x ** 2, large_list)
    custom_map_time = time.time() - start_time
    
    print(f"   Built-in map: {builtin_map_time:.4f} seconds")
    print(f"   Custom map:   {custom_map_time:.4f} seconds")
    print(f"   Results match: {result1 == result2}")
    print()
    
    # Filter performance test
    print("2. Filter Performance (even numbers):")
    
    start_time = time.time()
    result3 = list(filter(lambda x: x % 2 == 0, large_list))
    builtin_filter_time = time.time() - start_time
    
    start_time = time.time()
    result4 = custom_filter(lambda x: x % 2 == 0, large_list)
    custom_filter_time = time.time() - start_time
    
    print(f"   Built-in filter: {builtin_filter_time:.4f} seconds")
    print(f"   Custom filter:   {custom_filter_time:.4f} seconds")
    print(f"   Results match: {result3 == result4}")
    print()
    
    # Reduce performance test
    print("3. Reduce Performance (sum all numbers):")
    small_list = list(range(10000))  # Smaller list for reduce
    
    start_time = time.time()
    result5 = reduce(lambda x, y: x + y, small_list)
    builtin_reduce_time = time.time() - start_time
    
    start_time = time.time()
    result6 = custom_reduce(lambda x, y: x + y, small_list)
    custom_reduce_time = time.time() - start_time
    
    print(f"   Built-in reduce: {builtin_reduce_time:.4f} seconds")
    print(f"   Custom reduce:   {custom_reduce_time:.4f} seconds")
    print(f"   Results match: {result5 == result6}")
    print()

def interactive_function_builder():
    """Interactive tool to build and test higher-order functions"""
    
    print("=== Interactive Function Builder ===")
    
    # Custom implementations
    def custom_map(func, iterable):
        return [func(x) for x in iterable]
    
    def custom_filter(func, iterable):
        return [x for x in iterable if func(x)]
    
    def custom_reduce(func, iterable):
        result = iterable[0]
        for x in iterable[1:]:
            result = func(result, x)
        return result
    
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    while True:
        print(f"\nTest data: {test_data}")
        print("\nChoose operation:")
        print("1. Map")
        print("2. Filter")
        print("3. Reduce")
        print("4. Change test data")
        print("5. Return to main menu")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '5':
            break
        elif choice == '4':
            try:
                new_data = input("Enter new test data (comma-separated numbers): ")
                test_data = [int(x.strip()) for x in new_data.split(',')]
                print(f"New test data: {test_data}")
            except ValueError:
                print("Invalid input! Using default data.")
                test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            continue
        
        lambda_expr = input("Enter lambda expression (e.g., 'lambda x: x * 2'): ").strip()
        
        try:
            func = eval(lambda_expr)
            
            if choice == '1':
                result = custom_map(func, test_data)
                print(f"custom_map({lambda_expr}, {test_data}) = {result}")
            elif choice == '2':
                result = custom_filter(func, test_data)
                print(f"custom_filter({lambda_expr}, {test_data}) = {result}")
            elif choice == '3':
                if len(test_data) == 0:
                    print("Cannot reduce empty list!")
                else:
                    result = custom_reduce(func, test_data)
                    print(f"custom_reduce({lambda_expr}, {test_data}) = {result}")
            else:
                print("Invalid choice!")
                
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function to run the higher-order function implementation"""
    
    while True:
        print("\n" + "="*60)
        print("🔧 HIGHER-ORDER FUNCTION IMPLEMENTATION 🔧")
        print("="*60)
        print("1. Basic Examples (from requirements)")
        print("2. Enhanced Functions")
        print("3. Generator-Based Implementations")
        print("4. Advanced Higher-Order Functions")
        print("5. Practical Applications")
        print("6. Performance Comparison")
        print("7. Interactive Function Builder")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            demonstrate_basic_examples()
        elif choice == "2":
            implement_enhanced_functions()
        elif choice == "3":
            implement_generator_versions()
        elif choice == "4":
            implement_advanced_functions()
        elif choice == "5":
            demonstrate_practical_applications()
        elif choice == "6":
            performance_comparison()
        elif choice == "7":
            interactive_function_builder()
        elif choice == "8":
            print("Happy coding with higher-order functions! 🐍✨")
            break
        else:
            print("Invalid choice! Please enter 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
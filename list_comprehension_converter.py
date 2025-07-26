# List Comprehension Converter
# This program demonstrates converting traditional for-loops to list comprehensions

import time
import random

def demonstrate_basic_conversion():
    """Demonstrates basic loop to list comprehension conversion"""
    
    print("=== Basic List Creation ===")
    
    # Example 1: Squares
    print("1. Creating squares:")
    print("Traditional Loop:")
    print("squares = []")
    print("for i in range(10):")
    print("    squares.append(i * i)")
    
    # Traditional approach
    squares_traditional = []
    for i in range(10):
        squares_traditional.append(i * i)
    
    print(f"Result: {squares_traditional}")
    
    print("\nList Comprehension:")
    print("squares = [i * i for i in range(10)]")
    
    # List comprehension approach
    squares_comprehension = [i * i for i in range(10)]
    print(f"Result: {squares_comprehension}")
    
    print(f"Results match: {squares_traditional == squares_comprehension}")
    print()
    
    # Example 2: String operations
    print("2. String transformations:")
    words = ['hello', 'world', 'python', 'programming']
    
    print("Traditional Loop:")
    print("uppercase = []")
    print("for word in words:")
    print("    uppercase.append(word.upper())")
    
    # Traditional approach
    uppercase_traditional = []
    for word in words:
        uppercase_traditional.append(word.upper())
    
    print(f"Result: {uppercase_traditional}")
    
    print("\nList Comprehension:")
    print("uppercase = [word.upper() for word in words]")
    
    # List comprehension approach
    uppercase_comprehension = [word.upper() for word in words]
    print(f"Result: {uppercase_comprehension}")
    
    print(f"Results match: {uppercase_traditional == uppercase_comprehension}")
    print()

def demonstrate_filtering():
    """Demonstrates filtering with list comprehensions"""
    
    print("=== Filtering with Conditions ===")
    
    # Example 1: Even numbers
    print("1. Filtering even numbers:")
    print("Traditional Loop:")
    print("evens = []")
    print("for i in range(20):")
    print("    if i % 2 == 0:")
    print("        evens.append(i)")
    
    # Traditional approach
    evens_traditional = []
    for i in range(20):
        if i % 2 == 0:
            evens_traditional.append(i)
    
    print(f"Result: {evens_traditional}")
    
    print("\nList Comprehension:")
    print("evens = [i for i in range(20) if i % 2 == 0]")
    
    # List comprehension approach
    evens_comprehension = [i for i in range(20) if i % 2 == 0]
    print(f"Result: {evens_comprehension}")
    
    print(f"Results match: {evens_traditional == evens_comprehension}")
    print()
    
    # Example 2: Filtering strings by length
    print("2. Filtering words by length:")
    words = ['cat', 'elephant', 'dog', 'hippopotamus', 'bird', 'whale']
    
    print("Traditional Loop (words with length > 4):")
    print("long_words = []")
    print("for word in words:")
    print("    if len(word) > 4:")
    print("        long_words.append(word)")
    
    # Traditional approach
    long_words_traditional = []
    for word in words:
        if len(word) > 4:
            long_words_traditional.append(word)
    
    print(f"Result: {long_words_traditional}")
    
    print("\nList Comprehension:")
    print("long_words = [word for word in words if len(word) > 4]")
    
    # List comprehension approach
    long_words_comprehension = [word for word in words if len(word) > 4]
    print(f"Result: {long_words_comprehension}")
    
    print(f"Results match: {long_words_traditional == long_words_comprehension}")
    print()
    
    # Example 3: Complex filtering with transformation
    print("3. Complex filtering with transformation:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("Traditional Loop (squares of odd numbers):")
    print("odd_squares = []")
    print("for num in numbers:")
    print("    if num % 2 == 1:")
    print("        odd_squares.append(num ** 2)")
    
    # Traditional approach
    odd_squares_traditional = []
    for num in numbers:
        if num % 2 == 1:
            odd_squares_traditional.append(num ** 2)
    
    print(f"Result: {odd_squares_traditional}")
    
    print("\nList Comprehension:")
    print("odd_squares = [num ** 2 for num in numbers if num % 2 == 1]")
    
    # List comprehension approach
    odd_squares_comprehension = [num ** 2 for num in numbers if num % 2 == 1]
    print(f"Result: {odd_squares_comprehension}")
    
    print(f"Results match: {odd_squares_traditional == odd_squares_comprehension}")
    print()

def demonstrate_nested_loops():
    """Demonstrates nested loop conversion to list comprehensions"""
    
    print("=== Nested Loops ===")
    
    # Example 1: Coordinate pairs
    print("1. Creating coordinate pairs:")
    print("Traditional Nested Loop:")
    print("pairs = []")
    print("for x in range(3):")
    print("    for y in range(2):")
    print("        pairs.append((x, y))")
    
    # Traditional approach
    pairs_traditional = []
    for x in range(3):
        for y in range(2):
            pairs_traditional.append((x, y))
    
    print(f"Result: {pairs_traditional}")
    
    print("\nList Comprehension:")
    print("pairs = [(x, y) for x in range(3) for y in range(2)]")
    
    # List comprehension approach
    pairs_comprehension = [(x, y) for x in range(3) for y in range(2)]
    print(f"Result: {pairs_comprehension}")
    
    print(f"Results match: {pairs_traditional == pairs_comprehension}")
    print()
    
    # Example 2: Matrix flattening
    print("2. Matrix flattening:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    print("Traditional Nested Loop:")
    print("flattened = []")
    print("for row in matrix:")
    print("    for item in row:")
    print("        flattened.append(item)")
    
    # Traditional approach
    flattened_traditional = []
    for row in matrix:
        for item in row:
            flattened_traditional.append(item)
    
    print(f"Result: {flattened_traditional}")
    
    print("\nList Comprehension:")
    print("flattened = [item for row in matrix for item in row]")
    
    # List comprehension approach
    flattened_comprehension = [item for row in matrix for item in row]
    print(f"Result: {flattened_comprehension}")
    
    print(f"Results match: {flattened_traditional == flattened_comprehension}")
    print()
    
    # Example 3: Multiplication table
    print("3. Multiplication table (filtered):")
    print("Traditional Nested Loop (products < 20):")
    print("products = []")
    print("for i in range(1, 6):")
    print("    for j in range(1, 6):")
    print("        product = i * j")
    print("        if product < 20:")
    print("            products.append((i, j, product))")
    
    # Traditional approach
    products_traditional = []
    for i in range(1, 6):
        for j in range(1, 6):
            product = i * j
            if product < 20:
                products_traditional.append((i, j, product))
    
    print(f"Result: {products_traditional}")
    
    print("\nList Comprehension:")
    print("products = [(i, j, i*j) for i in range(1, 6) for j in range(1, 6) if i*j < 20]")
    
    # List comprehension approach
    products_comprehension = [(i, j, i*j) for i in range(1, 6) for j in range(1, 6) if i*j < 20]
    print(f"Result: {products_comprehension}")
    
    print(f"Results match: {products_traditional == products_comprehension}")
    print()

def demonstrate_advanced_comprehensions():
    """Demonstrates advanced list comprehension techniques"""
    
    print("=== Advanced Comprehensions ===")
    
    # Example 1: Conditional expressions
    print("1. Conditional expressions (ternary operator):")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("Traditional Loop:")
    print("classified = []")
    print("for num in numbers:")
    print("    if num % 2 == 0:")
    print("        classified.append('even')")
    print("    else:")
    print("        classified.append('odd')")
    
    # Traditional approach
    classified_traditional = []
    for num in numbers:
        if num % 2 == 0:
            classified_traditional.append('even')
        else:
            classified_traditional.append('odd')
    
    print(f"Result: {classified_traditional}")
    
    print("\nList Comprehension:")
    print("classified = ['even' if num % 2 == 0 else 'odd' for num in numbers]")
    
    # List comprehension approach
    classified_comprehension = ['even' if num % 2 == 0 else 'odd' for num in numbers]
    print(f"Result: {classified_comprehension}")
    
    print(f"Results match: {classified_traditional == classified_comprehension}")
    print()
    
    # Example 2: Working with dictionaries
    print("2. Dictionary to list conversion:")
    scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'Diana': 96}
    
    print("Traditional Loop:")
    print("high_scorers = []")
    print("for name, score in scores.items():")
    print("    if score > 80:")
    print("        high_scorers.append(f'{name}: {score}')")
    
    # Traditional approach
    high_scorers_traditional = []
    for name, score in scores.items():
        if score > 80:
            high_scorers_traditional.append(f'{name}: {score}')
    
    print(f"Result: {high_scorers_traditional}")
    
    print("\nList Comprehension:")
    print("high_scorers = [f'{name}: {score}' for name, score in scores.items() if score > 80]")
    
    # List comprehension approach
    high_scorers_comprehension = [f'{name}: {score}' for name, score in scores.items() if score > 80]
    print(f"Result: {high_scorers_comprehension}")
    
    print(f"Results match: {high_scorers_traditional == high_scorers_comprehension}")
    print()

def performance_comparison():
    """Compares performance between traditional loops and list comprehensions"""
    
    print("=== Performance Comparison ===")
    
    # Generate large dataset
    large_numbers = list(range(100000))
    
    # Test 1: Simple transformation
    print("1. Simple transformation (squares of 100,000 numbers):")
    
    # Traditional approach timing
    start_time = time.time()
    squares_traditional = []
    for num in large_numbers:
        squares_traditional.append(num ** 2)
    traditional_time = time.time() - start_time
    
    # List comprehension timing
    start_time = time.time()
    squares_comprehension = [num ** 2 for num in large_numbers]
    comprehension_time = time.time() - start_time
    
    print(f"Traditional loop time: {traditional_time:.4f} seconds")
    print(f"List comprehension time: {comprehension_time:.4f} seconds")
    print(f"List comprehension is {traditional_time/comprehension_time:.2f}x faster")
    print()
    
    # Test 2: Filtering
    print("2. Filtering (even numbers from 100,000):")
    
    # Traditional approach timing
    start_time = time.time()
    evens_traditional = []
    for num in large_numbers:
        if num % 2 == 0:
            evens_traditional.append(num)
    traditional_time = time.time() - start_time
    
    # List comprehension timing
    start_time = time.time()
    evens_comprehension = [num for num in large_numbers if num % 2 == 0]
    comprehension_time = time.time() - start_time
    
    print(f"Traditional loop time: {traditional_time:.4f} seconds")
    print(f"List comprehension time: {comprehension_time:.4f} seconds")
    print(f"List comprehension is {traditional_time/comprehension_time:.2f}x faster")
    print()

def interactive_converter():
    """Interactive tool to practice converting loops to comprehensions"""
    
    print("=== Interactive Converter Practice ===")
    
    exercises = [
        {
            "description": "Create cubes of numbers 1-10",
            "traditional": "cubes = []\nfor i in range(1, 11):\n    cubes.append(i ** 3)",
            "comprehension": "[i ** 3 for i in range(1, 11)]",
            "test_func": lambda: [i ** 3 for i in range(1, 11)]
        },
        {
            "description": "Get words longer than 5 characters",
            "traditional": "long_words = []\nfor word in ['apple', 'banana', 'cat', 'elephant']:\n    if len(word) > 5:\n        long_words.append(word)",
            "comprehension": "[word for word in ['apple', 'banana', 'cat', 'elephant'] if len(word) > 5]",
            "test_func": lambda: [word for word in ['apple', 'banana', 'cat', 'elephant'] if len(word) > 5]
        },
        {
            "description": "Create all combinations of [1,2] and ['a','b']",
            "traditional": "combinations = []\nfor num in [1, 2]:\n    for letter in ['a', 'b']:\n        combinations.append((num, letter))",
            "comprehension": "[(num, letter) for num in [1, 2] for letter in ['a', 'b']]",
            "test_func": lambda: [(num, letter) for num in [1, 2] for letter in ['a', 'b']]
        }
    ]
    
    for i, exercise in enumerate(exercises, 1):
        print(f"\n--- Exercise {i} ---")
        print(f"Task: {exercise['description']}")
        print("\nTraditional Loop:")
        print(exercise['traditional'])
        print(f"\nExpected Result: {exercise['test_func']()}")
        
        user_input = input("\nEnter your list comprehension: ").strip()
        
        if user_input == exercise['comprehension']:
            print("✅ Correct! Well done!")
        else:
            print("❌ Not quite right.")
            print(f"Correct answer: {exercise['comprehension']}")
        
        show_solution = input("Show explanation? (y/n): ").strip().lower()
        if show_solution in ['y', 'yes']:
            print(f"\nExplanation:")
            print(f"The comprehension '{exercise['comprehension']}' is equivalent to the traditional loop.")
            print("Key components:")
            if 'if' in exercise['comprehension']:
                print("- Expression: what to include in the result")
                print("- Iteration: what to loop over")
                print("- Condition: what to filter")
            else:
                print("- Expression: what to include in the result")
                print("- Iteration: what to loop over")

def main():
    """Main function to run the list comprehension converter"""
    
    while True:
        print("\n" + "="*60)
        print("📝 LIST COMPREHENSION CONVERTER 📝")
        print("="*60)
        print("1. Basic Conversion Examples")
        print("2. Filtering Examples")
        print("3. Nested Loop Examples")
        print("4. Advanced Comprehensions")
        print("5. Performance Comparison")
        print("6. Interactive Practice")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            demonstrate_basic_conversion()
        elif choice == "2":
            demonstrate_filtering()
        elif choice == "3":
            demonstrate_nested_loops()
        elif choice == "4":
            demonstrate_advanced_comprehensions()
        elif choice == "5":
            performance_comparison()
        elif choice == "6":
            interactive_converter()
        elif choice == "7":
            print("Happy coding with list comprehensions! 🐍✨")
            break
        else:
            print("Invalid choice! Please enter 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
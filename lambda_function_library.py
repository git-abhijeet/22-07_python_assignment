
from functools import reduce
import math

def demonstrate_basic_examples():
    """Demonstrates the basic lambda examples from requirements"""
    
    print("=== Basic Examples from Requirements ===")
    
    square = lambda x: x * x
    reverse = lambda s: s[::-1]
    filter_evens = lambda lst: list(filter(lambda x: x % 2 == 0, lst))
    
    print("1. Square function:")
    print("   square = lambda x: x * x")
    test_value = 5
    result = square(test_value)
    print(f"   square({test_value}) = {result}")
    print()
    
    print("2. Reverse string function:")
    print("   reverse = lambda s: s[::-1]")
    test_string = "hello"
    result = reverse(test_string)
    print(f"   reverse('{test_string}') = '{result}'")
    print()
    
    print("3. Filter evens function:")
    print("   filter_evens = lambda lst: list(filter(lambda x: x % 2 == 0, lst))")
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = filter_evens(test_list)
    print(f"   filter_evens({test_list}) = {result}")
    print()

def demonstrate_mathematical_lambdas():
    """Demonstrates mathematical lambda functions"""
    
    print("=== Mathematical Lambda Functions ===")
    
    add = lambda x, y: x + y
    multiply = lambda x, y: x * y
    power = lambda x, y: x ** y
    cube = lambda x: x ** 3
    absolute = lambda x: abs(x)
    
    factorial = lambda n: reduce(lambda x, y: x * y, range(1, n + 1), 1)
    fibonacci = lambda n: n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)
    is_prime = lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
    gcd = lambda a, b: a if b == 0 else gcd(b, a % b)
    
    sin_degrees = lambda degrees: math.sin(math.radians(degrees))
    cos_degrees = lambda degrees: math.cos(math.radians(degrees))
    
    distance_2d = lambda x1, y1, x2, y2: math.sqrt((x2-x1)**2 + (y2-y1)**2)
    circle_area = lambda radius: math.pi * radius ** 2
    
    print("Basic Operations:")
    print(f"   add = lambda x, y: x + y")
    print(f"   add(5, 3) = {add(5, 3)}")
    print(f"   multiply(4, 7) = {multiply(4, 7)}")
    print(f"   power(2, 8) = {power(2, 8)}")
    print(f"   cube(4) = {cube(4)}")
    print(f"   absolute(-15) = {absolute(-15)}")
    print()
    
    print("Advanced Operations:")
    print(f"   factorial(5) = {factorial(5)}")
    print(f"   fibonacci(7) = {fibonacci(7)}")
    print(f"   is_prime(17) = {is_prime(17)}")
    print(f"   gcd(48, 18) = {gcd(48, 18)}")
    print()
    
    print("Trigonometric Functions:")
    print(f"   sin_degrees(30) = {sin_degrees(30):.4f}")
    print(f"   cos_degrees(60) = {cos_degrees(60):.4f}")
    print()
    
    print("Geometry Functions:")
    print(f"   distance_2d(0, 0, 3, 4) = {distance_2d(0, 0, 3, 4):.2f}")
    print(f"   circle_area(5) = {circle_area(5):.2f}")
    print()

def demonstrate_string_lambdas():
    """Demonstrates string manipulation lambda functions"""
    
    print("=== String Manipulation Lambda Functions ===")
    
    uppercase = lambda s: s.upper()
    lowercase = lambda s: s.lower()
    capitalize_first = lambda s: s.capitalize()
    title_case = lambda s: s.title()
    reverse = lambda s: s[::-1]
    
    count_vowels = lambda s: sum(1 for c in s.lower() if c in 'aeiou')
    count_words = lambda s: len(s.split())
    remove_spaces = lambda s: s.replace(' ', '')
    is_palindrome = lambda s: s.lower() == s.lower()[::-1]
    
    swap_case = lambda s: s.swapcase()
    remove_vowels = lambda s: ''.join(c for c in s if c.lower() not in 'aeiou')
    first_char = lambda s: s[0] if s else ''
    last_char = lambda s: s[-1] if s else ''
    
    repeat_string = lambda s, n: s * n
    truncate = lambda s, n: s[:n] + '...' if len(s) > n else s
    center_string = lambda s, width: s.center(width)
    
    test_string = "Hello World"
    
    print("Basic String Operations:")
    print(f"   uppercase('{test_string}') = '{uppercase(test_string)}'")
    print(f"   lowercase('{test_string}') = '{lowercase(test_string)}'")
    print(f"   capitalize_first('{test_string}') = '{capitalize_first(test_string)}'")
    print(f"   title_case('{test_string}') = '{title_case(test_string)}'")
    print(f"   reverse('{test_string}') = '{reverse(test_string)}'")
    print()
    
    print("String Analysis:")
    print(f"   count_vowels('{test_string}') = {count_vowels(test_string)}")
    print(f"   count_words('{test_string}') = {count_words(test_string)}")
    print(f"   remove_spaces('{test_string}') = '{remove_spaces(test_string)}'")
    print(f"   is_palindrome('radar') = {is_palindrome('radar')}")
    print()
    
    print("String Transformations:")
    print(f"   swap_case('{test_string}') = '{swap_case(test_string)}'")
    print(f"   remove_vowels('{test_string}') = '{remove_vowels(test_string)}'")
    print(f"   first_char('{test_string}') = '{first_char(test_string)}'")
    print(f"   last_char('{test_string}') = '{last_char(test_string)}'")
    print()
    
    print("String Utilities:")
    print(f"   repeat_string('Hi', 3) = '{repeat_string('Hi', 3)}'")
    print(f"   truncate('{test_string}', 5) = '{truncate(test_string, 5)}'")
    print(f"   center_string('Hi', 10) = '{center_string('Hi', 10)}'")
    print()

def demonstrate_list_lambdas():
    """Demonstrates list operation lambda functions"""
    
    print("=== List Operation Lambda Functions ===")
    
    filter_evens = lambda lst: list(filter(lambda x: x % 2 == 0, lst))
    filter_odds = lambda lst: list(filter(lambda x: x % 2 == 1, lst))
    filter_positive = lambda lst: list(filter(lambda x: x > 0, lst))
    filter_greater_than = lambda lst, n: list(filter(lambda x: x > n, lst))
    
    square_list = lambda lst: list(map(lambda x: x ** 2, lst))
    double_list = lambda lst: list(map(lambda x: x * 2, lst))
    abs_list = lambda lst: list(map(abs, lst))
    str_list = lambda lst: list(map(str, lst))
    
    sum_list = lambda lst: sum(lst)
    product_list = lambda lst: reduce(lambda x, y: x * y, lst, 1)
    max_value = lambda lst: max(lst) if lst else None
    min_value = lambda lst: min(lst) if lst else None
    average = lambda lst: sum(lst) / len(lst) if lst else 0
    
    reverse_list = lambda lst: lst[::-1]
    first_n = lambda lst, n: lst[:n]
    last_n = lambda lst, n: lst[-n:] if n <= len(lst) else lst
    unique_list = lambda lst: list(set(lst))
    flatten = lambda lst: [item for sublist in lst for item in sublist]
    
    all_positive = lambda lst: all(x > 0 for x in lst)
    any_negative = lambda lst: any(x < 0 for x in lst)
    is_sorted = lambda lst: lst == sorted(lst)
    
    test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    mixed_list = [-3, -1, 0, 2, 4, 6]
    nested_list = [[1, 2], [3, 4], [5, 6]]
    
    print("Filtering Operations:")
    print(f"   filter_evens({test_list}) = {filter_evens(test_list)}")
    print(f"   filter_odds({test_list}) = {filter_odds(test_list)}")
    print(f"   filter_positive({mixed_list}) = {filter_positive(mixed_list)}")
    print(f"   filter_greater_than({test_list}, 5) = {filter_greater_than(test_list, 5)}")
    print()
    
    print("Transformation Operations:")
    print(f"   square_list([1, 2, 3, 4]) = {square_list([1, 2, 3, 4])}")
    print(f"   double_list([1, 2, 3, 4]) = {double_list([1, 2, 3, 4])}")
    print(f"   abs_list({mixed_list}) = {abs_list(mixed_list)}")
    print(f"   str_list([1, 2, 3]) = {str_list([1, 2, 3])}")
    print()
    
    print("Aggregation Operations:")
    print(f"   sum_list({test_list[:5]}) = {sum_list(test_list[:5])}")
    print(f"   product_list([1, 2, 3, 4]) = {product_list([1, 2, 3, 4])}")
    print(f"   max_value({test_list[:5]}) = {max_value(test_list[:5])}")
    print(f"   min_value({test_list[:5]}) = {min_value(test_list[:5])}")
    print(f"   average({test_list[:5]}) = {average(test_list[:5])}")
    print()
    
    print("List Utilities:")
    print(f"   reverse_list([1, 2, 3, 4, 5]) = {reverse_list([1, 2, 3, 4, 5])}")
    print(f"   first_n({test_list}, 3) = {first_n(test_list, 3)}")
    print(f"   last_n({test_list}, 3) = {last_n(test_list, 3)}")
    print(f"   unique_list([1, 2, 2, 3, 3, 4]) = {unique_list([1, 2, 2, 3, 3, 4])}")
    print(f"   flatten({nested_list}) = {flatten(nested_list)}")
    print()
    
    print("Boolean Operations:")
    print(f"   all_positive([1, 2, 3, 4]) = {all_positive([1, 2, 3, 4])}")
    print(f"   any_negative({mixed_list}) = {any_negative(mixed_list)}")
    print(f"   is_sorted([1, 2, 3, 4, 5]) = {is_sorted([1, 2, 3, 4, 5])}")
    print()

def demonstrate_advanced_lambdas():
    """Demonstrates advanced and complex lambda functions"""
    
    print("=== Advanced Lambda Functions ===")
    
    compose = lambda f, g: lambda x: f(g(x))
    apply_n_times = lambda f, n: lambda x: x if n == 0 else f(apply_n_times(f, n-1)(x))
    conditional = lambda condition, true_func, false_func: lambda x: true_func(x) if condition(x) else false_func(x)
    
    group_by = lambda lst, key_func: {k: [item for item in lst if key_func(item) == k] for k in set(map(key_func, lst))}
    sort_by = lambda lst, key_func: sorted(lst, key=key_func)
    partition = lambda lst, predicate: (list(filter(predicate, lst)), list(filter(lambda x: not predicate(x), lst)))
    
    extract_numbers = lambda s: [int(x) for x in s.split() if x.isdigit()]
    word_lengths = lambda sentence: list(map(len, sentence.split()))
    initials = lambda name: ''.join(word[0].upper() for word in name.split())
    
    clamp = lambda x, min_val, max_val: max(min_val, min(x, max_val))
    normalize = lambda lst: [(x - min(lst)) / (max(lst) - min(lst)) for x in lst] if max(lst) != min(lst) else [0] * len(lst)
    percentage = lambda part, total: (part / total) * 100 if total != 0 else 0
    
    print("Higher-order Functions:")
    double = lambda x: x * 2
    add_one = lambda x: x + 1
    double_then_add_one = compose(add_one, double)
    print(f"   compose(add_one, double)(5) = {double_then_add_one(5)}")
    
    increment = lambda x: x + 1
    increment_3_times = apply_n_times(increment, 3)
    print(f"   apply_n_times(increment, 3)(5) = {increment_3_times(5)}")
    print()
    
    print("Data Processing:")
    words = ['apple', 'banana', 'apricot', 'blueberry', 'cherry']
    grouped = group_by(words, lambda word: word[0])
    print(f"   group_by({words}, first_letter) = {grouped}")
    
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_numbers = sort_by(numbers, lambda x: x)
    print(f"   sort_by({numbers}, identity) = {sorted_numbers}")
    
    evens, odds = partition(numbers, lambda x: x % 2 == 0)
    print(f"   partition({numbers}, is_even) = ({evens}, {odds})")
    print()
    
    print("String Processors:")
    text = "I have 5 apples and 10 oranges"
    print(f"   extract_numbers('{text}') = {extract_numbers(text)}")
    
    sentence = "Hello world Python"
    print(f"   word_lengths('{sentence}') = {word_lengths(sentence)}")
    
    name = "John Doe Smith"
    print(f"   initials('{name}') = '{initials(name)}'")
    print()
    
    print("Mathematical Utilities:")
    print(f"   clamp(15, 1, 10) = {clamp(15, 1, 10)}")
    
    data = [1, 5, 3, 9, 2]
    normalized = normalize(data)
    print(f"   normalize({data}) = {[round(x, 3) for x in normalized]}")
    
    print(f"   percentage(25, 200) = {percentage(25, 200)}%")
    print()

def lambda_function_challenges():
    """Interactive challenges using lambda functions"""
    
    print("=== Lambda Function Challenges ===")
    
    challenges = [
        {
            "description": "Create a lambda to calculate the area of a rectangle",
            "solution": "lambda length, width: length * width",
            "test": lambda: (lambda length, width: length * width)(5, 3),
            "expected": 15
        },
        {
            "description": "Create a lambda to check if a number is even",
            "solution": "lambda x: x % 2 == 0",
            "test": lambda: (lambda x: x % 2 == 0)(8),
            "expected": True
        },
        {
            "description": "Create a lambda to get the maximum of three numbers",
            "solution": "lambda a, b, c: max(a, b, c)",
            "test": lambda: (lambda a, b, c: max(a, b, c))(10, 5, 15),
            "expected": 15
        },
        {
            "description": "Create a lambda to count characters in a string",
            "solution": "lambda s: len(s)",
            "test": lambda: (lambda s: len(s))("hello"),
            "expected": 5
        },
        {
            "description": "Create a lambda to convert Celsius to Fahrenheit",
            "solution": "lambda c: c * 9/5 + 32",
            "test": lambda: (lambda c: c * 9/5 + 32)(0),
            "expected": 32.0
        }
    ]
    
    score = 0
    total = len(challenges)
    
    for i, challenge in enumerate(challenges, 1):
        print(f"\n--- Challenge {i} ---")
        print(f"Task: {challenge['description']}")
        print(f"Expected result for test: {challenge['expected']}")
        
        user_answer = input("Enter your lambda function: ").strip()
        
        try:
            user_lambda = eval(user_answer)
            user_result = user_lambda(*challenge['test'].__code__.co_consts[1:]) if hasattr(challenge['test'].__code__, 'co_consts') else challenge['test']()
            
            if user_result == challenge['expected']:
                print("✅ Correct! Great job!")
                score += 1
            else:
                print(f"❌ Not quite right. Got {user_result}, expected {challenge['expected']}")
        except Exception as e:
            print(f"❌ Error in your lambda: {e}")
        
        print(f"Correct solution: {challenge['solution']}")
        actual_result = challenge['test']()
        print(f"Actual result: {actual_result}")
    
    print(f"\n=== Final Score: {score}/{total} ===")
    if score == total:
        print("🎉 Perfect score! You're a lambda master!")
    elif score >= total * 0.7:
        print("👍 Great job! You're getting good with lambdas!")
    else:
        print("💪 Keep practicing! Lambda functions take time to master.")

def lambda_reference():
    """Provides a reference guide for lambda functions"""
    
    print("=== Lambda Function Reference ===")
    
    reference = {
        "Basic Syntax": [
            "lambda arguments: expression",
            "lambda x: x + 1  # Single argument",
            "lambda x, y: x + y  # Multiple arguments",
            "lambda: 42  # No arguments"
        ],
        "Common Patterns": [
            "lambda x: x ** 2  # Square",
            "lambda x: x % 2 == 0  # Even check",
            "lambda s: s.upper()  # String transformation",
            "lambda lst: len(lst)  # List length",
            "lambda x, y: x if x > y else y  # Conditional"
        ],
        "With Built-in Functions": [
            "map(lambda x: x * 2, [1, 2, 3])",
            "filter(lambda x: x > 0, [-1, 0, 1, 2])",
            "sorted(lst, key=lambda x: x[1])",
            "reduce(lambda x, y: x + y, [1, 2, 3, 4])"
        ],
        "Best Practices": [
            "Keep lambdas simple and readable",
            "Use regular functions for complex logic",
            "Avoid side effects in lambdas",
            "Consider using partial() for complex cases",
            "Document complex lambda expressions"
        ],
        "Common Use Cases": [
            "Quick data transformations",
            "Sorting with custom keys",
            "Event handling (GUI programming)",
            "Functional programming patterns",
            "API callback functions"
        ]
    }
    
    for category, items in reference.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")

def main():
    """Main function to run the lambda function library"""
    
    while True:
        print("\n" + "="*60)
        print("🔥 LAMBDA FUNCTION LIBRARY 🔥")
        print("="*60)
        print("1. Basic Examples (from requirements)")
        print("2. Mathematical Lambda Functions")
        print("3. String Manipulation Lambdas")
        print("4. List Operation Lambdas")
        print("5. Advanced Lambda Functions")
        print("6. Lambda Function Challenges")
        print("7. Lambda Reference Guide")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            demonstrate_basic_examples()
        elif choice == "2":
            demonstrate_mathematical_lambdas()
        elif choice == "3":
            demonstrate_string_lambdas()
        elif choice == "4":
            demonstrate_list_lambdas()
        elif choice == "5":
            demonstrate_advanced_lambdas()
        elif choice == "6":
            lambda_function_challenges()
        elif choice == "7":
            lambda_reference()
        elif choice == "8":
            print("Happy coding with lambdas! 🐍✨")
            break
        else:
            print("Invalid choice! Please enter 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

from functools import reduce
import operator
import math

def demonstrate_basic_examples():
    """Demonstrates the basic examples from the requirements"""
    
    print("=== Basic Examples from Requirements ===")
    
    print("1. Square of even numbers from 1 to 10:")
    print("One-liner: [i*i for i in range(1, 11) if i % 2 == 0]")
    result1 = [i*i for i in range(1, 11) if i % 2 == 0]
    print(f"Result: {result1}")
    print()
    
    print("2. Capitalize all words in a list:")
    print("One-liner: list(map(str.capitalize, ['hello', 'world']))")
    result2 = list(map(str.capitalize, ['hello', 'world']))
    print(f"Result: {result2}")
    print()
    
    print("3. Sum of all numbers using reduce:")
    print("One-liner: reduce(lambda x, y: x + y, [1, 2, 3, 4])")
    result3 = reduce(lambda x, y: x + y, [1, 2, 3, 4])
    print(f"Result: {result3}")
    print()

def demonstrate_list_comprehension_challenges():
    """Demonstrates advanced list comprehension one-liners"""
    
    print("=== List Comprehension Challenges ===")
    
    print("1. Flatten a 2D matrix:")
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"Input: {matrix}")
    print("One-liner: [item for row in matrix for item in row]")
    result1 = [item for row in matrix for item in row]
    print(f"Result: {result1}")
    print()
    
    print("2. Get prime numbers up to 30:")
    print("One-liner: [n for n in range(2, 31) if all(n % i != 0 for i in range(2, int(n**0.5) + 1))]")
    result2 = [n for n in range(2, 31) if all(n % i != 0 for i in range(2, int(n**0.5) + 1))]
    print(f"Result: {result2}")
    print()
    
    print("3. Create dictionary from two lists:")
    keys = ['name', 'age', 'city']
    values = ['Alice', 25, 'New York']
    print(f"Keys: {keys}")
    print(f"Values: {values}")
    print("One-liner: {k: v for k, v in zip(keys, values)}")
    result3 = {k: v for k, v in zip(keys, values)}
    print(f"Result: {result3}")
    print()
    
    print("4. Find common elements in two lists:")
    list1 = [1, 2, 3, 4, 5]
    list2 = [3, 4, 5, 6, 7]
    print(f"List 1: {list1}")
    print(f"List 2: {list2}")
    print("One-liner: [x for x in list1 if x in list2]")
    result4 = [x for x in list1 if x in list2]
    print(f"Result: {result4}")
    print()
    
    print("5. Generate multiplication table (1-5):")
    print("One-liner: [(i, j, i*j) for i in range(1, 6) for j in range(1, 6)]")
    result5 = [(i, j, i*j) for i in range(1, 6) for j in range(1, 6)]
    print(f"Result (first 10): {result5[:10]}...")
    print()

def demonstrate_lambda_challenges():
    """Demonstrates lambda function one-liners"""
    
    print("=== Lambda Function Challenges ===")
    
    print("1. Sort list of tuples by second element:")
    students = [('Alice', 85), ('Bob', 90), ('Charlie', 78), ('Diana', 92)]
    print(f"Input: {students}")
    print("One-liner: sorted(students, key=lambda x: x[1])")
    result1 = sorted(students, key=lambda x: x[1])
    print(f"Result: {result1}")
    print()
    
    print("2. Filter odd numbers and square them:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Input: {numbers}")
    print("One-liner: list(map(lambda x: x**2, filter(lambda x: x % 2 == 1, numbers)))")
    result2 = list(map(lambda x: x**2, filter(lambda x: x % 2 == 1, numbers)))
    print(f"Result: {result2}")
    print()
    
    print("3. Find maximum using reduce and lambda:")
    numbers = [45, 23, 89, 12, 67, 34]
    print(f"Input: {numbers}")
    print("One-liner: reduce(lambda x, y: x if x > y else y, numbers)")
    result3 = reduce(lambda x, y: x if x > y else y, numbers)
    print(f"Result: {result3}")
    print()
    
    print("4. Group words by first letter:")
    words = ['apple', 'banana', 'cherry', 'apricot', 'blueberry', 'avocado']
    print(f"Input: {words}")
    print("One-liner: {k: [w for w in words if w[0] == k] for k in set(w[0] for w in words)}")
    result4 = {k: [w for w in words if w[0] == k] for k in set(w[0] for w in words)}
    print(f"Result: {result4}")
    print()

def demonstrate_map_filter_reduce_challenges():
    """Demonstrates map, filter, and reduce one-liners"""
    
    print("=== Map, Filter, Reduce Challenges ===")
    
    print("1. Convert strings to integers and filter > 5:")
    string_numbers = ['1', '10', '3', '15', '7', '2']
    print(f"Input: {string_numbers}")
    print("One-liner: list(filter(lambda x: x > 5, map(int, string_numbers)))")
    result1 = list(filter(lambda x: x > 5, map(int, string_numbers)))
    print(f"Result: {result1}")
    print()
    
    print("2. Calculate factorial of 5 using reduce:")
    print("One-liner: reduce(lambda x, y: x * y, range(1, 6))")
    result2 = reduce(lambda x, y: x * y, range(1, 6))
    print(f"Result: {result2}")
    print()
    
    print("3. Get lengths of words using map:")
    words = ['Python', 'JavaScript', 'Go', 'Rust', 'Swift']
    print(f"Input: {words}")
    print("One-liner: list(map(len, words))")
    result3 = list(map(len, words))
    print(f"Result: {result3}")
    print()
    
    print("4. Chain multiple operations (filter evens, square, sum):")
    numbers = range(1, 11)
    print(f"Input: {list(numbers)}")
    print("One-liner: reduce(operator.add, map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))")
    result4 = reduce(operator.add, map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
    print(f"Result: {result4}")
    print()

def demonstrate_advanced_challenges():
    """Demonstrates advanced one-liner challenges"""
    
    print("=== Advanced One-Liner Challenges ===")
    
    print("1. Generate first 10 Fibonacci numbers:")
    print("One-liner: [a := [1, 1], [a.append(a[-1] + a[-2]) for _ in range(8)], a][2]")
    result1 = [a := [1, 1], [a.append(a[-1] + a[-2]) for _ in range(8)], a][2]
    print(f"Result: {result1}")
    print()
    
    print("2. Count word frequencies:")
    text = "the quick brown fox jumps over the lazy dog the fox is quick"
    words = text.split()
    print(f"Input: {text}")
    print("One-liner: {word: words.count(word) for word in set(words)}")
    result2 = {word: words.count(word) for word in set(words)}
    print(f"Result: {result2}")
    print()
    
    print("3. Find palindromes in a list:")
    words = ['radar', 'hello', 'level', 'world', 'madam', 'python']
    print(f"Input: {words}")
    print("One-liner: [word for word in words if word == word[::-1]]")
    result3 = [word for word in words if word == word[::-1]]
    print(f"Result: {result3}")
    print()
    
    print("4. Calculate distances from origin for list of points:")
    points = [(3, 4), (1, 1), (5, 12), (0, 0)]
    print(f"Input: {points}")
    print("One-liner: [math.sqrt(x**2 + y**2) for x, y in points]")
    result4 = [math.sqrt(x**2 + y**2) for x, y in points]
    print(f"Result: {[round(d, 2) for d in result4]}")
    print()
    
    print("5. Generate all 2-letter combinations:")
    letters = 'ABC'
    print(f"Input letters: {letters}")
    print("One-liner: [a + b for a in letters for b in letters]")
    result5 = [a + b for a in letters for b in letters]
    print(f"Result: {result5}")
    print()

def demonstrate_string_challenges():
    """Demonstrates string manipulation one-liners"""
    
    print("=== String Manipulation Challenges ===")
    
    print("1. Remove vowels from a string:")
    text = "Hello World"
    print(f"Input: '{text}'")
    print("One-liner: ''.join([c for c in text if c.lower() not in 'aeiou'])")
    result1 = ''.join([c for c in text if c.lower() not in 'aeiou'])
    print(f"Result: '{result1}'")
    print()
    
    print("2. Reverse words in a sentence:")
    sentence = "Python is awesome"
    print(f"Input: '{sentence}'")
    print("One-liner: ' '.join(sentence.split()[::-1])")
    result2 = ' '.join(sentence.split()[::-1])
    print(f"Result: '{result2}'")
    print()
    
    print("3. Count each character in a string:")
    text = "hello"
    print(f"Input: '{text}'")
    print("One-liner: {char: text.count(char) for char in set(text)}")
    result3 = {char: text.count(char) for char in set(text)}
    print(f"Result: {result3}")
    print()
    
    print("4. Create acronym from phrase:")
    phrase = "Artificial Intelligence Machine Learning"
    print(f"Input: '{phrase}'")
    print("One-liner: ''.join([word[0].upper() for word in phrase.split()])")
    result4 = ''.join([word[0].upper() for word in phrase.split()])
    print(f"Result: '{result4}'")
    print()

def interactive_challenges():
    """Interactive one-liner challenges for practice"""
    
    print("=== Interactive One-Liner Challenges ===")
    
    challenges = [
        {
            "description": "Create squares of numbers 1-5",
            "solution": "[i**2 for i in range(1, 6)]",
            "expected": [1, 4, 9, 16, 25]
        },
        {
            "description": "Filter words longer than 4 characters",
            "data": ['cat', 'elephant', 'dog', 'tiger'],
            "solution": "[word for word in ['cat', 'elephant', 'dog', 'tiger'] if len(word) > 4]",
            "expected": ['elephant', 'tiger']
        },
        {
            "description": "Convert temperatures from Celsius to Fahrenheit",
            "data": [0, 25, 100],
            "solution": "[c * 9/5 + 32 for c in [0, 25, 100]]",
            "expected": [32.0, 77.0, 212.0]
        },
        {
            "description": "Get unique characters from a string",
            "data": "programming",
            "solution": "list(set('programming'))",
            "expected": "unique characters (order may vary)"
        },
        {
            "description": "Sum of squares using reduce",
            "data": [1, 2, 3, 4],
            "solution": "reduce(lambda x, y: x + y**2, [1, 2, 3, 4], 0)",
            "expected": 30
        }
    ]
    
    score = 0
    total = len(challenges)
    
    for i, challenge in enumerate(challenges, 1):
        print(f"\n--- Challenge {i} ---")
        print(f"Task: {challenge['description']}")
        
        if 'data' in challenge:
            print(f"Data: {challenge['data']}")
        
        print(f"Expected result: {challenge['expected']}")
        
        user_answer = input("Enter your one-liner solution: ").strip()
        
        if user_answer == challenge['solution']:
            print("✅ Correct! Great job!")
            score += 1
        else:
            print("❌ Not quite right.")
            print(f"Correct solution: {challenge['solution']}")
        
        try:
            if 'data' not in challenge:
                actual_result = eval(challenge['solution'])
            else:
                actual_result = eval(challenge['solution'])
            print(f"Actual result: {actual_result}")
        except Exception as e:
            print(f"Error testing solution: {e}")
    
    print(f"\n=== Final Score: {score}/{total} ===")
    if score == total:
        print("🎉 Perfect score! You're a one-liner master!")
    elif score >= total * 0.7:
        print("👍 Great job! You're getting the hang of one-liners!")
    else:
        print("💪 Keep practicing! One-liners take time to master.")

def one_liner_reference():
    """Provides a reference guide for one-liner techniques"""
    
    print("=== One-Liner Reference Guide ===")
    
    techniques = {
        "List Comprehensions": [
            "[expression for item in iterable]",
            "[expression for item in iterable if condition]",
            "[expression if condition else alternative for item in iterable]"
        ],
        "Map Function": [
            "list(map(function, iterable))",
            "list(map(lambda x: expression, iterable))"
        ],
        "Filter Function": [
            "list(filter(function, iterable))",
            "list(filter(lambda x: condition, iterable))"
        ],
        "Reduce Function": [
            "reduce(function, iterable)",
            "reduce(lambda x, y: expression, iterable, initial_value)"
        ],
        "Dictionary Comprehensions": [
            "{key: value for item in iterable}",
            "{key: value for item in iterable if condition}"
        ],
        "Set Comprehensions": [
            "{expression for item in iterable}",
            "{expression for item in iterable if condition}"
        ],
        "Generator Expressions": [
            "(expression for item in iterable)",
            "sum(expression for item in iterable if condition)"
        ]
    }
    
    for technique, examples in techniques.items():
        print(f"\n{technique}:")
        for example in examples:
            print(f"  • {example}")

def main():
    """Main function to run the one-liner challenges program"""
    
    while True:
        print("\n" + "="*60)
        print("🎯 ONE-LINER CHALLENGES 🎯")
        print("="*60)
        print("1. Basic Examples (from requirements)")
        print("2. List Comprehension Challenges")
        print("3. Lambda Function Challenges")
        print("4. Map, Filter, Reduce Challenges")
        print("5. Advanced Challenges")
        print("6. String Manipulation Challenges")
        print("7. Interactive Practice")
        print("8. One-Liner Reference Guide")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            demonstrate_basic_examples()
        elif choice == "2":
            demonstrate_list_comprehension_challenges()
        elif choice == "3":
            demonstrate_lambda_challenges()
        elif choice == "4":
            demonstrate_map_filter_reduce_challenges()
        elif choice == "5":
            demonstrate_advanced_challenges()
        elif choice == "6":
            demonstrate_string_challenges()
        elif choice == "7":
            interactive_challenges()
        elif choice == "8":
            one_liner_reference()
        elif choice == "9":
            print("Happy coding with one-liners! 🐍✨")
            break
        else:
            print("Invalid choice! Please enter 1-9.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
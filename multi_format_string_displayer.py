
def demonstrate_basic_example():
    """Demonstrates the basic example from requirements"""
    
    print("=== Basic Example from Requirements ===")
    
    name = "Alice"
    age = 28
    city = "Delhi"
    
    print(f"Variables:")
    print(f"name = \"{name}\"")
    print(f"age = {age}")
    print(f"city = \"{city}\"")
    print()
    
    expected_output = "My name is Alice, I am 28 years old, and I live in Delhi."
    print(f"Expected Output: {expected_output}")
    print()
    
    print("1. Using % formatting:")
    print("Code: \"My name is %s, I am %d years old, and I live in %s.\" % (name, age, city)")
    result1 = "My name is %s, I am %d years old, and I live in %s." % (name, age, city)
    print(f"Output: {result1}")
    print()
    
    print("2. Using .format() method:")
    print("Code: \"My name is {}, I am {} years old, and I live in {}.\".format(name, age, city)")
    result2 = "My name is {}, I am {} years old, and I live in {}.".format(name, age, city)
    print(f"Output: {result2}")
    print()
    
    print("3. Using f-strings:")
    print("Code: f\"My name is {name}, I am {age} years old, and I live in {city}.\"")
    result3 = f"My name is {name}, I am {age} years old, and I live in {city}."
    print(f"Output: {result3}")
    print()
    
    print("=== Verification ===")
    print(f"All outputs match: {result1 == result2 == result3 == expected_output}")

def demonstrate_advanced_formatting():
    """Demonstrates advanced formatting options for each method"""
    
    print("\n=== Advanced Formatting Examples ===")
    
    name = "Bob"
    salary = 75000.456
    percentage = 0.8567
    
    print(f"Variables:")
    print(f"name = \"{name}\"")
    print(f"salary = {salary}")
    print(f"percentage = {percentage}")
    print()
    
    print("1. Number Formatting:")
    print("   % formatting:")
    print("   Code: \"%s earns $%.2f, which is %.1f%% above average.\" % (name, salary, percentage * 100)")
    result1 = "%s earns $%.2f, which is %.1f%% above average." % (name, salary, percentage * 100)
    print(f"   Output: {result1}")
    
    print("\n   .format() method:")
    print("   Code: \"{} earns ${:.2f}, which is {:.1f}% above average.\".format(name, salary, percentage * 100)")
    result2 = "{} earns ${:.2f}, which is {:.1f}% above average.".format(name, salary, percentage * 100)
    print(f"   Output: {result2}")
    
    print("\n   f-strings:")
    print("   Code: f\"{name} earns ${salary:.2f}, which is {percentage * 100:.1f}% above average.\"")
    result3 = f"{name} earns ${salary:.2f}, which is {percentage * 100:.1f}% above average."
    print(f"   Output: {result3}")
    print()

def demonstrate_positioning_and_naming():
    """Demonstrates positional and named arguments"""
    
    print("=== Positioning and Named Arguments ===")
    
    first = "John"
    last = "Doe"
    age = 35
    
    print(f"Variables: first=\"{first}\", last=\"{last}\", age={age}")
    print()
    
    print("1. Positional Arguments with .format():")
    print("   Code: \"Hello {1} {0}, you are {2} years old.\".format(first, last, age)")
    result1 = "Hello {1} {0}, you are {2} years old.".format(first, last, age)
    print(f"   Output: {result1}")
    print()
    
    print("2. Named Arguments with .format():")
    print("   Code: \"Hello {last} {first}, you are {age} years old.\".format(first=first, last=last, age=age)")
    result2 = "Hello {last} {first}, you are {age} years old.".format(first=first, last=last, age=age)
    print(f"   Output: {result2}")
    print()
    
    print("3. f-strings with expressions:")
    print("   Code: f\"Hello {last.upper()} {first.lower()}, you are {age + 5} years old in 5 years.\"")
    result3 = f"Hello {last.upper()} {first.lower()}, you are {age + 5} years old in 5 years."
    print(f"   Output: {result3}")
    print()

def demonstrate_alignment_and_padding():
    """Demonstrates text alignment and padding"""
    
    print("=== Alignment and Padding ===")
    
    items = [
        ("Apple", 1.50, 5),
        ("Banana", 0.75, 12),
        ("Orange", 2.00, 3)
    ]
    
    print("Creating a formatted table:")
    print()
    
    print("Using % formatting:")
    print("%-10s %8s %5s" % ("Item", "Price", "Qty"))
    print("-" * 25)
    for item, price, qty in items:
        print("%-10s $%7.2f %5d" % (item, price, qty))
    print()
    
    print("Using .format() method:")
    print("{:<10} {:>8} {:>5}".format("Item", "Price", "Qty"))
    print("-" * 25)
    for item, price, qty in items:
        print("{:<10} ${:>7.2f} {:>5}".format(item, price, qty))
    print()
    
    print("Using f-strings:")
    print(f"{'Item':<10} {'Price':>8} {'Qty':>5}")
    print("-" * 25)
    for item, price, qty in items:
        print(f"{item:<10} ${price:>7.2f} {qty:>5}")
    print()

def demonstrate_special_cases():
    """Demonstrates special formatting cases"""
    
    print("=== Special Cases ===")
    
    from datetime import datetime
    now = datetime.now()
    
    print("1. Date Formatting:")
    print("   % formatting:")
    result1 = "Today is %s" % now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"   Output: {result1}")
    
    print("\n   .format() method:")
    result2 = "Today is {}".format(now.strftime("%Y-%m-%d %H:%M:%S"))
    print(f"   Output: {result2}")
    
    print("\n   f-strings:")
    result3 = f"Today is {now:%Y-%m-%d %H:%M:%S}"
    print(f"   Output: {result3}")
    print()
    
    print("2. Dictionary Formatting:")
    person = {"name": "Charlie", "age": 30, "job": "Engineer"}
    
    print("   % formatting:")
    result4 = "%(name)s is %(age)d years old and works as an %(job)s." % person
    print(f"   Output: {result4}")
    
    print("\n   .format() method:")
    result5 = "{name} is {age} years old and works as an {job}.".format(**person)
    print(f"   Output: {result5}")
    
    print("\n   f-strings:")
    result6 = f"{person['name']} is {person['age']} years old and works as an {person['job']}."
    print(f"   Output: {result6}")
    print()

def performance_comparison():
    """Compares performance of different formatting methods"""
    
    print("=== Performance Comparison ===")
    
    import time
    
    name = "Performance"
    age = 100
    city = "Test City"
    iterations = 100000
    
    start_time = time.time()
    for _ in range(iterations):
        result = "My name is %s, I am %d years old, and I live in %s." % (name, age, city)
    percent_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(iterations):
        result = "My name is {}, I am {} years old, and I live in {}.".format(name, age, city)
    format_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(iterations):
        result = f"My name is {name}, I am {age} years old, and I live in {city}."
    fstring_time = time.time() - start_time
    
    print(f"Performance test ({iterations:,} iterations):")
    print(f"% formatting:  {percent_time:.4f} seconds")
    print(f".format():     {format_time:.4f} seconds")
    print(f"f-strings:     {fstring_time:.4f} seconds")
    print()
    print("Speed ranking (fastest to slowest):")
    
    times = [("% formatting", percent_time), (".format()", format_time), ("f-strings", fstring_time)]
    times.sort(key=lambda x: x[1])
    
    for i, (method, time_taken) in enumerate(times, 1):
        print(f"{i}. {method}: {time_taken:.4f}s")

def interactive_formatter():
    """Interactive tool to practice different formatting methods"""
    
    print("\n=== Interactive Formatter ===")
    
    name = input("Enter a name: ").strip()
    try:
        age = int(input("Enter an age: ").strip())
    except ValueError:
        age = 25
        print("Invalid age, using 25 as default")
    
    city = input("Enter a city: ").strip()
    
    if not name:
        name = "Anonymous"
    if not city:
        city = "Unknown City"
    
    print(f"\nUsing: name=\"{name}\", age={age}, city=\"{city}\"")
    print()
    
    templates = [
        "My name is {name}, I am {age} years old, and I live in {city}.",
        "Hello! I'm {name} from {city}, and I'm {age} years old.",
        "{name} ({age}) lives in {city}.",
        "City: {city}, Resident: {name}, Age: {age}"
    ]
    
    for i, template in enumerate(templates, 1):
        print(f"Template {i}: {template}")
        print()
        
        print("  % formatting:")
        percent_template = template.replace("{name}", "%s").replace("{age}", "%d").replace("{city}", "%s")
        percent_result = percent_template % (name, age, city)
        print(f"    \"{percent_template}\" % (name, age, city)")
        print(f"    Result: {percent_result}")
        
        print("\n  .format() method:")
        format_template = template.replace("{name}", "{}").replace("{age}", "{}").replace("{city}", "{}")
        format_result = format_template.format(name, age, city)
        print(f"    \"{format_template}\".format(name, age, city)")
        print(f"    Result: {format_result}")
        
        print("\n  f-strings:")
        fstring_result = template.format(name=name, age=age, city=city)
        print(f"    f\"{template}\"")
        print(f"    Result: {fstring_result}")
        print("-" * 50)

def formatting_reference():
    """Provides a reference guide for string formatting"""
    
    print("=== String Formatting Reference ===")
    
    reference = {
        "% Formatting (Old Style)": [
            "%s - String",
            "%d - Integer", 
            "%f - Float",
            "%.2f - Float with 2 decimal places",
            "%10s - String with minimum width 10",
            "%-10s - Left-aligned string with width 10",
            "%(name)s - Named placeholder from dictionary"
        ],
        ".format() Method": [
            "{} - Positional argument",
            "{0} - Positional argument by index",
            "{name} - Named argument",
            "{:.2f} - Float with 2 decimal places",
            "{:10} - Minimum width 10",
            "{:<10} - Left-aligned with width 10",
            "{:>10} - Right-aligned with width 10",
            "{:^10} - Center-aligned with width 10"
        ],
        "f-strings (Modern)": [
            "f'{variable}' - Variable interpolation",
            "f'{variable:.2f}' - Float with 2 decimal places",
            "f'{variable:10}' - Minimum width 10",
            "f'{variable:<10}' - Left-aligned with width 10",
            "f'{expression}' - Any valid Python expression",
            "f'{datetime_obj:%Y-%m-%d}' - Date formatting",
            "f'{number:,}' - Thousand separators"
        ]
    }
    
    for method, examples in reference.items():
        print(f"\n{method}:")
        for example in examples:
            print(f"  • {example}")

def main():
    """Main function to run the multi-format string displayer"""
    
    while True:
        print("\n" + "="*60)
        print("📝 MULTI-FORMAT STRING DISPLAYER 📝")
        print("="*60)
        print("1. Basic Example (from requirements)")
        print("2. Advanced Formatting")
        print("3. Positioning and Named Arguments")
        print("4. Alignment and Padding")
        print("5. Special Cases")
        print("6. Performance Comparison")
        print("7. Interactive Formatter")
        print("8. Formatting Reference")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            demonstrate_basic_example()
        elif choice == "2":
            demonstrate_advanced_formatting()
        elif choice == "3":
            demonstrate_positioning_and_naming()
        elif choice == "4":
            demonstrate_alignment_and_padding()
        elif choice == "5":
            demonstrate_special_cases()
        elif choice == "6":
            performance_comparison()
        elif choice == "7":
            interactive_formatter()
        elif choice == "8":
            formatting_reference()
        elif choice == "9":
            print("Happy formatting! 🐍✨")
            break
        else:
            print("Invalid choice! Please enter 1-9.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
employees = [
    ("Alice", 50000, "Engineering"),
    ("Bob", 60000, "Marketing"),
    ("Carol", 55000, "Engineering"),
    ("David", 45000, "Sales")
]

def display_employees(employee_list, title="Employees"):
    """Helper function to display employees in a formatted table"""
    print(f"=== {title} ===")
    print(f"{'Name':<10} {'Salary':<10} {'Department'}")
    print("-" * 40)
    for name, salary, department in employee_list:
        print(f"{name:<10} ${salary:<9,} {department}")
    print()

def sort_by_salary():
    """Sort the list of employees by salary in both ascending and descending order"""
    print("=== Task 1: Sort by Salary ===")
    print()
    
    display_employees(employees, "Original Employees")
    
    employees_salary_asc = sorted(employees, key=lambda emp: emp[1])
    display_employees(employees_salary_asc, "Sorted by Salary (Ascending)")
    
    employees_salary_desc = sorted(employees, key=lambda emp: emp[1], reverse=True)
    display_employees(employees_salary_desc, "Sorted by Salary (Descending)")
    
    print("Alternative method using index notation:")
    employees_salary_asc_alt = sorted(employees, key=lambda emp: emp[1])
    print("Ascending by salary (using index):")
    for i, (name, salary, dept) in enumerate(employees_salary_asc_alt):
        print(f"  {i+1}. {name}: ${salary:,}")
    print()

def sort_by_department_then_salary():
    """Sort by department name alphabetically, then by salary within each department"""
    print("=== Task 2: Sort by Department, Then by Salary ===")
    print()
    
    display_employees(employees, "Original Employees")
    
    employees_dept_salary = sorted(employees, key=lambda emp: (emp[2], emp[1]))
    display_employees(employees_dept_salary, "Sorted by Department, then Salary")
    
    employees_dept_desc = sorted(employees, key=lambda emp: (emp[2], -emp[1]))
    display_employees(employees_dept_desc, "Sorted by Department, then Salary (Desc)")
    
    print("Grouped by Department:")
    current_dept = None
    for name, salary, dept in employees_dept_salary:
        if dept != current_dept:
            print(f"\n  {dept} Department:")
            current_dept = dept
        print(f"    {name}: ${salary:,}")
    print()

def create_reversed_list():
    """Reverse the order of the original list without modifying the original"""
    print("=== Task 3: Create a Reversed List ===")
    print()
    
    display_employees(employees, "Original Employees")
    
    employees_reversed_1 = list(reversed(employees))
    display_employees(employees_reversed_1, "Reversed using reversed()")
    
    employees_reversed_2 = employees[::-1]
    display_employees(employees_reversed_2, "Reversed using slice [::-1]")
    
    employees_copy = employees.copy()
    employees_copy.reverse()
    display_employees(employees_copy, "Reversed using .reverse() on copy")
    
    print("Verification - Original list unchanged:")
    display_employees(employees, "Original Employees (Unchanged)")
    
    print("All reversal methods produce the same result:")
    print(f"Method 1 == Method 2: {employees_reversed_1 == employees_reversed_2}")
    print(f"Method 2 == Method 3: {employees_reversed_2 == employees_copy}")
    print()

def sort_by_name_length():
    """Sort employees based on the length of their names"""
    print("=== Task 4: Sort by Name Length ===")
    print()
    
    display_employees(employees, "Original Employees")
    
    employees_name_len_asc = sorted(employees, key=lambda emp: len(emp[0]))
    display_employees(employees_name_len_asc, "Sorted by Name Length (Ascending)")
    
    employees_name_len_desc = sorted(employees, key=lambda emp: len(emp[0]), reverse=True)
    display_employees(employees_name_len_desc, "Sorted by Name Length (Descending)")
    
    employees_name_len_alpha = sorted(employees, key=lambda emp: (len(emp[0]), emp[0]))
    display_employees(employees_name_len_alpha, "Sorted by Name Length, then Alphabetically")
    
    print("Name Lengths:")
    for name, salary, dept in employees_name_len_asc:
        print(f"  {name}: {len(name)} characters")
    print()

def demonstrate_sorted_vs_sort():
    """Use .sort() when modifying original list and sorted() when creating new sorted list"""
    print("=== Task 5: Use sorted() vs .sort() Appropriately ===")
    print()
    
    print("1. Using sorted() - Creates new list, original unchanged:")
    print("Original employees:")
    display_employees(employees, "Original")
    
    new_sorted_list = sorted(employees, key=lambda emp: emp[0])  # Sort by name
    print("After new_sorted_list = sorted(employees, key=lambda emp: emp[0]):")
    display_employees(new_sorted_list, "New Sorted List (by Name)")
    display_employees(employees, "Original (Unchanged)")
    
    print("2. Using .sort() - Modifies original list:")
    employees_copy_for_sort = employees.copy()
    print("Before .sort():")
    display_employees(employees_copy_for_sort, "Copy Before Sort")
    
    employees_copy_for_sort.sort(key=lambda emp: emp[1])  # Sort by salary
    print("After employees_copy.sort(key=lambda emp: emp[1]):")
    display_employees(employees_copy_for_sort, "Copy After Sort (by Salary)")
    
    print("3. Best Practices:")
    print()
    
    print("Use sorted() when:")
    print("  • You need to keep the original list unchanged")
    print("  • You want to create multiple sorted versions")
    print("  • Working with immutable sequences (tuples)")
    print()
    
    sorted_by_name = sorted(employees, key=lambda emp: emp[0])
    sorted_by_salary = sorted(employees, key=lambda emp: emp[1])
    sorted_by_dept = sorted(employees, key=lambda emp: emp[2])
    
    print("Multiple sorted versions from same original:")
    display_employees(sorted_by_name, "By Name")
    display_employees(sorted_by_salary, "By Salary")
    display_employees(sorted_by_dept, "By Department")
    
    print("Use .sort() when:")
    print("  • You want to permanently change the list order")
    print("  • Memory efficiency is important (no new list created)")
    print("  • You're done with the original order")
    print()
    
    print("4. Memory Efficiency Comparison:")
    import sys
    
    large_list = [(f"Employee_{i}", 30000 + i * 1000, "Dept") for i in range(1000)]
    print(f"Original list size: {sys.getsizeof(large_list)} bytes")
    
    sorted_list = sorted(large_list, key=lambda x: x[1])
    print(f"New sorted list size: {sys.getsizeof(sorted_list)} bytes")
    print(f"Total memory usage: {sys.getsizeof(large_list) + sys.getsizeof(sorted_list)} bytes")
    
    large_list_copy = large_list.copy()
    large_list_copy.sort(key=lambda x: x[1])
    print(f"In-place sorted list size: {sys.getsizeof(large_list_copy)} bytes")
    print("Memory saved by using .sort(): 50% (no duplicate list)")
    print()

def advanced_sorting_examples():
    """Demonstrate advanced sorting techniques"""
    print("=== Advanced Sorting Examples ===")
    print()
    
    print("1. Complex Sorting Criteria:")
    
    complex_sort = sorted(employees, key=lambda emp: (emp[2], -emp[1], emp[0]))
    display_employees(complex_sort, "Dept (asc), Salary (desc), Name (asc)")
    
    def employee_priority(emp):
        name, salary, dept = emp
        if dept == "Engineering":
            return (1, -salary)  # Higher salary first within Engineering
        else:
            return (2, -salary)  # Then others by salary
    
    priority_sorted = sorted(employees, key=employee_priority)
    display_employees(priority_sorted, "Engineering First, then by Salary")
    
    print("2. Using operator.itemgetter:")
    from operator import itemgetter
    
    itemgetter_sorted = sorted(employees, key=itemgetter(2, 1))
    display_employees(itemgetter_sorted, "Using itemgetter(2, 1)")
    
    print("3. Performance Comparison (1000 iterations):")
    import time
    
    start_time = time.time()
    for _ in range(1000):
        sorted(employees, key=lambda emp: (emp[2], emp[1]))
    lambda_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(1000):
        sorted(employees, key=itemgetter(2, 1))
    itemgetter_time = time.time() - start_time
    
    print(f"  Lambda function: {lambda_time:.6f} seconds")
    print(f"  itemgetter:      {itemgetter_time:.6f} seconds")
    print(f"  itemgetter is {lambda_time/itemgetter_time:.1f}x faster")
    print()

def practical_sorting_applications():
    """Show practical applications of sorting"""
    print("=== Practical Sorting Applications ===")
    print()
    
    print("1. Finding Top Performers:")
    top_earners = sorted(employees, key=lambda emp: emp[1], reverse=True)[:2]
    print("Top 2 earners:")
    for i, (name, salary, dept) in enumerate(top_earners, 1):
        print(f"  {i}. {name}: ${salary:,} ({dept})")
    print()
    
    print("2. Department Analysis:")
    by_dept = sorted(employees, key=lambda emp: emp[2])
    dept_groups = {}
    for name, salary, dept in by_dept:
        if dept not in dept_groups:
            dept_groups[dept] = []
        dept_groups[dept].append((name, salary))
    
    for dept, workers in dept_groups.items():
        avg_salary = sum(salary for _, salary in workers) / len(workers)
        print(f"  {dept}: {len(workers)} employees, avg salary: ${avg_salary:,.0f}")
    print()
    
    print("3. Salary Distribution:")
    salary_ranges = {
        "Entry Level ($40k-$49k)": [],
        "Mid Level ($50k-$59k)": [],
        "Senior Level ($60k+)": []
    }
    
    for name, salary, dept in employees:
        if salary < 50000:
            salary_ranges["Entry Level ($40k-$49k)"].append(name)
        elif salary < 60000:
            salary_ranges["Mid Level ($50k-$59k)"].append(name)
        else:
            salary_ranges["Senior Level ($60k+)"].append(name)
    
    for range_name, workers in salary_ranges.items():
        print(f"  {range_name}: {workers}")
    print()
    
    print("4. Employee Directory (Alphabetical):")
    directory = sorted(employees, key=lambda emp: emp[0])
    for name, salary, dept in directory:
        print(f"  {name:<10} | {dept:<12} | ${salary:,}")
    print()

def interactive_sorting_demo():
    """Interactive demonstration of different sorting options"""
    print("=== Interactive Sorting Demo ===")
    print()
    
    sorting_options = {
        "1": ("Name (A-Z)", lambda emp: emp[0]),
        "2": ("Name (Z-A)", lambda emp: emp[0], True),
        "3": ("Salary (Low to High)", lambda emp: emp[1]),
        "4": ("Salary (High to Low)", lambda emp: emp[1], True),
        "5": ("Department", lambda emp: emp[2]),
        "6": ("Name Length", lambda emp: len(emp[0])),
        "7": ("Department + Salary", lambda emp: (emp[2], emp[1]))
    }
    
    print("Available sorting options:")
    for key, option in sorting_options.items():
        print(f"  {key}. {option[0]}")
    print()
    
    demo_sorts = ["1", "4", "7"]
    
    for sort_key in demo_sorts:
        option = sorting_options[sort_key]
        reverse = len(option) > 2 and option[2]
        sorted_list = sorted(employees, key=option[1], reverse=reverse)
        display_employees(sorted_list, f"Demo: {option[0]}")

def main():
    print("👥 EMPLOYEE SORTING & REVERSING OPERATIONS 👥")
    print("=" * 70)
    print()
    
    print("Initial Employee Data:")
    display_employees(employees, "All Employees")
    
    sort_by_salary()
    sort_by_department_then_salary()
    create_reversed_list()
    sort_by_name_length()
    demonstrate_sorted_vs_sort()
    advanced_sorting_examples()
    practical_sorting_applications()
    interactive_sorting_demo()
    
    print("=== Summary & Best Practices ===")
    print()
    print("Key Takeaways:")
    print()
    print("1. sorted() vs .sort():")
    print("   • sorted(): Creates new list, original unchanged")
    print("   • .sort(): Modifies original list in place, more memory efficient")
    print()
    print("2. Key Functions:")
    print("   • lambda functions for simple extractions")
    print("   • operator.itemgetter() for better performance")
    print("   • Custom functions for complex logic")
    print()
    print("3. Multiple Criteria:")
    print("   • Use tuples in key function: (primary, secondary, ...)")
    print("   • Use negative values for descending: -salary")
    print("   • Mix ascending/descending as needed")
    print()
    print("4. Performance Tips:")
    print("   • itemgetter() is faster than lambda for simple field access")
    print("   • .sort() uses less memory than sorted()")
    print("   • Avoid repeated sorting - sort once with multiple criteria")
    print()
    print("5. Common Patterns:")
    print("   • Top N: sorted(data, key=..., reverse=True)[:N]")
    print("   • Grouping: Sort first, then group consecutive items")
    print("   • Ranking: Use enumerate() after sorting")
    print()

if __name__ == "__main__":
    main()

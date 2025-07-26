students = [
    (101, "Alice", 85, 20),
    (102, "Bob", 92, 19),
    (103, "Carol", 78, 21),
    (104, "David", 88, 20)
]

def find_highest_grade_student(student_list):
    """Find the student with the highest grade"""
    if not student_list:
        return None
    
    highest_student = student_list[0]
    for student in student_list:
        if student[2] > highest_student[2]:  # Compare grades (index 2)
            highest_student = student
    
    return highest_student

def create_name_grade_list(student_list):
    """Create a list of (name, grade) tuples"""
    name_grade_list = []
    for student in student_list:
        name_grade_tuple = (student[1], student[2])  # name (index 1), grade (index 2)
        name_grade_list.append(name_grade_tuple)
    
    return name_grade_list

def demonstrate_tuple_immutability():
    """Demonstrate that tuples are immutable"""
    print("=== Demonstrating Tuple Immutability ===")
    print()
    
    student = students[0]  # Alice's record
    print(f"Original student record: {student}")
    print(f"Student ID: {student[0]}, Name: {student[1]}, Grade: {student[2]}, Age: {student[3]}")
    print()
    
    print("Attempting to change Alice's grade from 85 to 95...")
    try:
        student[2] = 95  # Try to change the grade
        print("Grade changed successfully!")
    except TypeError as e:
        print(f"Error: {e}")
        print("❌ Cannot modify tuple elements because tuples are immutable!")
    
    print()
    print("Why tuples are preferred for student records:")
    print("• Data Integrity: Prevents accidental modification of student records")
    print("• Immutability: Ensures data consistency across the program")
    print("• Memory Efficiency: Tuples use less memory than lists")
    print("• Hashable: Can be used as dictionary keys or in sets")
    print("• Performance: Faster access and iteration compared to lists")
    print("• Predictability: Structure remains constant throughout program execution")

def display_all_students(student_list):
    """Display all students in a formatted table"""
    print("=== All Student Records ===")
    print(f"{'ID':<5} {'Name':<10} {'Grade':<7} {'Age':<5}")
    print("-" * 30)
    for student in student_list:
        print(f"{student[0]:<5} {student[1]:<10} {student[2]:<7} {student[3]:<5}")
    print()

def main():
    print("🎓 STUDENT RECORDS MANAGEMENT 🎓")
    print("=" * 50)
    print()
    
    display_all_students(students)
    
    print("=== Task 1: Find Student with Highest Grade ===")
    highest_student = find_highest_grade_student(students)
    if highest_student:
        print(f"Student with highest grade: {highest_student}")
        print(f"🏆 {highest_student[1]} has the highest grade of {highest_student[2]}!")
    else:
        print("No students found.")
    print()
    
    print("=== Task 2: Create Name-Grade List ===")
    name_grade_list = create_name_grade_list(students)
    print("Name-Grade pairs:")
    for name_grade in name_grade_list:
        print(f"  {name_grade}")
    print()
    
    print("Same result using list comprehension:")
    name_grade_comprehension = [(student[1], student[2]) for student in students]
    print(f"  {name_grade_comprehension}")
    print()
    
    demonstrate_tuple_immutability()
    print()
    
    print("=== Additional Tuple Operations ===")
    
    print("1. Tuple Unpacking:")
    student_id, name, grade, age = students[1]  # Bob's record
    print(f"   Unpacked Bob's data: ID={student_id}, Name={name}, Grade={grade}, Age={age}")
    print()
    
    print("2. Tuple Methods:")
    alice_record = students[0]
    print(f"   Alice's record: {alice_record}")
    print(f"   Count of value 85: {alice_record.count(85)}")
    print(f"   Index of 'Alice': {alice_record.index('Alice')}")
    print()
    
    print("3. Nested Tuples (Advanced Records):")
    advanced_students = [
        (101, ("Alice", "Johnson"), (85, 90, 88), 20),  # (id, (first, last), (test1, test2, test3), age)
        (102, ("Bob", "Smith"), (92, 89, 94), 19)
    ]
    for student in advanced_students:
        student_id, full_name, grades, age = student
        first_name, last_name = full_name
        avg_grade = sum(grades) / len(grades)
        print(f"   {first_name} {last_name}: Average grade = {avg_grade:.1f}")
    print()
    
    print("4. Sorting Students by Grade:")
    sorted_students = sorted(students, key=lambda student: student[2], reverse=True)
    print("   Students sorted by grade (highest to lowest):")
    for rank, student in enumerate(sorted_students, 1):
        print(f"   {rank}. {student[1]}: {student[2]}")
    print()
    
    print("5. Filtering Students:")
    high_achievers = [student for student in students if student[2] >= 85]
    print("   High achievers (grade >= 85):")
    for student in high_achievers:
        print(f"   • {student[1]}: {student[2]}")
    print()

if __name__ == "__main__":
    main()

school = {
    "Math": {
        "teacher": "Mr. Smith",
        "students": [("Alice", 85), ("Bob", 92), ("Carol", 78)]
    },
    "Science": {
        "teacher": "Ms. Johnson",
        "students": [("David", 88), ("Eve", 94), ("Frank", 82)]
    }
}

def display_school_overview(school_data):
    """Display a comprehensive overview of the school"""
    print("=== SCHOOL OVERVIEW ===")
    print()
    
    total_classes = len(school_data)
    total_students = sum(len(class_info["students"]) for class_info in school_data.values())
    
    print(f"📚 Total Classes: {total_classes}")
    print(f"👥 Total Students: {total_students}")
    print()
    
    print(f"{'Class':<10} {'Teacher':<15} {'Students':<10} {'Avg Grade'}")
    print("-" * 50)
    
    for class_name, class_info in school_data.items():
        teacher = class_info["teacher"]
        student_count = len(class_info["students"])
        
        grades = [grade for _, grade in class_info["students"]]
        avg_grade = sum(grades) / len(grades) if grades else 0
        
        print(f"{class_name:<10} {teacher:<15} {student_count:<10} {avg_grade:.1f}")
    
    print()

def print_teacher_names(school_data):
    """Iterate through all classes and print the name of each teacher"""
    print("=== Task 1: Print Teacher Names ===")
    print()
    
    print("Teachers in our school:")
    
    for class_name, class_info in school_data.items():
        teacher_name = class_info["teacher"]
        print(f"📖 {class_name}: {teacher_name}")
    
    print()
    
    print("Alternative - All teachers list:")
    teachers = [class_info["teacher"] for class_info in school_data.values()]
    for i, teacher in enumerate(teachers, 1):
        print(f"   {i}. {teacher}")
    
    print()
    
    print("Teacher-Class Assignment:")
    for class_name, class_info in school_data.items():
        teacher = class_info["teacher"]
        student_count = len(class_info["students"])
        print(f"   {teacher} teaches {class_name} with {student_count} students")
    
    print()

def calculate_class_averages(school_data):
    """Calculate and display the average grade for each class"""
    print("=== Task 2: Calculate Class Average Grades ===")
    print()
    
    class_averages = {}
    
    print("Class Performance Report:")
    print(f"{'Class':<10} {'Teacher':<15} {'Students':<10} {'Average':<8} {'Status'}")
    print("-" * 60)
    
    for class_name, class_info in school_data.items():
        teacher = class_info["teacher"]
        students = class_info["students"]
        
        grades = [grade for _, grade in students]
        average_grade = sum(grades) / len(grades) if grades else 0
        
        class_averages[class_name] = average_grade
        
        if average_grade >= 90:
            status = "Excellent"
        elif average_grade >= 80:
            status = "Good"
        elif average_grade >= 70:
            status = "Average"
        else:
            status = "Needs Improvement"
        
        print(f"{class_name:<10} {teacher:<15} {len(students):<10} {average_grade:<8.1f} {status}")
    
    print()
    
    print("Detailed Grade Analysis:")
    for class_name, class_info in school_data.items():
        students = class_info["students"]
        grades = [grade for _, grade in students]
        
        print(f"\n📚 {class_name} Class:")
        print(f"   Teacher: {class_info['teacher']}")
        print(f"   Students: {len(students)}")
        print(f"   Average Grade: {class_averages[class_name]:.1f}")
        print(f"   Highest Grade: {max(grades)}")
        print(f"   Lowest Grade: {min(grades)}")
        print(f"   Grade Range: {max(grades) - min(grades)} points")
        
        print("   Student Grades:")
        for name, grade in students:
            print(f"     • {name}: {grade}")
    
    print()
    return class_averages

def find_top_student(school_data):
    """Identify the student with the highest grade across all classes"""
    print("=== Task 3: Find Top Student Across All Classes ===")
    print()
    
    all_students = []
    
    for class_name, class_info in school_data.items():
        for name, grade in class_info["students"]:
            all_students.append((name, grade, class_name))
    
    if not all_students:
        print("No students found in the school.")
        return None
    
    top_student = max(all_students, key=lambda student: student[1])
    top_name, top_grade, top_class = top_student
    
    print("🏆 TOP STUDENT ANALYSIS")
    print(f"   Name: {top_name}")
    print(f"   Grade: {top_grade}")
    print(f"   Class: {top_class}")
    print(f"   Teacher: {school_data[top_class]['teacher']}")
    print()
    
    print("🥇 TOP 3 STUDENTS ACROSS ALL CLASSES:")
    sorted_students = sorted(all_students, key=lambda x: x[1], reverse=True)
    
    for rank, (name, grade, class_name) in enumerate(sorted_students[:3], 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        print(f"   {medal} {rank}. {name}: {grade} points ({class_name})")
    
    print()
    
    print("🌟 TOP PERFORMER BY CLASS:")
    for class_name, class_info in school_data.items():
        students = class_info["students"]
        if students:
            top_in_class = max(students, key=lambda x: x[1])
            name, grade = top_in_class
            print(f"   {class_name}: {name} with {grade} points")
    
    print()
    return top_student

def demonstrate_unpacking(school_data):
    """Use tuple unpacking to extract and work with student names and grades"""
    print("=== Task 4: Use Unpacking ===")
    print()
    
    print("Demonstrating tuple unpacking techniques:")
    print()
    
    print("1. Basic Tuple Unpacking in Loops:")
    for class_name, class_info in school_data.items():
        print(f"\n   📚 {class_name} Class:")
        for name, grade in class_info["students"]:  # Tuple unpacking here
            print(f"      Student: {name}, Grade: {grade}")
    
    print()
    
    print("2. Unpacking with Enumeration:")
    student_number = 1
    for class_name, class_info in school_data.items():
        print(f"\n   📚 {class_name}:")
        for i, (name, grade) in enumerate(class_info["students"], 1):
            print(f"      {i}. {name}: {grade} points")
            student_number += 1
    
    print()
    
    print("3. Creating Separate Lists Using Unpacking:")
    all_names = []
    all_grades = []
    
    for class_name, class_info in school_data.items():
        for name, grade in class_info["students"]:
            all_names.append(name)
            all_grades.append(grade)
    
    print(f"   All student names: {all_names}")
    print(f"   All grades: {all_grades}")
    print()
    
    print("4. Multiple Assignment with Unpacking:")
    for class_name, class_info in school_data.items():
        teacher = class_info["teacher"]
        students = class_info["students"]
        
        if students:  # Check if class has students
            first_name, first_grade = students[0]
            print(f"   {class_name}: First student is {first_name} with {first_grade} points")
            
            last_name, last_grade = students[-1]
            print(f"   {class_name}: Last student is {last_name} with {last_grade} points")
    
    print()
    
    print("5. Advanced Unpacking Examples:")
    
    all_class_students = []
    for class_name, class_info in school_data.items():
        for student_data in class_info["students"]:
            name, grade = student_data  # Unpacking tuple
            all_class_students.append((name, grade, class_name))
    
    if len(all_class_students) >= 3:
        first_student = all_class_students[0]
        last_student = all_class_students[-1]
        first_name, first_grade, first_class = first_student
        last_name, last_grade, last_class = last_student
        
        print(f"   First enrolled: {first_name} ({first_grade} in {first_class})")
        print(f"   Last enrolled: {last_name} ({last_grade} in {last_class})")
    
    print()
    
    print("6. Dictionary Unpacking (Bonus):")
    for class_name, class_info in school_data.items():
        teacher, students = class_info["teacher"], class_info["students"]
        print(f"   Class: {class_name}")
        print(f"   Teacher: {teacher}")
        print(f"   Student count: {len(students)}")
        
        grade_sum = 0
        for name, grade in students:
            grade_sum += grade
        
        average = grade_sum / len(students) if students else 0
        print(f"   Average: {average:.1f}")
        print()

def advanced_school_analytics(school_data):
    """Perform advanced analytics on school data"""
    print("=== Advanced School Analytics ===")
    print()
    
    all_students_data = []
    for class_name, class_info in school_data.items():
        teacher = class_info["teacher"]
        for name, grade in class_info["students"]:
            all_students_data.append({
                'name': name,
                'grade': grade,
                'class': class_name,
                'teacher': teacher
            })
    
    print("1. Grade Distribution Analysis:")
    grade_ranges = {
        'A (90-100)': [s for s in all_students_data if s['grade'] >= 90],
        'B (80-89)': [s for s in all_students_data if 80 <= s['grade'] < 90],
        'C (70-79)': [s for s in all_students_data if 70 <= s['grade'] < 80],
        'D (60-69)': [s for s in all_students_data if 60 <= s['grade'] < 70],
        'F (Below 60)': [s for s in all_students_data if s['grade'] < 60]
    }
    
    for grade_range, students in grade_ranges.items():
        count = len(students)
        percentage = (count / len(all_students_data)) * 100 if all_students_data else 0
        print(f"   {grade_range}: {count} students ({percentage:.1f}%)")
        if students:
            names = [s['name'] for s in students]
            print(f"      Students: {', '.join(names)}")
    
    print()
    
    print("2. Teacher Performance Comparison:")
    teacher_stats = {}
    
    for class_name, class_info in school_data.items():
        teacher = class_info["teacher"]
        grades = [grade for _, grade in class_info["students"]]
        
        teacher_stats[teacher] = {
            'class': class_name,
            'student_count': len(grades),
            'average_grade': sum(grades) / len(grades) if grades else 0,
            'highest_grade': max(grades) if grades else 0,
            'lowest_grade': min(grades) if grades else 0
        }
    
    for teacher, stats in teacher_stats.items():
        print(f"   👨‍🏫 {teacher} ({stats['class']}):")
        print(f"      Students: {stats['student_count']}")
        print(f"      Class Average: {stats['average_grade']:.1f}")
        print(f"      Highest Grade: {stats['highest_grade']}")
        print(f"      Lowest Grade: {stats['lowest_grade']}")
        print()
    
    print("3. Overall School Statistics:")
    all_grades = [s['grade'] for s in all_students_data]
    
    if all_grades:
        school_average = sum(all_grades) / len(all_grades)
        highest_grade = max(all_grades)
        lowest_grade = min(all_grades)
        
        print(f"   🏫 School Average: {school_average:.1f}")
        print(f"   📈 Highest Grade: {highest_grade}")
        print(f"   📉 Lowest Grade: {lowest_grade}")
        print(f"   📊 Grade Range: {highest_grade - lowest_grade} points")
        print(f"   👥 Total Students: {len(all_students_data)}")
        print(f"   📚 Total Classes: {len(school_data)}")
    
    print()

def student_lookup_system(school_data):
    """Demonstrate student lookup and search functionality"""
    print("=== Student Lookup System ===")
    print()
    
    student_directory = {}
    for class_name, class_info in school_data.items():
        teacher = class_info["teacher"]
        for name, grade in class_info["students"]:
            student_directory[name] = {
                'grade': grade,
                'class': class_name,
                'teacher': teacher
            }
    
    print("Student Directory:")
    print(f"{'Name':<10} {'Grade':<7} {'Class':<10} {'Teacher'}")
    print("-" * 45)
    
    for name, info in sorted(student_directory.items()):
        print(f"{name:<10} {info['grade']:<7} {info['class']:<10} {info['teacher']}")
    
    print()
    
    print("Search Examples:")
    search_names = ["Alice", "Eve", "Unknown"]
    
    for search_name in search_names:
        if search_name in student_directory:
            info = student_directory[search_name]
            print(f"   ✅ {search_name}: {info['grade']} points in {info['class']} with {info['teacher']}")
        else:
            print(f"   ❌ {search_name}: Student not found")
    
    print()

def main():
    print("🏫 SCHOOL MANAGEMENT SYSTEM 🏫")
    print("=" * 60)
    print()
    
    print("Initial School Data Structure:")
    for class_name, class_info in school.items():
        print(f"📚 {class_name}:")
        print(f"   Teacher: {class_info['teacher']}")
        print(f"   Students: {class_info['students']}")
    print()
    
    display_school_overview(school)
    
    print("Executing Required Tasks:")
    print()
    
    print_teacher_names(school)
    
    class_averages = calculate_class_averages(school)
    
    top_student = find_top_student(school)
    
    demonstrate_unpacking(school)
    
    advanced_school_analytics(school)
    student_lookup_system(school)
    
    print("=== Summary & Key Concepts ===")
    print()
    print("✅ Completed Tasks:")
    print("   1. ✅ Printed all teacher names")
    print("   2. ✅ Calculated class average grades")
    print("   3. ✅ Found top student across all classes")
    print("   4. ✅ Demonstrated tuple unpacking techniques")
    print()
    print("🔧 Technical Concepts Demonstrated:")
    print("   • Nested dictionary navigation")
    print("   • Tuple unpacking in various contexts")
    print("   • Data aggregation and analysis")
    print("   • List comprehensions with nested data")
    print("   • Dictionary creation from nested structures")
    print("   • Statistical calculations")
    print()
    print("📊 Data Structure Benefits:")
    print("   • Hierarchical organization (school → class → students)")
    print("   • Fast lookups by class name")
    print("   • Flexible data modeling")
    print("   • Easy to extend with new classes/attributes")
    print("   • Natural representation of real-world relationships")
    print()

if __name__ == "__main__":
    main()

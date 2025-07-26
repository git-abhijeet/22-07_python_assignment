students = ["Alice", "Bob", "Carol", "David", "Eve"]
scores = [85, 92, 78, 88, 95]

def create_numbered_student_list(student_list):
    """Create a numbered list of students starting from 1"""
    print("=== Task 1: Numbered List of Students ===")
    print("Students with numbers (starting from 1):")
    
    for index, student in enumerate(student_list, start=1):
        print(f"{index}. {student}")
    print()

def pair_students_with_scores(student_list, score_list):
    """Pair students with their scores using enumerate()"""
    print("=== Task 2: Pair Students with Scores ===")
    print("Student-Score pairs:")
    
    print("Method 1 - Using enumerate with zip:")
    for index, (student, score) in enumerate(zip(student_list, score_list)):
        print(f"  {index}. {student}: {score}")
    print()
    
    print("Method 2 - Using enumerate on students:")
    for index, student in enumerate(student_list):
        print(f"  {index}. {student}: {score_list[index]}")
    print()

def find_high_scorer_positions(score_list, threshold=90):
    """Find positions of students who scored above the threshold"""
    print(f"=== Task 3: Find Positions of High Scorers (>{threshold}) ===")
    
    high_scorer_positions = []
    high_scorer_details = []
    
    for index, score in enumerate(score_list):
        if score > threshold:
            high_scorer_positions.append(index)
            high_scorer_details.append((index, students[index], score))
    
    print(f"Positions of students with scores > {threshold}:")
    print(f"Positions (indices): {high_scorer_positions}")
    print()
    
    print("Detailed information:")
    for index, student, score in high_scorer_details:
        print(f"  Position {index}: {student} scored {score}")
    print()
    
    return high_scorer_positions

def map_positions_to_names(student_list):
    """Create a dictionary mapping positions to student names"""
    print("=== Task 4: Map Positions to Student Names ===")
    
    position_to_name = {}
    for position, name in enumerate(student_list):
        position_to_name[position] = name
    
    print("Position-to-Name dictionary (positions start from 0):")
    for position, name in position_to_name.items():
        print(f"  Position {position}: {name}")
    print()
    
    position_to_name_alt = {position: name for position, name in enumerate(student_list)}
    print("Same result using dictionary comprehension:")
    print(f"  {position_to_name_alt}")
    print()
    
    return position_to_name

def demonstrate_enumerate_variations():
    """Demonstrate different ways to use enumerate()"""
    print("=== Enumerate Variations and Advanced Usage ===")
    
    print("1. Different start values:")
    print("   Starting from 0 (default):")
    for i, student in enumerate(students):
        print(f"     {i}: {student}")
    
    print("   Starting from 1:")
    for i, student in enumerate(students, 1):
        print(f"     {i}: {student}")
    
    print("   Starting from 100:")
    for i, student in enumerate(students, 100):
        print(f"     {i}: {student}")
    print()
    
    print("2. Enumerate with filtering (scores >= 85):")
    for i, (student, score) in enumerate(zip(students, scores)):
        if score >= 85:
            print(f"   {i}: {student} - {score}")
    print()
    
    print("3. Enumerate in list comprehensions:")
    indexed_students = [(i, student) for i, student in enumerate(students)]
    print(f"   Indexed students: {indexed_students}")
    
    high_positions = [i for i, score in enumerate(scores) if score > 90]
    print(f"   High scorer positions: {high_positions}")
    print()
    
    print("4. Enumerate with reversed data:")
    for i, student in enumerate(reversed(students)):
        print(f"   {i}: {student}")
    print()

def create_comprehensive_report():
    """Create a comprehensive student report using enumerate"""
    print("=== Comprehensive Student Report ===")
    
    average_score = sum(scores) / len(scores)
    max_score = max(scores)
    min_score = min(scores)
    
    print(f"Class Statistics:")
    print(f"  Total Students: {len(students)}")
    print(f"  Average Score: {average_score:.1f}")
    print(f"  Highest Score: {max_score}")
    print(f"  Lowest Score: {min_score}")
    print()
    
    print("Individual Student Reports:")
    print(f"{'Rank':<6} {'Position':<10} {'Name':<10} {'Score':<7} {'Performance'}")
    print("-" * 55)
    
    student_score_pairs = [(i, student, score) for i, (student, score) in enumerate(zip(students, scores))]
    sorted_pairs = sorted(student_score_pairs, key=lambda x: x[2], reverse=True)
    
    for rank, (original_pos, student, score) in enumerate(sorted_pairs, 1):
        if score >= 90:
            performance = "Excellent"
        elif score >= 80:
            performance = "Good"
        elif score >= 70:
            performance = "Average"
        else:
            performance = "Needs Improvement"
        
        print(f"{rank:<6} {original_pos:<10} {student:<10} {score:<7} {performance}")
    print()

def demonstrate_practical_applications():
    """Show practical applications of enumerate in data processing"""
    print("=== Practical Applications of enumerate() ===")
    
    print("1. Processing CSV-like data:")
    csv_data = [
        "Name,Score,Grade",
        "Alice,85,B",
        "Bob,92,A",
        "Carol,78,C"
    ]
    
    for line_num, line in enumerate(csv_data):
        if line_num == 0:
            print(f"   Header (line {line_num}): {line}")
        else:
            print(f"   Data row {line_num}: {line}")
    print()
    
    print("2. Error tracking with line numbers:")
    data_to_validate = ["85", "92", "invalid", "88", "95"]
    errors = []
    
    for line_num, value in enumerate(data_to_validate, 1):
        try:
            int(value)
            print(f"   Line {line_num}: '{value}' - Valid")
        except ValueError:
            error_msg = f"Line {line_num}: '{value}' - Invalid number"
            errors.append(error_msg)
            print(f"   {error_msg}")
    
    if errors:
        print(f"   Found {len(errors)} error(s)")
    print()
    
    print("3. Creating lookup tables:")
    grade_lookup = {pos: f"Grade_{chr(65 + pos)}" for pos, _ in enumerate(students)}
    print(f"   Grade lookup: {grade_lookup}")
    
    print("4. Batch processing simulation:")
    data_to_process = students.copy()
    processed_items = []
    
    for i, item in enumerate(data_to_process):
        processed_item = f"Processed_{item}"
        processed_items.append(processed_item)
        progress = ((i + 1) / len(data_to_process)) * 100
        print(f"   Processing item {i + 1}/{len(data_to_process)}: {item} -> {processed_item} ({progress:.1f}% complete)")
    print()

def main():
    print("📊 DATA PROCESSING WITH ENUMERATE() 📊")
    print("=" * 60)
    print()
    
    print("Initial Data:")
    print(f"Students: {students}")
    print(f"Scores:   {scores}")
    print()
    
    create_numbered_student_list(students)
    
    pair_students_with_scores(students, scores)
    
    high_scorer_positions = find_high_scorer_positions(scores, threshold=90)
    
    position_map = map_positions_to_names(students)
    
    demonstrate_enumerate_variations()
    create_comprehensive_report()
    demonstrate_practical_applications()
    
    print("=== Interactive Exploration ===")
    print("Try these examples in your Python console:")
    print("1. list(enumerate(students))")
    print("2. list(enumerate(students, start=1))")
    print("3. dict(enumerate(students))")
    print("4. [i for i, score in enumerate(scores) if score > 85]")
    print("5. [(i, name, score) for i, (name, score) in enumerate(zip(students, scores))]")
    print()

if __name__ == "__main__":
    main()

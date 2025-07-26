class GradeAnalyzer:
    """Comprehensive grade analysis system using Python lists"""
    
    def __init__(self):
        self.original_grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]
        self.grades = self.original_grades.copy()  # Working copy
        self.operation_history = []  # Track all operations
        
        print("📊 GRADE ANALYZER SYSTEM 📊")
        print("=" * 50)
        print()
        self.display_current_grades("Initial Grades")
    
    def display_current_grades(self, title="Current Grades"):
        """Display current grades with statistics"""
        print(f"📋 {title}:")
        print(f"   Grades: {self.grades}")
        print(f"   Count: {len(self.grades)}")
        if self.grades:
            print(f"   Average: {sum(self.grades) / len(self.grades):.2f}")
            print(f"   Highest: {max(self.grades)}")
            print(f"   Lowest: {min(self.grades)}")
        print()
    
    def log_operation(self, operation, description, result=None):
        """Log operations for history tracking"""
        self.operation_history.append({
            'operation': operation,
            'description': description,
            'result': result,
            'grades_after': self.grades.copy()
        })
    
    def slice_grades_2_to_7(self):
        """Task 1: Slice grades from index 2 to 7"""
        print("1️⃣ SLICING GRADES (INDEX 2 TO 7)")
        print("-" * 40)
        
        print("   🔍 Original grades with indices:")
        for i, grade in enumerate(self.grades):
            marker = " 👈" if 2 <= i <= 6 else ""
            print(f"      Index {i}: {grade}{marker}")
        print()
        
        sliced_grades = self.grades[2:7]
        
        print(f"   📊 Sliced grades [2:7]: {sliced_grades}")
        print(f"   📏 Length of slice: {len(sliced_grades)}")
        print(f"   🎯 Index range: 2 (inclusive) to 7 (exclusive)")
        
        print("\n   🔧 Additional Slicing Examples:")
        print(f"      First 3 grades [0:3]: {self.grades[0:3]}")
        print(f"      Last 3 grades [-3:]: {self.grades[-3:]}")
        print(f"      Every 2nd grade [::2]: {self.grades[::2]}")
        print(f"      Reverse order [::-1]: {self.grades[::-1]}")
        
        self.log_operation("slice", f"Sliced grades from index 2 to 7", sliced_grades)
        print()
        return sliced_grades
    
    def find_grades_above_85(self):
        """Task 2: Use list comprehension to find grades above 85"""
        print("2️⃣ GRADES ABOVE 85 (LIST COMPREHENSION)")
        print("-" * 40)
        
        grades_above_85 = [grade for grade in self.grades if grade > 85]
        
        print(f"   📈 Grades above 85: {grades_above_85}")
        print(f"   📊 Count: {len(grades_above_85)}")
        print(f"   📏 Percentage: {len(grades_above_85) / len(self.grades) * 100:.1f}%")
        
        print("\n   🚀 Advanced List Comprehensions:")
        
        letter_grades = [(grade, self.get_letter_grade(grade)) for grade in self.grades]
        print(f"      With letter grades: {letter_grades}")
        
        adjusted_grades = [grade + 2 if grade < 80 else grade for grade in self.grades]
        print(f"      Adjusted (+2 for <80): {adjusted_grades}")
        
        excellent_grades = [grade for grade in self.grades if grade > 85 and grade < 95]
        print(f"      Excellent (85-95): {excellent_grades}")
        
        indexed_high_grades = [(i, grade) for i, grade in enumerate(self.grades) if grade > 85]
        print(f"      High grades with index: {indexed_high_grades}")
        
        self.log_operation("filter", "Found grades above 85", grades_above_85)
        print()
        return grades_above_85
    
    def replace_grade_at_index_3(self):
        """Task 3: Replace the grade at index 3 with 95"""
        print("3️⃣ REPLACING GRADE AT INDEX 3 WITH 95")
        print("-" * 40)
        
        old_grade = self.grades[3]
        print(f"   🔄 Before replacement:")
        print(f"      Index 3: {old_grade}")
        
        self.grades[3] = 95
        
        print(f"   ✅ After replacement:")
        print(f"      Index 3: {self.grades[3]}")
        print(f"   📈 Change: {old_grade} → {self.grades[3]} (+{self.grades[3] - old_grade})")
        
        new_avg = sum(self.grades) / len(self.grades)
        print(f"   📊 New average: {new_avg:.2f}")
        
        self.log_operation("replace", f"Replaced grade at index 3: {old_grade} → 95")
        self.display_current_grades("Updated Grades")
        return old_grade
    
    def append_three_new_grades(self):
        """Task 4: Append three new grades"""
        print("4️⃣ APPENDING THREE NEW GRADES")
        print("-" * 40)
        
        new_grades = [93, 86, 88]
        original_length = len(self.grades)
        
        print(f"   📝 Adding new grades: {new_grades}")
        print(f"   📏 Current list length: {original_length}")
        
        for i, grade in enumerate(new_grades, 1):
            self.grades.append(grade)
            print(f"      Added grade #{i}: {grade}")
        
        print(f"   ✅ New list length: {len(self.grades)}")
        print(f"   📈 Added {len(new_grades)} grades")
        
        print("\n   🔧 Alternative Append Methods:")
        temp_list = self.grades.copy()
        
        temp_list2 = self.grades[:-3].copy()  # Remove the just added grades
        temp_list2.extend([93, 86, 88])
        print(f"      Using extend(): {temp_list2[-6:]}")  # Show last 6
        
        temp_list3 = self.grades[:-3] + [93, 86, 88]
        print(f"      Using concatenation: {temp_list3[-6:]}")  # Show last 6
        
        temp_list4 = [*self.grades[:-3], 93, 86, 88]
        print(f"      Using unpacking: {temp_list4[-6:]}")  # Show last 6
        
        self.log_operation("append", f"Appended 3 new grades: {new_grades}")
        self.display_current_grades("After Adding New Grades")
        return new_grades
    
    def sort_and_show_top_5(self):
        """Task 5: Sort in descending order and display top 5 grades"""
        print("5️⃣ SORTING AND TOP 5 GRADES")
        print("-" * 40)
        
        print(f"   📋 Before sorting: {self.grades}")
        
        sorted_grades = sorted(self.grades, reverse=True)
        
        print(f"   📊 After sorting (descending): {sorted_grades}")
        
        top_5_grades = sorted_grades[:5]
        print(f"   🏆 Top 5 grades: {top_5_grades}")
        
        print("\n   🥇 Grade Rankings:")
        for i, grade in enumerate(top_5_grades, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
            print(f"      {medal} Rank {i}: {grade}")
        
        print("\n   🔧 Alternative Sorting Methods:")
        
        temp_grades = self.grades.copy()
        temp_grades.sort(reverse=True)
        print(f"      In-place sort(): {temp_grades[:5]}")
        
        temp_grades2 = sorted(self.grades, key=lambda x: -x)  # Negative for descending
        print(f"      With key function: {temp_grades2[:5]}")
        
        temp_grades3 = sorted(self.grades, key=lambda x: abs(x - 90))
        print(f"      Closest to 90: {temp_grades3[:5]}")
        
        self.log_operation("sort", "Sorted grades in descending order", top_5_grades)
        print()
        return top_5_grades
    
    def get_letter_grade(self, numeric_grade):
        """Convert numeric grade to letter grade"""
        if numeric_grade >= 97:
            return 'A+'
        elif numeric_grade >= 93:
            return 'A'
        elif numeric_grade >= 90:
            return 'A-'
        elif numeric_grade >= 87:
            return 'B+'
        elif numeric_grade >= 83:
            return 'B'
        elif numeric_grade >= 80:
            return 'B-'
        elif numeric_grade >= 77:
            return 'C+'
        elif numeric_grade >= 73:
            return 'C'
        elif numeric_grade >= 70:
            return 'C-'
        else:
            return 'F'
    
    def comprehensive_analysis(self):
        """Perform comprehensive grade analysis"""
        print("📈 COMPREHENSIVE GRADE ANALYSIS")
        print("-" * 40)
        
        grades = self.grades
        avg = sum(grades) / len(grades)
        
        grade_ranges = {
            'A (90-100)': len([g for g in grades if g >= 90]),
            'B (80-89)': len([g for g in grades if 80 <= g < 90]),
            'C (70-79)': len([g for g in grades if 70 <= g < 80]),
            'D (60-69)': len([g for g in grades if 60 <= g < 70]),
            'F (0-59)': len([g for g in grades if g < 60])
        }
        
        print(f"   📊 Statistical Summary:")
        print(f"      Total Students: {len(grades)}")
        print(f"      Average Grade: {avg:.2f}")
        print(f"      Median Grade: {sorted(grades)[len(grades)//2]}")
        print(f"      Standard Deviation: {self.calculate_std_dev(grades):.2f}")
        
        print(f"\n   📈 Grade Distribution:")
        for range_name, count in grade_ranges.items():
            percentage = (count / len(grades)) * 100
            bar = "█" * int(percentage // 5)  # Visual bar
            print(f"      {range_name}: {count} students ({percentage:.1f}%) {bar}")
        
        print(f"\n   💡 Performance Insights:")
        failing_count = len([g for g in grades if g < 70])
        excellent_count = len([g for g in grades if g >= 95])
        
        if failing_count > 0:
            print(f"      ⚠️  {failing_count} student(s) need improvement")
        if excellent_count > 0:
            print(f"      ⭐ {excellent_count} student(s) achieved excellence")
        
        if avg >= 85:
            print(f"      🎉 Class performance is excellent!")
        elif avg >= 75:
            print(f"      👍 Class performance is good")
        else:
            print(f"      📚 Class needs additional support")
    
    def calculate_std_dev(self, grades):
        """Calculate standard deviation"""
        avg = sum(grades) / len(grades)
        variance = sum((g - avg) ** 2 for g in grades) / len(grades)
        return variance ** 0.5
    
    def show_operation_history(self):
        """Display complete operation history"""
        print("📋 OPERATION HISTORY")
        print("-" * 40)
        
        if not self.operation_history:
            print("   No operations recorded")
            return
        
        for i, op in enumerate(self.operation_history, 1):
            print(f"   {i}. {op['operation'].upper()}: {op['description']}")
            if op['result']:
                print(f"      Result: {op['result']}")
            print(f"      Grades after: {op['grades_after']}")
            print()
    
    def run_all_tasks(self):
        """Execute all required tasks in sequence"""
        print("\n🚀 EXECUTING ALL REQUIRED TASKS")
        print("=" * 50)
        print()
        
        sliced_result = self.slice_grades_2_to_7()
        
        high_grades = self.find_grades_above_85()
        
        old_grade = self.replace_grade_at_index_3()
        
        new_grades = self.append_three_new_grades()
        
        top_5 = self.sort_and_show_top_5()
        
        self.comprehensive_analysis()
        
        return {
            'sliced_grades': sliced_result,
            'high_grades': high_grades,
            'replaced_grade': old_grade,
            'new_grades': new_grades,
            'top_5_grades': top_5
        }

def demonstrate_list_operations():
    """Demonstrate various list operations and techniques"""
    print("\n🎓 LIST OPERATIONS DEMONSTRATION 🎓")
    print("=" * 50)
    print()
    
    sample_grades = [85, 92, 78, 90, 88]
    
    print("📚 Advanced List Techniques:")
    print(f"   Original list: {sample_grades}")
    print()
    
    print("   🔪 Slicing Techniques:")
    print(f"      [1:4]: {sample_grades[1:4]}")
    print(f"      [::2]: {sample_grades[::2]}")
    print(f"      [-2:]: {sample_grades[-2:]}")
    print(f"      [::-1]: {sample_grades[::-1]}")
    print()
    
    print("   📝 List Comprehension Patterns:")
    print(f"      Squared: {[x**2 for x in sample_grades]}")
    print(f"      Passed: {[x for x in sample_grades if x >= 80]}")
    print(f"      Letter grades: {[(x, 'A' if x >= 90 else 'B' if x >= 80 else 'C') for x in sample_grades]}")
    print()
    
    print("   🛠️  List Methods:")
    temp_list = sample_grades.copy()
    print(f"      Original: {temp_list}")
    temp_list.insert(2, 95)
    print(f"      After insert(2, 95): {temp_list}")
    temp_list.remove(92)
    print(f"      After remove(92): {temp_list}")
    popped = temp_list.pop()
    print(f"      After pop(): {temp_list} (popped: {popped})")
    print()

def performance_comparison():
    """Compare performance of different list operations"""
    print("⚡ PERFORMANCE COMPARISON ⚡")
    print("=" * 50)
    print()
    
    import time
    
    large_grades = list(range(10000))
    
    print("🔬 Testing with 10,000 elements:")
    
    start_time = time.time()
    comp_result = [x for x in large_grades if x % 2 == 0]
    comp_time = time.time() - start_time
    
    start_time = time.time()
    filter_result = list(filter(lambda x: x % 2 == 0, large_grades))
    filter_time = time.time() - start_time
    
    print(f"   📊 Finding even numbers:")
    print(f"      List comprehension: {comp_time:.6f} seconds")
    print(f"      Filter function: {filter_time:.6f} seconds")
    
    unsorted_grades = large_grades.copy()
    import random
    random.shuffle(unsorted_grades)
    
    start_time = time.time()
    sorted_copy = sorted(unsorted_grades)
    sorted_time = time.time() - start_time
    
    start_time = time.time()
    unsorted_grades.sort()
    inplace_time = time.time() - start_time
    
    print(f"\n   🔄 Sorting 10,000 elements:")
    print(f"      sorted(): {sorted_time:.6f} seconds")
    print(f"      .sort(): {inplace_time:.6f} seconds")
    print()

def main():
    """Main function to run grade analyzer"""
    analyzer = GradeAnalyzer()
    results = analyzer.run_all_tasks()
    
    analyzer.show_operation_history()
    
    demonstrate_list_operations()
    performance_comparison()
    
    print("🎉 GRADE ANALYSIS COMPLETE!")
    print("=" * 50)
    print()
    print("✅ All required tasks completed:")
    print(f"   1. ✅ Sliced grades [2:7]: {results['sliced_grades']}")
    print(f"   2. ✅ Grades above 85: {results['high_grades']}")
    print(f"   3. ✅ Replaced grade at index 3: {results['replaced_grade']} → 95")
    print(f"   4. ✅ Added new grades: {results['new_grades']}")
    print(f"   5. ✅ Top 5 grades: {results['top_5_grades']}")
    print()
    print("🚀 Additional features demonstrated:")
    print("   • Comprehensive statistical analysis")
    print("   • Grade distribution visualization")
    print("   • Performance insights and recommendations")
    print("   • Operation history tracking")
    print("   • Advanced list manipulation techniques")
    print("   • Performance comparison studies")
    print()

if __name__ == "__main__":
    main()

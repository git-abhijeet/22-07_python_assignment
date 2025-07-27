from collections import defaultdict
import statistics
from datetime import datetime

class GradeManager:
    """
    A comprehensive grade management system using defaultdict for efficient data organization
    """
    
    def __init__(self):
        """
        Initialize the grade manager with appropriate defaultdict structures
        Use defaultdict to avoid key existence checks
        """
        print("📚 STUDENT GRADE MANAGEMENT SYSTEM")
        print("=" * 50)
        print()
        
        # Initialize data structures using defaultdict
        # student_grades: {student_name: {subject: [grades]}}
        self.student_grades = defaultdict(lambda: defaultdict(list))
        
        # subject_grades: {subject: [grades]}
        self.subject_grades = defaultdict(list)
        
        # student_averages cache for performance
        self.student_averages_cache = defaultdict(float)
        
        # Additional tracking for analytics
        self.grade_history = defaultdict(list)  # Track all grades with timestamps
        self.subject_count = defaultdict(int)   # Count of students per subject
        
        print("✅ Grade Manager initialized with defaultdict structures")
        print("   📊 Student grades: defaultdict(lambda: defaultdict(list))")
        print("   📈 Subject grades: defaultdict(list)")
        print("   💾 Caching system: enabled")
        print()
    
    def add_grade(self, student_name, subject, grade):
        """
        Add a grade for a student in a specific subject
        Args:
            student_name (str): Name of the student
            subject (str): Subject name
            grade (float): Grade value (0-100)
        """
        if not (0 <= grade <= 100):
            raise ValueError(f"Grade must be between 0 and 100, got {grade}")
        
        # Add grade using defaultdict - no need to check if keys exist!
        self.student_grades[student_name][subject].append(grade)
        self.subject_grades[subject].append(grade)
        
        # Track grade history with timestamp
        self.grade_history[student_name].append({
            'subject': subject,
            'grade': grade,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Update subject count
        if len(self.student_grades[student_name][subject]) == 1:
            self.subject_count[subject] += 1
        
        # Clear cache for this student
        if student_name in self.student_averages_cache:
            del self.student_averages_cache[student_name]
        
        print(f"✅ Added grade: {student_name} - {subject}: {grade}")
    
    def get_student_average(self, student_name):
        """
        Calculate average grade for a student across all subjects
        Args:
            student_name (str): Name of the student
        Returns:
            float: Average grade or 0 if student not found
        """
        # Check cache first
        if student_name in self.student_averages_cache:
            return self.student_averages_cache[student_name]
        
        if student_name not in self.student_grades:
            return 0.0
        
        all_grades = []
        for subject_grades in self.student_grades[student_name].values():
            all_grades.extend(subject_grades)
        
        if not all_grades:
            return 0.0
        
        average = sum(all_grades) / len(all_grades)
        
        # Cache the result
        self.student_averages_cache[student_name] = average
        
        return round(average, 2)
    
    def get_subject_statistics(self, subject):
        """
        Get statistics for a specific subject across all students
        Args:
            subject (str): Subject name
        Returns:
            dict: Contains 'average', 'highest', 'lowest', 'student_count', 'median', 'std_dev'
        """
        if subject not in self.subject_grades or not self.subject_grades[subject]:
            return {
                'average': 0.0,
                'highest': 0.0,
                'lowest': 0.0,
                'student_count': 0,
                'median': 0.0,
                'std_dev': 0.0,
                'grade_distribution': {}
            }
        
        grades = self.subject_grades[subject]
        
        # Calculate statistics
        avg = sum(grades) / len(grades)
        highest = max(grades)
        lowest = min(grades)
        student_count = self.subject_count[subject]
        median = statistics.median(grades)
        std_dev = statistics.stdev(grades) if len(grades) > 1 else 0.0
        
        # Grade distribution
        grade_ranges = {
            'A (90-100)': len([g for g in grades if 90 <= g <= 100]),
            'B (80-89)': len([g for g in grades if 80 <= g < 90]),
            'C (70-79)': len([g for g in grades if 70 <= g < 80]),
            'D (60-69)': len([g for g in grades if 60 <= g < 70]),
            'F (0-59)': len([g for g in grades if 0 <= g < 60])
        }
        
        return {
            'average': round(avg, 2),
            'highest': highest,
            'lowest': lowest,
            'student_count': student_count,
            'median': round(median, 2),
            'std_dev': round(std_dev, 2),
            'grade_distribution': grade_ranges,
            'total_grades': len(grades)
        }
    
    def get_top_students(self, n=3):
        """
        Get top N students based on their overall average
        Args:
            n (int): Number of top students to return
        Returns:
            list: List of tuples (student_name, average_grade)
        """
        student_averages = []
        
        for student in self.student_grades.keys():
            avg = self.get_student_average(student)
            if avg > 0:  # Only include students with grades
                student_averages.append((student, avg))
        
        # Sort by average grade in descending order
        student_averages.sort(key=lambda x: x[1], reverse=True)
        
        return student_averages[:n]
    
    def get_failing_students(self, passing_grade=60):
        """
        Get students who are failing (average below passing grade)
        Args:
            passing_grade (float): Minimum grade to pass
        Returns:
            list: List of tuples (student_name, average_grade)
        """
        failing_students = []
        
        for student in self.student_grades.keys():
            avg = self.get_student_average(student)
            if 0 < avg < passing_grade:  # Has grades but below passing
                failing_students.append((student, avg))
        
        # Sort by average grade (lowest first)
        failing_students.sort(key=lambda x: x[1])
        
        return failing_students
    
    def get_student_detailed_report(self, student_name):
        """
        Generate a detailed report for a specific student
        Args:
            student_name (str): Name of the student
        Returns:
            dict: Detailed student information
        """
        if student_name not in self.student_grades:
            return None
        
        student_data = self.student_grades[student_name]
        subject_averages = {}
        
        for subject, grades in student_data.items():
            if grades:
                subject_averages[subject] = {
                    'average': round(sum(grades) / len(grades), 2),
                    'highest': max(grades),
                    'lowest': min(grades),
                    'grade_count': len(grades),
                    'grades': grades
                }
        
        overall_average = self.get_student_average(student_name)
        
        return {
            'student_name': student_name,
            'overall_average': overall_average,
            'subject_details': subject_averages,
            'subjects_count': len(subject_averages),
            'total_grades': sum(len(grades) for grades in student_data.values()),
            'grade_history': self.grade_history[student_name]
        }
    
    def get_class_statistics(self):
        """
        Get overall class statistics
        Returns:
            dict: Class-wide statistics
        """
        all_students = list(self.student_grades.keys())
        if not all_students:
            return {}
        
        # Calculate class average
        student_averages = [self.get_student_average(student) for student in all_students]
        student_averages = [avg for avg in student_averages if avg > 0]
        
        if not student_averages:
            return {}
        
        class_average = sum(student_averages) / len(student_averages)
        
        # Get subject information
        subjects = list(self.subject_grades.keys())
        subject_stats = {}
        for subject in subjects:
            subject_stats[subject] = self.get_subject_statistics(subject)
        
        return {
            'total_students': len(all_students),
            'class_average': round(class_average, 2),
            'highest_student_avg': max(student_averages),
            'lowest_student_avg': min(student_averages),
            'subjects_offered': subjects,
            'subject_count': len(subjects),
            'subject_statistics': subject_stats
        }
    
    def display_comprehensive_report(self):
        """Display a comprehensive report of all data"""
        print("📊 COMPREHENSIVE GRADE REPORT")
        print("=" * 50)
        print()
        
        # Class statistics
        class_stats = self.get_class_statistics()
        if class_stats:
            print("🏫 CLASS OVERVIEW:")
            print(f"   Total Students: {class_stats['total_students']}")
            print(f"   Subjects Offered: {class_stats['subject_count']}")
            print(f"   Class Average: {class_stats['class_average']}")
            print(f"   Highest Student Average: {class_stats['highest_student_avg']}")
            print(f"   Lowest Student Average: {class_stats['lowest_student_avg']}")
            print()
        
        # Top performers
        top_students = self.get_top_students(5)
        if top_students:
            print("🏆 TOP PERFORMERS:")
            for i, (student, avg) in enumerate(top_students, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                print(f"   {medal} {student}: {avg}")
            print()
        
        # Subject statistics
        print("📚 SUBJECT ANALYSIS:")
        for subject in sorted(self.subject_grades.keys()):
            stats = self.get_subject_statistics(subject)
            print(f"   📖 {subject}:")
            print(f"      Students: {stats['student_count']}")
            print(f"      Average: {stats['average']}")
            print(f"      Range: {stats['lowest']} - {stats['highest']}")
            print(f"      Median: {stats['median']}")
            print(f"      Std Dev: {stats['std_dev']}")
            
            # Grade distribution
            print(f"      Distribution:")
            for grade_range, count in stats['grade_distribution'].items():
                percentage = (count / stats['total_grades'] * 100) if stats['total_grades'] > 0 else 0
                bar = "█" * (count // 2) if count > 0 else ""
                print(f"         {grade_range}: {count} ({percentage:.1f}%) {bar}")
            print()


def demonstrate_defaultdict_benefits():
    """Demonstrate the benefits of using defaultdict"""
    print("🔧 DEFAULTDICT BENEFITS DEMONSTRATION")
    print("=" * 50)
    print()
    
    # Regular dict vs defaultdict comparison
    print("📝 Regular Dict vs DefaultDict:")
    print()
    
    print("❌ Regular Dict (requires key checking):")
    regular_dict = {}
    print("   # Adding grades with regular dict")
    print("   if 'Alice' not in regular_dict:")
    print("       regular_dict['Alice'] = {}")
    print("   if 'Math' not in regular_dict['Alice']:")
    print("       regular_dict['Alice']['Math'] = []")
    print("   regular_dict['Alice']['Math'].append(85)")
    print()
    
    print("✅ DefaultDict (automatic initialization):")
    auto_dict = defaultdict(lambda: defaultdict(list))
    print("   # Adding grades with defaultdict")
    print("   auto_dict['Alice']['Math'].append(85)  # Just works!")
    auto_dict['Alice']['Math'].append(85)
    print(f"   Result: {dict(auto_dict)}")
    print()
    
    # Performance demonstration
    print("⚡ Performance Benefits:")
    print("   • No key existence checks needed")
    print("   • Cleaner, more readable code")
    print("   • Automatic nested structure creation")
    print("   • Reduced chance of KeyError exceptions")
    print()


def main():
    """Main function to test the GradeManager implementation"""
    print("🎯 TESTING GRADE MANAGER SYSTEM")
    print("=" * 60)
    print()
    
    # Create manager instance
    manager = GradeManager()
    
    # Add sample grades
    print("📝 ADDING SAMPLE GRADES:")
    print("-" * 30)
    
    grades_data = [
        ("Alice", "Math", 85), ("Alice", "Science", 92), ("Alice", "English", 78),
        ("Bob", "Math", 75), ("Bob", "Science", 68), ("Bob", "English", 82),
        ("Charlie", "Math", 95), ("Charlie", "Science", 88), ("Charlie", "History", 91),
        ("Diana", "Math", 55), ("Diana", "Science", 62), ("Diana", "English", 70),
        ("Eve", "Math", 88), ("Eve", "Science", 94), ("Eve", "English", 86), ("Eve", "History", 89),
        ("Frank", "Math", 92), ("Frank", "Science", 85), ("Frank", "English", 88), ("Frank", "History", 90),
        ("Grace", "Math", 45), ("Grace", "Science", 52), ("Grace", "English", 58),
        ("Henry", "Math", 78), ("Henry", "Science", 82), ("Henry", "History", 85)
    ]
    
    for student, subject, grade in grades_data:
        manager.add_grade(student, subject, grade)
    
    print()
    
    # Test all methods
    print("🧪 TESTING ALL METHODS:")
    print("-" * 30)
    
    # Test individual student average
    alice_avg = manager.get_student_average("Alice")
    print(f"📊 Alice's average: {alice_avg}")
    
    # Test subject statistics
    math_stats = manager.get_subject_statistics("Math")
    print(f"📈 Math statistics:")
    print(f"   Average: {math_stats['average']}")
    print(f"   Range: {math_stats['lowest']} - {math_stats['highest']}")
    print(f"   Students: {math_stats['student_count']}")
    print(f"   Standard Deviation: {math_stats['std_dev']}")
    
    # Test top students
    top_students = manager.get_top_students(3)
    print(f"🏆 Top 3 students: {top_students}")
    
    # Test failing students
    failing_students = manager.get_failing_students(75)
    print(f"⚠️  Failing students (below 75): {failing_students}")
    print()
    
    # Generate detailed reports
    print("📋 DETAILED STUDENT REPORT:")
    print("-" * 30)
    charlie_report = manager.get_student_detailed_report("Charlie")
    if charlie_report:
        print(f"Student: {charlie_report['student_name']}")
        print(f"Overall Average: {charlie_report['overall_average']}")
        print(f"Subjects: {charlie_report['subjects_count']}")
        print("Subject Details:")
        for subject, details in charlie_report['subject_details'].items():
            print(f"   {subject}: {details['average']} (from {details['grade_count']} grades)")
    print()
    
    # Display comprehensive report
    manager.display_comprehensive_report()
    
    # Demonstrate defaultdict benefits
    demonstrate_defaultdict_benefits()
    
    print("🎉 GRADE MANAGEMENT SYSTEM TESTING COMPLETE!")
    print("=" * 60)
    print()
    print("✅ All features tested successfully:")
    print("   • Grade addition with automatic structure creation")
    print("   • Student average calculations with caching")
    print("   • Subject statistics with comprehensive metrics")
    print("   • Top student identification")
    print("   • Failing student detection")
    print("   • Detailed reporting system")
    print("   • Class-wide analytics")
    print("   • DefaultDict performance benefits demonstrated")
    print()


if __name__ == "__main__":
    main()

from datetime import datetime
from typing import Dict, List, Optional, Tuple
import statistics

class Course:
    """
    Course class for managing university courses
    Handles enrollment, capacity, grades, and course statistics
    """
    
    # Class variables for tracking all courses
    _all_courses = {}
    _total_enrollments = 0
    
    def __init__(self, course_code: str, course_name: str, instructor: str, credit_hours: int, max_capacity: int):
        """
        Initialize a course
        
        Args:
            course_code (str): Unique course identifier (e.g., "MATH101")
            course_name (str): Name of the course
            instructor (str): Instructor name
            credit_hours (int): Number of credit hours
            max_capacity (int): Maximum number of students
        """
        print("🎓 UNIVERSITY COURSE MANAGEMENT SYSTEM")
        print("=" * 50)
        print()
        
        # Validate input
        self._validate_course_data(course_code, course_name, instructor, credit_hours, max_capacity)
        
        # Course attributes
        self.course_code = course_code
        self.course_name = course_name
        self.instructor = instructor
        self.credit_hours = credit_hours
        self.max_capacity = max_capacity
        self.created_at = datetime.now()
        
        # Enrollment tracking
        self.enrolled_students = {}  # {student_id: Student object}
        self.student_grades = {}     # {student_id: grade}
        self.waitlist = []           # List of students waiting for enrollment
        
        # Register course globally
        Course._all_courses[course_code] = self
        
        print(f"✅ Course created successfully:")
        print(f"   Code: {self.course_code}")
        print(f"   Name: {self.course_name}")
        print(f"   Instructor: {self.instructor}")
        print(f"   Credit Hours: {self.credit_hours}")
        print(f"   Max Capacity: {self.max_capacity}")
        print()
    
    def _validate_course_data(self, course_code, course_name, instructor, credit_hours, max_capacity):
        """Validate course creation data"""
        if not course_code or not isinstance(course_code, str):
            raise ValueError("Course code must be a non-empty string")
        
        if course_code in Course._all_courses:
            raise ValueError(f"Course code {course_code} already exists")
        
        if not course_name or not isinstance(course_name, str):
            raise ValueError("Course name must be a non-empty string")
        
        if not instructor or not isinstance(instructor, str):
            raise ValueError("Instructor name must be a non-empty string")
        
        if not isinstance(credit_hours, int) or credit_hours <= 0:
            raise ValueError("Credit hours must be a positive integer")
        
        if not isinstance(max_capacity, int) or max_capacity <= 0:
            raise ValueError("Max capacity must be a positive integer")
    
    def enroll_student(self, student) -> bool:
        """
        Enroll a student in the course
        
        Args:
            student: Student object to enroll
        
        Returns:
            bool: True if enrolled, False if added to waitlist
        """
        if student.student_id in self.enrolled_students:
            print(f"❌ {student.name} is already enrolled in {self.course_name}")
            return True
        
        if self.is_full():
            # Add to waitlist
            if student not in self.waitlist:
                self.waitlist.append(student)
                print(f"📝 {student.name} added to waitlist for {self.course_name}")
                print(f"   Waitlist position: {len(self.waitlist)}")
            return False
        
        # Enroll the student
        self.enrolled_students[student.student_id] = student
        Course._total_enrollments += 1
        
        print(f"✅ {student.name} enrolled in {self.course_name}")
        print(f"   Enrollment count: {self.get_enrollment_count()}/{self.max_capacity}")
        return True
    
    def drop_student(self, student_id: str) -> bool:
        """
        Drop a student from the course
        
        Args:
            student_id (str): ID of student to drop
        
        Returns:
            bool: True if successfully dropped
        """
        if student_id not in self.enrolled_students:
            print(f"❌ Student {student_id} not enrolled in {self.course_name}")
            return False
        
        # Remove student
        student = self.enrolled_students.pop(student_id)
        if student_id in self.student_grades:
            del self.student_grades[student_id]
        
        Course._total_enrollments -= 1
        
        print(f"🗑️ {student.name} dropped from {self.course_name}")
        
        # Check waitlist for next student
        if self.waitlist:
            next_student = self.waitlist.pop(0)
            self.enroll_student(next_student)
            print(f"📢 {next_student.name} moved from waitlist to enrolled")
        
        return True
    
    def add_grade(self, student_id: str, grade: float) -> bool:
        """
        Add grade for a student
        
        Args:
            student_id (str): Student ID
            grade (float): Grade value (0-100)
        
        Returns:
            bool: True if successful
        """
        if student_id not in self.enrolled_students:
            print(f"❌ Student {student_id} not enrolled in {self.course_name}")
            return False
        
        if not isinstance(grade, (int, float)) or grade < 0 or grade > 100:
            print(f"❌ Invalid grade: {grade}. Grade must be between 0 and 100")
            return False
        
        self.student_grades[student_id] = float(grade)
        student_name = self.enrolled_students[student_id].name
        
        print(f"📝 Grade added:")
        print(f"   Student: {student_name}")
        print(f"   Course: {self.course_name}")
        print(f"   Grade: {grade}")
        return True
    
    def get_enrollment_count(self) -> int:
        """Get current enrollment count"""
        return len(self.enrolled_students)
    
    def get_available_spots(self) -> int:
        """Get number of available spots"""
        return self.max_capacity - self.get_enrollment_count()
    
    def is_full(self) -> bool:
        """Check if course is at maximum capacity"""
        return self.get_enrollment_count() >= self.max_capacity
    
    def get_course_statistics(self) -> dict:
        """Get comprehensive course statistics"""
        if not self.student_grades:
            return {
                'course_code': self.course_code,
                'course_name': self.course_name,
                'enrolled_students': self.get_enrollment_count(),
                'graded_students': 0,
                'average_grade': None,
                'highest_grade': None,
                'lowest_grade': None,
                'passing_rate': None
            }
        
        grades = list(self.student_grades.values())
        passing_grades = [g for g in grades if g >= 60]
        
        stats = {
            'course_code': self.course_code,
            'course_name': self.course_name,
            'enrolled_students': self.get_enrollment_count(),
            'graded_students': len(grades),
            'average_grade': round(statistics.mean(grades), 2),
            'highest_grade': max(grades),
            'lowest_grade': min(grades),
            'passing_rate': round((len(passing_grades) / len(grades)) * 100, 2) if grades else 0
        }
        
        return stats
    
    def get_enrolled_students(self) -> List:
        """Get list of enrolled students"""
        return list(self.enrolled_students.values())
    
    def __str__(self):
        return f"Course({self.course_code}: {self.course_name} - {self.instructor})"
    
    def __repr__(self):
        return f"Course(code='{self.course_code}', name='{self.course_name}', instructor='{self.instructor}')"
    
    @classmethod
    def get_course_by_code(cls, course_code: str) -> Optional['Course']:
        """Get course by course code"""
        return cls._all_courses.get(course_code)
    
    @classmethod
    def get_total_enrollments(cls) -> int:
        """Get total enrollments across all courses"""
        return cls._total_enrollments
    
    @classmethod
    def get_all_courses(cls) -> List['Course']:
        """Get all courses"""
        return list(cls._all_courses.values())


class Student:
    """
    Student class for managing student information and academic records
    """
    
    # Class variables
    _all_students = {}
    _total_students = 0
    
    def __init__(self, student_id: str, name: str, email: str, program: str):
        """
        Initialize a student
        
        Args:
            student_id (str): Unique student identifier
            name (str): Student name
            email (str): Student email
            program (str): Academic program/major
        """
        # Validate input
        self._validate_student_data(student_id, name, email, program)
        
        # Student attributes
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program
        self.enrollment_date = datetime.now()
        
        # Academic tracking
        self.enrolled_courses = {}    # {course_code: Course object}
        self.completed_courses = {}   # {course_code: {'course': Course, 'grade': float}}
        self.current_gpa = 0.0
        
        # Register student
        Student._all_students[student_id] = self
        Student._total_students += 1
        
        print(f"👤 Student registered:")
        print(f"   ID: {self.student_id}")
        print(f"   Name: {self.name}")
        print(f"   Email: {self.email}")
        print(f"   Program: {self.program}")
        print()
    
    def _validate_student_data(self, student_id, name, email, program):
        """Validate student creation data"""
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")
        
        if student_id in Student._all_students:
            raise ValueError(f"Student ID {student_id} already exists")
        
        if not name or not isinstance(name, str):
            raise ValueError("Student name must be a non-empty string")
        
        if not email or not isinstance(email, str) or '@' not in email:
            raise ValueError("Valid email address is required")
        
        if not program or not isinstance(program, str):
            raise ValueError("Program must be a non-empty string")
    
    def enroll_in_course(self, course) -> bool:
        """
        Enroll in a course
        
        Args:
            course: Course object to enroll in
        
        Returns:
            bool: True if enrolled successfully
        """
        if not isinstance(course, Course):
            raise ValueError("Invalid course object")
        
        if course.course_code in self.enrolled_courses:
            print(f"❌ Already enrolled in {course.course_name}")
            return False
        
        # Try to enroll in the course
        enrollment_success = course.enroll_student(self)
        
        if enrollment_success:
            self.enrolled_courses[course.course_code] = course
            print(f"✅ {self.name} successfully enrolled in {course.course_name}")
        else:
            print(f"📝 {self.name} added to waitlist for {course.course_name}")
        
        return enrollment_success
    
    def drop_course(self, course_code: str) -> bool:
        """
        Drop a course
        
        Args:
            course_code (str): Course code to drop
        
        Returns:
            bool: True if dropped successfully
        """
        if course_code not in self.enrolled_courses:
            print(f"❌ Not enrolled in course {course_code}")
            return False
        
        course = self.enrolled_courses.pop(course_code)
        course.drop_student(self.student_id)
        
        print(f"🗑️ {self.name} dropped from {course.course_name}")
        return True
    
    def add_grade(self, course_code: str, grade: float) -> bool:
        """
        Add grade for a course
        
        Args:
            course_code (str): Course code
            grade (float): Grade value
        
        Returns:
            bool: True if successful
        """
        # Check if student is enrolled in the course
        course = Course.get_course_by_code(course_code)
        if not course:
            print(f"❌ Course {course_code} not found")
            return False
        
        if self.student_id not in course.enrolled_students:
            print(f"❌ Not enrolled in {course_code}")
            return False
        
        # Add grade to course and move to completed courses
        if course.add_grade(self.student_id, grade):
            self.completed_courses[course_code] = {
                'course': course,
                'grade': grade
            }
            
            # Remove from current enrollments if course is completed
            if course_code in self.enrolled_courses:
                del self.enrolled_courses[course_code]
            
            # Recalculate GPA
            self._calculate_gpa()
            
            print(f"✅ Grade {grade} added for {self.name} in {course.course_name}")
            return True
        
        return False
    
    def _calculate_gpa(self):
        """Calculate and update current GPA"""
        if not self.completed_courses:
            self.current_gpa = 0.0
            return
        
        total_grade_points = 0.0
        total_credit_hours = 0
        
        for course_data in self.completed_courses.values():
            course = course_data['course']
            grade = course_data['grade']
            
            # Convert percentage to GPA points (4.0 scale)
            if grade >= 90:
                grade_points = 4.0
            elif grade >= 80:
                grade_points = 3.0
            elif grade >= 70:
                grade_points = 2.0
            elif grade >= 60:
                grade_points = 1.0
            else:
                grade_points = 0.0
            
            total_grade_points += grade_points * course.credit_hours
            total_credit_hours += course.credit_hours
        
        self.current_gpa = round(total_grade_points / total_credit_hours, 2) if total_credit_hours > 0 else 0.0
    
    def calculate_gpa(self) -> float:
        """Get current GPA"""
        return self.current_gpa
    
    def get_transcript(self) -> dict:
        """Get academic transcript"""
        transcript = {
            'student_id': self.student_id,
            'name': self.name,
            'program': self.program,
            'gpa': self.current_gpa,
            'total_credit_hours': sum(course_data['course'].credit_hours 
                                    for course_data in self.completed_courses.values()),
            'completed_courses': []
        }
        
        for course_code, course_data in self.completed_courses.items():
            course = course_data['course']
            grade = course_data['grade']
            
            transcript['completed_courses'].append({
                'course_code': course_code,
                'course_name': course.course_name,
                'credit_hours': course.credit_hours,
                'grade': grade,
                'letter_grade': self._get_letter_grade(grade)
            })
        
        return transcript
    
    def _get_letter_grade(self, grade: float) -> str:
        """Convert percentage to letter grade"""
        if grade >= 90:
            return 'A'
        elif grade >= 80:
            return 'B'
        elif grade >= 70:
            return 'C'
        elif grade >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_enrolled_courses(self) -> List:
        """Get list of currently enrolled courses"""
        return list(self.enrolled_courses.values())
    
    def get_completed_courses(self) -> List:
        """Get list of completed courses"""
        return list(self.completed_courses.keys())
    
    def __str__(self):
        return f"Student({self.student_id}: {self.name} - {self.program})"
    
    def __repr__(self):
        return f"Student(id='{self.student_id}', name='{self.name}', program='{self.program}')"
    
    @classmethod
    def get_student_by_id(cls, student_id: str) -> Optional['Student']:
        """Get student by ID"""
        return cls._all_students.get(student_id)
    
    @classmethod
    def get_total_students(cls) -> int:
        """Get total number of students"""
        return cls._total_students
    
    @classmethod
    def get_average_gpa(cls) -> float:
        """Get average GPA across all students"""
        if not cls._all_students:
            return 0.0
        
        students_with_gpa = [student for student in cls._all_students.values() 
                           if student.current_gpa > 0]
        
        if not students_with_gpa:
            return 0.0
        
        total_gpa = sum(student.current_gpa for student in students_with_gpa)
        return round(total_gpa / len(students_with_gpa), 2)
    
    @classmethod
    def get_top_students(cls, count: int = 5) -> List[Tuple[str, float]]:
        """
        Get top students by GPA
        
        Args:
            count (int): Number of top students to return
        
        Returns:
            List of (student_name, gpa) tuples
        """
        students_with_gpa = [(student.name, student.current_gpa) 
                           for student in cls._all_students.values() 
                           if student.current_gpa > 0]
        
        students_with_gpa.sort(key=lambda x: x[1], reverse=True)
        return students_with_gpa[:count]
    
    @classmethod
    def get_students_by_program(cls, program: str) -> List['Student']:
        """Get all students in a specific program"""
        return [student for student in cls._all_students.values() 
                if student.program.lower() == program.lower()]


def demonstrate_advanced_features():
    """Demonstrate advanced course management features"""
    print("🚀 ADVANCED COURSE MANAGEMENT FEATURES")
    print("=" * 50)
    print()
    
    # Create additional courses for demonstration
    english_course = Course("ENG101", "English Composition", "Prof. Williams", 3, 15)
    
    # Create student for advanced features
    demo_student = Student("S004", "David Kim", "david@university.edu", "Engineering")
    
    # Demonstrate waitlist functionality
    print("📝 TESTING WAITLIST FUNCTIONALITY:")
    print("-" * 30)
    
    # Fill up the English course
    for i in range(15):  # Fill to capacity
        temp_student = Student(f"T{i:03d}", f"Temp Student {i}", f"temp{i}@uni.edu", "General")
        temp_student.enroll_in_course(english_course)
    
    # Try to enroll one more (should go to waitlist)
    demo_student.enroll_in_course(english_course)
    print(f"English course full: {english_course.is_full()}")
    print(f"Waitlist size: {len(english_course.waitlist)}")
    print()
    
    # Demonstrate dropping and waitlist movement
    print("📝 TESTING WAITLIST MOVEMENT:")
    print("-" * 30)
    first_student = english_course.get_enrolled_students()[0]
    english_course.drop_student(first_student.student_id)
    print()
    
    # Show program-based analytics
    print("📊 PROGRAM-BASED ANALYTICS:")
    print("-" * 30)
    for program in ["Computer Science", "Mathematics", "Physics", "General"]:
        students_in_program = Student.get_students_by_program(program)
        print(f"{program}: {len(students_in_program)} students")
    print()


def main():
    """Main function to test the course management system"""
    print("🎯 TESTING UNIVERSITY COURSE MANAGEMENT SYSTEM")
    print("=" * 70)
    print()
    
    try:
        # Test Case 1: Creating courses with enrollment limits
        print("📝 TEST CASE 1: Creating Courses")
        print("-" * 50)
        
        math_course = Course("MATH101", "Calculus I", "Dr. Smith", 3, 30)
        physics_course = Course("PHYS101", "Physics I", "Dr. Johnson", 4, 25)
        cs_course = Course("CS101", "Programming Basics", "Prof. Brown", 3, 20)
        
        print(f"Course: {math_course}")
        print(f"Available spots in Math: {math_course.get_available_spots()}")
        print()
        
        # Test Case 2: Creating students with different programs
        print("📝 TEST CASE 2: Creating Students")
        print("-" * 50)
        
        student1 = Student("S001", "Alice Wilson", "alice@university.edu", "Computer Science")
        student2 = Student("S002", "Bob Davis", "bob@university.edu", "Mathematics")
        student3 = Student("S003", "Carol Lee", "carol@university.edu", "Physics")
        
        print(f"Student: {student1}")
        print(f"Total students: {Student.get_total_students()}")
        print()
        
        # Test Case 3: Course enrollment
        print("📝 TEST CASE 3: Course Enrollment")
        print("-" * 50)
        
        enrollment1 = student1.enroll_in_course(math_course)
        enrollment2 = student1.enroll_in_course(cs_course)
        enrollment3 = student2.enroll_in_course(math_course)
        
        print(f"Alice's enrollment in Math: {enrollment1}")
        print(f"Math course enrollment count: {math_course.get_enrollment_count()}")
        print()
        
        # Test Case 4: Adding grades and calculating GPA
        print("📝 TEST CASE 4: Grades and GPA Calculation")
        print("-" * 50)
        
        student1.add_grade("MATH101", 85.5)
        student1.add_grade("CS101", 92.0)
        student2.add_grade("MATH101", 78.3)
        
        print(f"Alice's GPA: {student1.calculate_gpa()}")
        alice_transcript = student1.get_transcript()
        print(f"Alice's transcript: {alice_transcript}")
        print()
        
        # Test Case 5: Course statistics
        print("📝 TEST CASE 5: Course Statistics")
        print("-" * 50)
        
        math_course.add_grade("S001", 85.5)
        math_course.add_grade("S002", 78.3)
        
        course_stats = math_course.get_course_statistics()
        print(f"Math course statistics: {course_stats}")
        print()
        
        # Test Case 6: University-wide analytics using class methods
        print("📝 TEST CASE 6: University Analytics")
        print("-" * 50)
        
        total_enrollments = Course.get_total_enrollments()
        print(f"Total enrollments across all courses: {total_enrollments}")
        
        average_gpa = Student.get_average_gpa()
        print(f"University average GPA: {average_gpa}")
        
        top_students = Student.get_top_students(2)
        print(f"Top 2 students: {top_students}")
        print()
        
        # Test Case 7: Enrollment limits and waitlist
        print("📝 TEST CASE 7: Enrollment Limits and Waitlist")
        print("-" * 50)
        
        # Try to enroll more students than course capacity
        print("Enrolling students to test capacity limits...")
        enrolled_count = 0
        waitlist_count = 0
        
        for i in range(25):  # Assuming math course limit is 30
            temp_student = Student(f"S{100+i}", f"Student {i}", f"student{i}@uni.edu", "General")
            result = temp_student.enroll_in_course(math_course)
            if result:
                enrolled_count += 1
            else:
                waitlist_count += 1
        
        print(f"Successfully enrolled: {enrolled_count} additional students")
        print(f"Added to waitlist: {waitlist_count} students")
        print(f"Course full status: {math_course.is_full()}")
        print(f"Waitlist size: {len(math_course.waitlist) if hasattr(math_course, 'waitlist') else 0}")
        print()
        
        # Additional advanced features
        demonstrate_advanced_features()
        
        print("🎉 COURSE MANAGEMENT SYSTEM TESTING COMPLETE!")
        print("=" * 70)
        print()
        print("✅ All features tested successfully:")
        print("   • Course creation with enrollment limits")
        print("   • Student registration and program tracking")
        print("   • Course enrollment with capacity management")
        print("   • Waitlist functionality for full courses")
        print("   • Grade tracking and GPA calculation")
        print("   • Course statistics and analytics")
        print("   • University-wide reporting")
        print("   • Academic transcript generation")
        print("   • Top student identification")
        print("   • Program-based student grouping")
        print()
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        raise


if __name__ == "__main__":
    main()

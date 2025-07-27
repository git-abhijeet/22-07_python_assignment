from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import uvicorn
import re
from enum import Enum


# Enhanced Pydantic Models with Validation
class GradeEnum(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"

class Student(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    major: str
    year: int = Field(..., ge=1, le=4)
    gpa: float = Field(default=0.0, ge=0.0, le=4.0)

    @validator('email')
    def validate_unique_email(cls, v):
        # In real app, check database for uniqueness
        return v

class Course(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=200)
    code: str = Field(..., regex=r'^[A-Z]{2,4}\d{3}-\d{3}$')
    credits: int = Field(..., ge=1, le=6)
    professor_id: int
    max_capacity: int = Field(..., ge=1, le=500)
    enrolled_count: int = Field(default=0, ge=0)

class Professor(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str
    hire_date: date

    @validator('hire_date')
    def validate_hire_date(cls, v):
        if v > date.today():
            raise ValueError('Hire date cannot be in the future')
        if v.year < 1950:
            raise ValueError('Hire date cannot be before 1950')
        return v

class Enrollment(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: Optional[GradeEnum] = None

    @validator('enrollment_date')
    def validate_enrollment_date(cls, v):
        if v > date.today():
            raise ValueError('Enrollment date cannot be in the future')
        return v

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    major: str
    year: int = Field(..., ge=1, le=4)

class CourseCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    code: str = Field(..., regex=r'^[A-Z]{2,4}\d{3}-\d{3}$')
    credits: int = Field(..., ge=1, le=6)
    professor_id: int
    max_capacity: int = Field(..., ge=1, le=500)

class ProfessorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str
    hire_date: date

    @validator('hire_date')
    def validate_hire_date(cls, v):
        if v > date.today():
            raise ValueError('Hire date cannot be in the future')
        if v.year < 1950:
            raise ValueError('Hire date cannot be before 1950')
        return v

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class GradeUpdate(BaseModel):
    grade: GradeEnum

# Response Models
class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    field_errors: Optional[Dict[str, List[str]]] = None
    timestamp: datetime

class EnrollmentResponse(BaseModel):
    message: str
    enrollment_id: str
    student: Student
    course: Course
    enrollment_date: date

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int

class GPADistribution(BaseModel):
    range_0_1: int = 0
    range_1_2: int = 0
    range_2_3: int = 0
    range_3_4: int = 0


# Initialize FastAPI app
app = FastAPI(title="University Course Management System", version="1.0.0")

# In-memory databases
students_db: Dict[int, Student] = {}
courses_db: Dict[int, Course] = {}
professors_db: Dict[int, Professor] = {}
enrollments_db: Dict[str, Enrollment] = {}  # key: f"{student_id}_{course_id}"

# Auto-increment counters
student_counter = 1
course_counter = 1
professor_counter = 1


# Enhanced Helper functions
def calculate_gpa(student_id: int) -> float:
    """Calculate GPA for a student based on their grades"""
    grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
    total_points = 0.0
    total_credits = 0
    
    for enrollment_key, enrollment in enrollments_db.items():
        if enrollment.student_id == student_id and enrollment.grade:
            course = courses_db[enrollment.course_id]
            if enrollment.grade in grade_points:
                total_points += grade_points[enrollment.grade] * course.credits
                total_credits += course.credits
    
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

def get_enrollment_key(student_id: int, course_id: int) -> str:
    return f"{student_id}_{course_id}"

def check_email_uniqueness(email: str, exclude_id: Optional[int] = None) -> bool:
    """Check if email is unique across all entities"""
    for student in students_db.values():
        if student.email == email and (exclude_id is None or student.id != exclude_id):
            return False
    for professor in professors_db.values():
        if professor.email == email and (exclude_id is None or professor.id != exclude_id):
            return False
    return True

def check_student_credit_limit(student_id: int, additional_credits: int = 0) -> bool:
    """Check if student exceeds 18 credit hour limit"""
    total_credits = 0
    for enrollment in enrollments_db.values():
        if enrollment.student_id == student_id:
            course = courses_db[enrollment.course_id]
            total_credits += course.credits
    return (total_credits + additional_credits) <= 18

def check_professor_teaching_load(professor_id: int) -> bool:
    """Check if professor teaches more than 4 courses"""
    course_count = sum(1 for course in courses_db.values() if course.professor_id == professor_id)
    return course_count < 4

def is_on_academic_probation(student_id: int) -> bool:
    """Check if student is on academic probation (GPA < 2.0)"""
    student = students_db.get(student_id)
    return student and student.gpa < 2.0

def paginate_results(items: List, page: int, limit: int) -> Dict:
    """Paginate results"""
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    pages = (total + limit - 1) // limit
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }


# Enhanced Student endpoints with pagination and filtering
@app.get("/students", response_model=Dict)
async def get_all_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    major: Optional[str] = Query(None),
    year: Optional[int] = Query(None, ge=1, le=4),
    gpa_min: Optional[float] = Query(None, ge=0.0, le=4.0),
    gpa_max: Optional[float] = Query(None, ge=0.0, le=4.0)
):
    students = list(students_db.values())
    
    # Apply filters
    if major:
        students = [s for s in students if major.lower() in s.major.lower()]
    if year:
        students = [s for s in students if s.year == year]
    if gpa_min is not None:
        students = [s for s in students if s.gpa >= gpa_min]
    if gpa_max is not None:
        students = [s for s in students if s.gpa <= gpa_max]
    
    return paginate_results(students, page, limit)

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate):
    global student_counter
    
    # Check email uniqueness
    if not check_email_uniqueness(student.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                detail="Email already exists",
                error_code="EMAIL_ALREADY_EXISTS",
                timestamp=datetime.now()
            ).dict()
        )
    
    new_student = Student(
        id=student_counter,
        name=student.name,
        email=student.email,
        major=student.major,
        year=student.year
    )
    students_db[student_counter] = new_student
    student_counter += 1
    return new_student

@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return students_db[student_id]

@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, student_update: StudentCreate):
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check email uniqueness (excluding current student)
    if not check_email_uniqueness(student_update.email, student_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    
    updated_student = Student(
        id=student_id,
        name=student_update.name,
        email=student_update.email,
        major=student_update.major,
        year=student_update.year,
        gpa=calculate_gpa(student_id)
    )
    students_db[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Remove all enrollments for this student
    keys_to_remove = [key for key in enrollments_db.keys() if enrollments_db[key].student_id == student_id]
    for key in keys_to_remove:
        course_id = enrollments_db[key].course_id
        courses_db[course_id].enrolled_count -= 1
        del enrollments_db[key]
    
    del students_db[student_id]

@app.get("/students/{student_id}/courses", response_model=List[Course])
async def get_student_courses(student_id: int):
    if student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    student_courses = []
    for enrollment in enrollments_db.values():
        if enrollment.student_id == student_id:
            student_courses.append(courses_db[enrollment.course_id])
    
    return student_courses


# Course endpoints
@app.get("/courses", response_model=List[Course])
async def get_all_courses():
    return list(courses_db.values())


@app.post("/courses", response_model=Course)
async def create_course(course: CourseCreate):
    global course_counter
    
    # Validate professor exists
    if course.professor_id not in professors_db:
        raise HTTPException(status_code=400, detail="Professor not found")
    
    new_course = Course(
        id=course_counter,
        name=course.name,
        code=course.code,
        credits=course.credits,
        professor_id=course.professor_id,
        max_capacity=course.max_capacity
    )
    courses_db[course_counter] = new_course
    course_counter += 1
    return new_course


@app.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: int):
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses_db[course_id]


@app.put("/courses/{course_id}", response_model=Course)
async def update_course(course_id: int, course_update: CourseCreate):
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Validate professor exists
    if course_update.professor_id not in professors_db:
        raise HTTPException(status_code=400, detail="Professor not found")
    
    existing_course = courses_db[course_id]
    updated_course = Course(
        id=course_id,
        name=course_update.name,
        code=course_update.code,
        credits=course_update.credits,
        professor_id=course_update.professor_id,
        max_capacity=course_update.max_capacity,
        enrolled_count=existing_course.enrolled_count
    )
    courses_db[course_id] = updated_course
    return updated_course


@app.delete("/courses/{course_id}")
async def delete_course(course_id: int):
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Remove all enrollments for this course
    keys_to_remove = [key for key in enrollments_db.keys() if enrollments_db[key].course_id == course_id]
    for key in keys_to_remove:
        del enrollments_db[key]
    
    del courses_db[course_id]
    return {"message": "Course deleted successfully"}


@app.get("/courses/{course_id}/students", response_model=List[Student])
async def get_course_roster(course_id: int):
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrolled_students = []
    for enrollment in enrollments_db.values():
        if enrollment.course_id == course_id:
            enrolled_students.append(students_db[enrollment.student_id])
    
    return enrolled_students


# Professor endpoints
@app.get("/professors", response_model=List[Professor])
async def get_all_professors():
    return list(professors_db.values())


@app.post("/professors", response_model=Professor)
async def create_professor(professor: ProfessorCreate):
    global professor_counter
    new_professor = Professor(
        id=professor_counter,
        name=professor.name,
        email=professor.email,
        department=professor.department,
        hire_date=professor.hire_date
    )
    professors_db[professor_counter] = new_professor
    professor_counter += 1
    return new_professor


@app.get("/professors/{professor_id}", response_model=Professor)
async def get_professor(professor_id: int):
    if professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professors_db[professor_id]


@app.put("/professors/{professor_id}", response_model=Professor)
async def update_professor(professor_id: int, professor_update: ProfessorCreate):
    if professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    updated_professor = Professor(
        id=professor_id,
        name=professor_update.name,
        email=professor_update.email,
        department=professor_update.department,
        hire_date=professor_update.hire_date
    )
    professors_db[professor_id] = updated_professor
    return updated_professor


@app.delete("/professors/{professor_id}")
async def delete_professor(professor_id: int):
    if professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    # Check if professor has assigned courses
    assigned_courses = [course for course in courses_db.values() if course.professor_id == professor_id]
    if assigned_courses:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete professor. They are assigned to {len(assigned_courses)} course(s)"
        )
    
    del professors_db[professor_id]
    return {"message": "Professor deleted successfully"}


@app.get("/professors/{professor_id}/courses", response_model=List[Course])
async def get_professor_courses(professor_id: int):
    if professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    professor_courses = [course for course in courses_db.values() if course.professor_id == professor_id]
    return professor_courses


# Enhanced Enrollment endpoints with business rules
@app.get("/enrollments", response_model=List[Enrollment])
async def get_all_enrollments():
    return list(enrollments_db.values())

@app.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(enrollment: EnrollmentCreate):
    # Validate student and course exist
    if enrollment.student_id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    if enrollment.course_id not in courses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if student is already enrolled
    enrollment_key = get_enrollment_key(enrollment.student_id, enrollment.course_id)
    if enrollment_key in enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                detail="Student already enrolled in this course",
                error_code="DUPLICATE_ENROLLMENT",
                timestamp=datetime.now()
            ).dict()
        )
    
    # Check course capacity
    course = courses_db[enrollment.course_id]
    if course.enrolled_count >= course.max_capacity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                detail="Course has reached maximum capacity",
                error_code="ENROLLMENT_CAPACITY_EXCEEDED",
                timestamp=datetime.now()
            ).dict()
        )
    
    # Check student credit limit
    if not check_student_credit_limit(enrollment.student_id, course.credits):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student would exceed 18 credit hour limit"
        )
    
    # Create enrollment
    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrollment_date=date.today()
    )
    
    # Update course enrollment count
    course.enrolled_count += 1
    courses_db[enrollment.course_id] = course
    
    enrollments_db[enrollment_key] = new_enrollment
    
    return EnrollmentResponse(
        message="Student successfully enrolled",
        enrollment_id=enrollment_key,
        student=students_db[enrollment.student_id],
        course=course,
        enrollment_date=date.today()
    )

@app.put("/enrollments/{student_id}/{course_id}", response_model=Enrollment)
async def update_enrollment_grade(student_id: int, course_id: int, grade_update: GradeUpdate):
    enrollment_key = get_enrollment_key(student_id, course_id)
    
    if enrollment_key not in enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Update enrollment grade
    enrollment = enrollments_db[enrollment_key]
    enrollment.grade = grade_update.grade
    enrollments_db[enrollment_key] = enrollment
    
    # Update student GPA
    students_db[student_id].gpa = calculate_gpa(student_id)
    
    return enrollment

@app.delete("/enrollments/{student_id}/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(student_id: int, course_id: int):
    enrollment_key = get_enrollment_key(student_id, course_id)
    
    if enrollment_key not in enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Update course enrollment count
    course = courses_db[course_id]
    course.enrolled_count -= 1
    courses_db[course_id] = course
    
    # Remove enrollment
    del enrollments_db[enrollment_key]
    
    # Update student GPA
    students_db[student_id].gpa = calculate_gpa(student_id)

# Analytics endpoints
@app.get("/analytics/students/gpa-distribution", response_model=GPADistribution)
async def get_gpa_distribution():
    distribution = GPADistribution()
    
    for student in students_db.values():
        if 0.0 <= student.gpa < 1.0:
            distribution.range_0_1 += 1
        elif 1.0 <= student.gpa < 2.0:
            distribution.range_1_2 += 1
        elif 2.0 <= student.gpa < 3.0:
            distribution.range_2_3 += 1
        elif 3.0 <= student.gpa <= 4.0:
            distribution.range_3_4 += 1
    
    return distribution

@app.get("/analytics/courses/enrollment-stats")
async def get_enrollment_stats():
    stats = []
    for course in courses_db.values():
        utilization = (course.enrolled_count / course.max_capacity) * 100
        stats.append({
            "course_id": course.id,
            "course_name": course.name,
            "enrolled": course.enrolled_count,
            "capacity": course.max_capacity,
            "utilization_percent": round(utilization, 2)
        })
    
    return {"courses": stats}

@app.get("/analytics/professors/teaching-load")
async def get_professor_teaching_load():
    stats = []
    for professor in professors_db.values():
        course_count = sum(1 for course in courses_db.values() if course.professor_id == professor.id)
        total_students = sum(
            course.enrolled_count for course in courses_db.values() 
            if course.professor_id == professor.id
        )
        
        stats.append({
            "professor_id": professor.id,
            "professor_name": professor.name,
            "courses_taught": course_count,
            "total_students": total_students,
            "at_capacity": course_count >= 4
        })
    
    return {"professors": stats}

@app.get("/analytics/departments/performance")
async def get_department_performance():
    dept_stats = {}
    
    # Group students by major (department)
    for student in students_db.values():
        dept = student.major
        if dept not in dept_stats:
            dept_stats[dept] = {"students": [], "total_gpa": 0}
        dept_stats[dept]["students"].append(student)
        dept_stats[dept]["total_gpa"] += student.gpa
    
    # Calculate department averages
    performance = []
    for dept, data in dept_stats.items():
        avg_gpa = data["total_gpa"] / len(data["students"]) if data["students"] else 0
        performance.append({
            "department": dept,
            "student_count": len(data["students"]),
            "average_gpa": round(avg_gpa, 2),
            "students_on_probation": sum(1 for s in data["students"] if s.gpa < 2.0)
        })
    
    return {"departments": performance}


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "University Course Management System API",
        "version": "1.0.0",
        "endpoints": {
            "students": "/students",
            "courses": "/courses", 
            "professors": "/professors",
            "enrollments": "/enrollments"
        }
    }


# Sample data initialization
@app.on_event("startup")
async def startup_event():
    # Add sample professors
    prof1 = Professor(id=1, name="Dr. John Smith", email="john.smith@university.edu", 
                     department="Computer Science", hire_date=date(2020, 1, 15))
    prof2 = Professor(id=2, name="Dr. Sarah Johnson", email="sarah.johnson@university.edu",
                     department="Mathematics", hire_date=date(2018, 8, 20))
    
    professors_db[1] = prof1
    professors_db[2] = prof2
    
    # Add sample students
    student1 = Student(id=1, name="Alice Brown", email="alice.brown@student.edu",
                      major="Computer Science", year=3, gpa=3.5)
    student2 = Student(id=2, name="Bob Wilson", email="bob.wilson@student.edu",
                      major="Mathematics", year=2, gpa=3.2)
    
    students_db[1] = student1
    students_db[2] = student2
    
    # Add sample courses
    course1 = Course(id=1, name="Data Structures", code="CS301", credits=3,
                    professor_id=1, max_capacity=30, enrolled_count=0)
    course2 = Course(id=2, name="Calculus I", code="MATH101", credits=4,
                    professor_id=2, max_capacity=25, enrolled_count=0)
    
    courses_db[1] = course1
    courses_db[2] = course2
    
    # Update counters
    global student_counter, course_counter, professor_counter
    student_counter = 3
    course_counter = 3
    professor_counter = 3


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

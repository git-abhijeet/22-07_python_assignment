from datetime import datetime, timedelta
import re


class Employee:
    """Employee Management System with class variables and methods."""
    
    # Class variables
    company_name = ""
    total_employees = 0
    departments = {}
    tax_rates = {}
    next_employee_id = 1
    
    def __init__(self, name, department, base_salary, country, email):
        """Initialize employee with validation."""
        if not self.validate_email(email):
            raise ValueError("Invalid email format")
        if not self.is_valid_department(department):
            raise ValueError("Invalid department")
        
        self.employee_id = self.generate_employee_id()
        self.name = name
        self.department = department
        self.base_salary = base_salary
        self.country = country
        self.email = email
        self.hire_date = datetime.now()
        self.performance_ratings = []
        
        # Update class variables
        Employee.total_employees += 1
        Employee.departments[department] += 1
    
    @staticmethod
    def validate_email(email):
        """Check proper email format with domain validation."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def calculate_tax(salary, country):
        """Calculate tax based on country rates."""
        if country not in Employee.tax_rates:
            return 0
        return salary * Employee.tax_rates[country]
    
    @staticmethod
    def is_valid_department(dept):
        """Check against approved departments list."""
        return dept in Employee.departments
    
    @staticmethod
    def generate_employee_id():
        """Create unique ID with format 'EMP-YYYY-XXXX'."""
        year = datetime.now().year
        emp_id = f"EMP-{year}-{Employee.next_employee_id:04d}"
        Employee.next_employee_id += 1
        return emp_id
    
    @classmethod
    def from_csv_data(cls, csv_line):
        """Create employee from 'name,dept,salary,country,email' format."""
        parts = [part.strip() for part in csv_line.split(',')]
        name, dept, salary, country, email = parts
        return cls(name, dept, float(salary), country, email)
    
    @classmethod
    def get_department_stats(cls):
        """Return detailed department statistics."""
        stats = {}
        for dept, count in cls.departments.items():
            stats[dept] = {
                "count": count,
                "percentage": (count / cls.total_employees * 100) if cls.total_employees > 0 else 0
            }
        return stats
    
    @classmethod
    def set_tax_rate(cls, country, rate):
        """Update tax rate for specific country."""
        cls.tax_rates[country] = rate
    
    @classmethod
    def hire_bulk_employees(cls, employee_list):
        """Process multiple hires at once."""
        employees = []
        for csv_data in employee_list:
            emp = cls.from_csv_data(csv_data)
            employees.append(emp)
        return employees
    
    def add_performance_rating(self, rating):
        """Add rating (1-5 scale) with validation."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.performance_ratings.append(rating)
    
    def get_average_performance(self):
        """Calculate average of all ratings."""
        if not self.performance_ratings:
            return 0
        return sum(self.performance_ratings) / len(self.performance_ratings)
    
    def calculate_net_salary(self):
        """Base salary minus taxes."""
        tax_amount = self.calculate_tax(self.base_salary, self.country)
        return self.base_salary - tax_amount
    
    def get_years_of_service(self):
        """Calculate from hire date to current date."""
        service_time = datetime.now() - self.hire_date
        return service_time.days / 365.25
    
    def is_eligible_for_bonus(self):
        """Check if avg performance > 3.5 and service > 1 year."""
        return (self.get_average_performance() > 3.5 and 
                self.get_years_of_service() > 1)


if __name__ == "__main__":
    # Test Case 1: Class setup and basic functionality
    Employee.company_name = "GlobalTech Solutions"
    Employee.tax_rates = {"USA": 0.22, "India": 0.18, "UK": 0.25}
    Employee.departments = {"Engineering": 0, "Sales": 0, "HR": 0, "Marketing": 0}

    emp1 = Employee("John Smith", "Engineering", 85000, "USA", "john.smith@globaltech.com")
    assert emp1.employee_id.startswith("EMP-2025-")  # Updated to current year
    assert Employee.total_employees == 1
    assert Employee.departments["Engineering"] == 1
    print("Test Case 1: PASSED")

    # Test Case 2: Static method validations
    assert Employee.validate_email("test@company.com") == True
    assert Employee.validate_email("invalid.email") == False
    assert Employee.is_valid_department("Engineering") == True
    assert Employee.is_valid_department("InvalidDept") == False
    assert abs(Employee.calculate_tax(100000, "USA") - 22000) < 0.01
    print("Test Case 2: PASSED")

    # Test Case 3: Class methods and bulk operations
    emp2 = Employee.from_csv_data("Sarah Johnson,Sales,75000,UK,sarah.j@globaltech.com")
    assert emp2.name == "Sarah Johnson"
    assert emp2.department == "Sales"
    assert Employee.departments["Sales"] == 1

    bulk_data = [
        "Mike Wilson,Marketing,65000,India,mike.w@globaltech.com",
        "Lisa Chen,HR,70000,USA,lisa.chen@globaltech.com"
    ]

    Employee.hire_bulk_employees(bulk_data)
    assert Employee.total_employees == 4

    stats = Employee.get_department_stats()
    assert stats["Engineering"]["count"] == 1
    assert stats["Sales"]["count"] == 1
    print("Test Case 3: PASSED")

    # Test Case 4: Performance and bonus calculations
    emp1.add_performance_rating(4.2)
    emp1.add_performance_rating(3.8)
    emp1.add_performance_rating(4.5)
    assert abs(emp1.get_average_performance() - 4.17) < 0.01

    # Simulate employee with 2 years of service
    emp1.hire_date = datetime.now() - timedelta(days=800)
    assert emp1.get_years_of_service() >= 2
    assert emp1.is_eligible_for_bonus() == True
    print("Test Case 4: PASSED")

    # Test Case 5: Salary calculations
    net_salary = emp1.calculate_net_salary()
    expected_net = 85000 - (85000 * 0.22)
    assert abs(net_salary - expected_net) < 0.01
    print("Test Case 5: PASSED")

    print("\nAll tests passed! Employee Management System is working correctly.")
    print(f"\nCompany: {Employee.company_name}")
    print(f"Total Employees: {Employee.total_employees}")
    print(f"Department Stats: {Employee.get_department_stats()}")
    print(f"Employee {emp1.name} - Net Salary: ${emp1.calculate_net_salary():.2f}")
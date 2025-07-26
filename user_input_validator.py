# User Input Validator
# This program demonstrates robust input validation with error handling

def validate_integer_range(prompt, min_value, max_value):
    """
    Validates integer input within a specified range
    
    Args:
        prompt (str): The prompt message to display
        min_value (int): Minimum allowed value
        max_value (int): Maximum allowed value
    
    Returns:
        int: Valid integer within the specified range
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Check for empty input
            if not user_input:
                print("Empty input. Please enter a value.")
                continue
            
            # Try to convert to integer
            value = int(user_input)
            
            # Check if value is within range
            if value < min_value or value > max_value:
                print(f"Out of range. Please enter a number between {min_value} and {max_value}.")
                continue
            
            return value
            
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            return None

def validate_float_range(prompt, min_value, max_value):
    """
    Validates float input within a specified range
    
    Args:
        prompt (str): The prompt message to display
        min_value (float): Minimum allowed value
        max_value (float): Maximum allowed value
    
    Returns:
        float: Valid float within the specified range
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Check for empty input
            if not user_input:
                print("Empty input. Please enter a value.")
                continue
            
            # Try to convert to float
            value = float(user_input)
            
            # Check if value is within range
            if value < min_value or value > max_value:
                print(f"Out of range. Please enter a number between {min_value} and {max_value}.")
                continue
            
            return value
            
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            return None

def validate_string_length(prompt, min_length=1, max_length=100):
    """
    Validates string input with length constraints
    
    Args:
        prompt (str): The prompt message to display
        min_length (int): Minimum string length
        max_length (int): Maximum string length
    
    Returns:
        str: Valid string within length constraints
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Check for empty input
            if len(user_input) < min_length:
                if min_length == 1:
                    print("Empty input. Please enter a value.")
                else:
                    print(f"Input too short. Please enter at least {min_length} characters.")
                continue
            
            # Check maximum length
            if len(user_input) > max_length:
                print(f"Input too long. Please enter no more than {max_length} characters.")
                continue
            
            return user_input
            
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            return None

def validate_email(prompt):
    """
    Validates email format
    
    Args:
        prompt (str): The prompt message to display
    
    Returns:
        str: Valid email address
    """
    import re
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Check for empty input
            if not user_input:
                print("Empty input. Please enter an email address.")
                continue
            
            # Validate email format
            if not re.match(email_pattern, user_input):
                print("Invalid email format. Please enter a valid email address (e.g., user@example.com).")
                continue
            
            return user_input
            
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            return None

def validate_choice(prompt, valid_choices):
    """
    Validates user choice from a list of valid options
    
    Args:
        prompt (str): The prompt message to display
        valid_choices (list): List of valid choices
    
    Returns:
        str: Valid choice from the list
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Check for empty input
            if not user_input:
                print("Empty input. Please enter a choice.")
                continue
            
            # Check if choice is valid (case-insensitive)
            if user_input.lower() not in [choice.lower() for choice in valid_choices]:
                print(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")
                continue
            
            # Return the choice in original case from valid_choices
            for choice in valid_choices:
                if choice.lower() == user_input.lower():
                    return choice
            
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            return None

def validate_phone_number(prompt):
    """
    Validates phone number format
    
    Args:
        prompt (str): The prompt message to display
    
    Returns:
        str: Valid phone number
    """
    import re
    
    # Phone number pattern (supports various formats)
    phone_pattern = r'^(\+\d{1,3}[- ]?)?\d{10}$|^(\+\d{1,3}[- ]?)?\(\d{3}\)[- ]?\d{3}[- ]?\d{4}$'
    
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Check for empty input
            if not user_input:
                print("Empty input. Please enter a phone number.")
                continue
            
            # Remove spaces and dashes for validation
            clean_input = re.sub(r'[- ()]', '', user_input)
            
            # Check if it contains only digits and optional +
            if not re.match(r'^\+?\d+$', clean_input):
                print("Invalid phone number. Please enter digits only (with optional country code).")
                continue
            
            # Check length (10-15 digits including country code)
            digit_count = len(re.sub(r'[^\d]', '', clean_input))
            if digit_count < 10 or digit_count > 15:
                print("Invalid phone number length. Please enter 10-15 digits.")
                continue
            
            return user_input
            
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            return None

def demonstration_program():
    """Main demonstration program showing all validation functions"""
    
    print("=== User Input Validator Demonstration ===")
    print("This program demonstrates robust input validation with error handling.\n")
    
    # Age validation (as per the example)
    print("1. Age Validation:")
    age = validate_integer_range("Enter your age (1-120): ", 1, 120)
    if age is not None:
        print(f"You entered a valid age: {age}\n")
    
    # Name validation
    print("2. Name Validation:")
    name = validate_string_length("Enter your full name (2-50 characters): ", 2, 50)
    if name is not None:
        print(f"You entered a valid name: {name}\n")
    
    # Height validation
    print("3. Height Validation:")
    height = validate_float_range("Enter your height in meters (0.5-3.0): ", 0.5, 3.0)
    if height is not None:
        print(f"You entered a valid height: {height:.2f} meters\n")
    
    # Email validation
    print("4. Email Validation:")
    email = validate_email("Enter your email address: ")
    if email is not None:
        print(f"You entered a valid email: {email}\n")
    
    # Choice validation
    print("5. Choice Validation:")
    gender = validate_choice("Enter your gender (Male/Female/Other): ", ["Male", "Female", "Other"])
    if gender is not None:
        print(f"You selected: {gender}\n")
    
    # Phone validation
    print("6. Phone Number Validation:")
    phone = validate_phone_number("Enter your phone number: ")
    if phone is not None:
        print(f"You entered a valid phone number: {phone}\n")
    
    # Summary
    if all(value is not None for value in [age, name, height, email, gender, phone]):
        print("=== Validation Summary ===")
        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Height: {height:.2f} meters")
        print(f"Email: {email}")
        print(f"Gender: {gender}")
        print(f"Phone: {phone}")
        print("\nAll inputs validated successfully! ✅")

def interactive_validator():
    """Interactive validator for specific validation types"""
    
    print("\n=== Interactive Validator ===")
    
    validation_types = {
        "1": ("Integer Range", lambda: validate_integer_range("Enter an integer (1-100): ", 1, 100)),
        "2": ("Float Range", lambda: validate_float_range("Enter a decimal (0.0-10.0): ", 0.0, 10.0)),
        "3": ("String Length", lambda: validate_string_length("Enter text (5-20 chars): ", 5, 20)),
        "4": ("Email Format", lambda: validate_email("Enter email: ")),
        "5": ("Choice Selection", lambda: validate_choice("Choose color (Red/Blue/Green): ", ["Red", "Blue", "Green"])),
        "6": ("Phone Number", lambda: validate_phone_number("Enter phone: "))
    }
    
    while True:
        print("\nSelect validation type:")
        for key, (name, _) in validation_types.items():
            print(f"{key}. {name}")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "7":
            print("Thank you for using the validator!")
            break
        
        if choice in validation_types:
            name, validator_func = validation_types[choice]
            print(f"\n--- {name} Validation ---")
            result = validator_func()
            if result is not None:
                print(f"✅ Valid input: {result}")
        else:
            print("Invalid choice! Please select 1-7.")

def main():
    """Main function to run the input validator program"""
    
    while True:
        print("\n" + "="*50)
        print("🔍 USER INPUT VALIDATOR 🔍")
        print("="*50)
        print("1. Run Full Demonstration")
        print("2. Interactive Validator")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            demonstration_program()
        elif choice == "2":
            interactive_validator()
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
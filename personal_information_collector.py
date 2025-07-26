# Personal Information Collector
# This program asks the user for their personal information and displays a formatted summary

def main():
    """Main function to collect user information and display formatted summary"""
    
    # Collect user information
    print("=== Personal Information Collector ===")
    print()
    
    name = input("Enter your full name: ")
    age = input("Enter your age: ")
    city = input("Enter your city: ")
    hobby = input("Enter your hobby: ")
    
    # Display formatted summary
    print()
    print("=== Your Information Summary ===")
    print(f"Hello, {name}!")
    print(f"You are {age} years old and live in {city}.")
    print(f"In your free time, you enjoy {hobby}.")

if __name__ == "__main__":
    main()
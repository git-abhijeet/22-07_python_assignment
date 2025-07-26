
def main():
    """Main function to collect user information and display formatted summary"""
    
    print("=== Personal Information Collector ===")
    print()
    
    name = input("Enter your full name: ")
    age = input("Enter your age: ")
    city = input("Enter your city: ")
    hobby = input("Enter your hobby: ")
    
    print()
    print("=== Your Information Summary ===")
    print(f"Hello, {name}!")
    print(f"You are {age} years old and live in {city}.")
    print(f"In your free time, you enjoy {hobby}.")

if __name__ == "__main__":
    main()
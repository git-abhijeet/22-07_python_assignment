# Temperature Conversion Functions
# This program provides functions to convert between Celsius, Fahrenheit, and Kelvin

def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit
    Formula: F = (C × 9/5) + 32
    """
    return (celsius * 9/5) + 32

def celsius_to_kelvin(celsius):
    """
    Convert Celsius to Kelvin
    Formula: K = C + 273.15
    """
    return celsius + 273.15

def fahrenheit_to_celsius(fahrenheit):
    """
    Convert Fahrenheit to Celsius
    Formula: C = (F - 32) × 5/9
    """
    return (fahrenheit - 32) * 5/9

def fahrenheit_to_kelvin(fahrenheit):
    """
    Convert Fahrenheit to Kelvin
    Formula: K = (F - 32) × 5/9 + 273.15
    """
    celsius = fahrenheit_to_celsius(fahrenheit)
    return celsius_to_kelvin(celsius)

def kelvin_to_celsius(kelvin):
    """
    Convert Kelvin to Celsius
    Formula: C = K - 273.15
    """
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    """
    Convert Kelvin to Fahrenheit
    Formula: F = (K - 273.15) × 9/5 + 32
    """
    celsius = kelvin_to_celsius(kelvin)
    return celsius_to_fahrenheit(celsius)

def main():
    """Main function to demonstrate all temperature conversion functions"""
    
    print("=== Temperature Conversion Functions ===")
    print()
    
    # Example conversions as specified in the problem
    print("Sample Function Calls:")
    print(f"celsius_to_fahrenheit(0) = {celsius_to_fahrenheit(0)}")
    print(f"fahrenheit_to_kelvin(32) = {fahrenheit_to_kelvin(32)}")
    print(f"kelvin_to_celsius(300) = {kelvin_to_celsius(300)}")
    print()
    
    print("Formatted Output:")
    print(f"0°C = {celsius_to_fahrenheit(0)}°F")
    print(f"32°F = {fahrenheit_to_kelvin(32)}K")
    print(f"300K = {kelvin_to_celsius(300)}°C")
    print()
    
    # Additional demonstrations
    print("=== Additional Conversion Examples ===")
    
    # Common temperature conversions
    temps_celsius = [0, 25, 100, -40]
    temps_fahrenheit = [32, 68, 212, -40]
    temps_kelvin = [273.15, 298.15, 373.15, 233.15]
    
    print("\nCelsius to other units:")
    for temp in temps_celsius:
        f_temp = celsius_to_fahrenheit(temp)
        k_temp = celsius_to_kelvin(temp)
        print(f"{temp}°C = {f_temp:.1f}°F = {k_temp:.2f}K")
    
    print("\nFahrenheit to other units:")
    for temp in temps_fahrenheit:
        c_temp = fahrenheit_to_celsius(temp)
        k_temp = fahrenheit_to_kelvin(temp)
        print(f"{temp}°F = {c_temp:.1f}°C = {k_temp:.2f}K")
    
    print("\nKelvin to other units:")
    for temp in temps_kelvin:
        c_temp = kelvin_to_celsius(temp)
        f_temp = kelvin_to_fahrenheit(temp)
        print(f"{temp}K = {c_temp:.1f}°C = {f_temp:.1f}°F")

def interactive_converter():
    """Interactive temperature converter for user input"""
    
    print("\n=== Interactive Temperature Converter ===")
    
    while True:
        print("\nConversion Options:")
        print("1. Celsius to Fahrenheit")
        print("2. Celsius to Kelvin")
        print("3. Fahrenheit to Celsius")
        print("4. Fahrenheit to Kelvin")
        print("5. Kelvin to Celsius")
        print("6. Kelvin to Fahrenheit")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '7':
            print("Thank you for using the temperature converter!")
            break
        
        if choice not in ['1', '2', '3', '4', '5', '6']:
            print("Invalid choice! Please enter a number between 1-7.")
            continue
        
        try:
            temp = float(input("Enter the temperature value: "))
            
            if choice == '1':
                result = celsius_to_fahrenheit(temp)
                print(f"{temp}°C = {result:.2f}°F")
            elif choice == '2':
                result = celsius_to_kelvin(temp)
                print(f"{temp}°C = {result:.2f}K")
            elif choice == '3':
                result = fahrenheit_to_celsius(temp)
                print(f"{temp}°F = {result:.2f}°C")
            elif choice == '4':
                result = fahrenheit_to_kelvin(temp)
                print(f"{temp}°F = {result:.2f}K")
            elif choice == '5':
                result = kelvin_to_celsius(temp)
                print(f"{temp}K = {result:.2f}°C")
            elif choice == '6':
                result = kelvin_to_fahrenheit(temp)
                print(f"{temp}K = {result:.2f}°F")
                
        except ValueError:
            print("Invalid input! Please enter a valid number.")

if __name__ == "__main__":
    # Run the main demonstration
    main()
    
    # Ask if user wants to try interactive converter
    try_interactive = input("\nWould you like to try the interactive converter? (y/n): ")
    if try_interactive.lower() in ['y', 'yes']:
        interactive_converter()

library_inventory = []

def add_book():
    """Function to add a new book to the library inventory"""
    print("\n=== Add New Book ===")
    
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    
    if not title or not author:
        print("Error: Both title and author are required!")
        return
    
    for book in library_inventory:
        if book['title'].lower() == title.lower() and book['author'].lower() == author.lower():
            print(f"Book '{title}' by {author} already exists in the inventory!")
            return
    
    book = {
        'title': title,
        'author': author
    }
    library_inventory.append(book)
    print(f"Book '{title}' by {author} has been added successfully!")

def search_book():
    """Function to search for a book in the library inventory"""
    print("\n=== Search Book ===")
    
    if not library_inventory:
        print("No books in the inventory to search!")
        return
    
    search_term = input("Enter book title or author name to search: ").strip().lower()
    
    if not search_term:
        print("Error: Please enter a search term!")
        return
    
    found_books = []
    
    for book in library_inventory:
        if (search_term in book['title'].lower() or 
            search_term in book['author'].lower()):
            found_books.append(book)
    
    if found_books:
        print(f"\nFound {len(found_books)} book(s):")
        for book in found_books:
            print(f"- Book: {book['title']} | Author: {book['author']}")
    else:
        print(f"No books found matching '{search_term}'")

def display_inventory():
    """Function to display all books in the library inventory"""
    print("\n=== Library Inventory ===")
    
    if not library_inventory:
        print("No books in the inventory!")
        return
    
    print(f"Total books: {len(library_inventory)}")
    print("\nInventory:")
    for book in library_inventory:
        print(f"- Book: {book['title']} | Author: {book['author']}")

def remove_book():
    """Function to remove a book from the library inventory"""
    print("\n=== Remove Book ===")
    
    if not library_inventory:
        print("No books in the inventory to remove!")
        return
    
    title = input("Enter book title to remove: ").strip()
    author = input("Enter author name: ").strip()
    
    if not title or not author:
        print("Error: Both title and author are required!")
        return
    
    for i, book in enumerate(library_inventory):
        if book['title'].lower() == title.lower() and book['author'].lower() == author.lower():
            removed_book = library_inventory.pop(i)
            print(f"Book '{removed_book['title']}' by {removed_book['author']} has been removed!")
            return
    
    print(f"Book '{title}' by {author} not found in the inventory!")

def display_menu():
    """Function to display the main menu options"""
    print("\n" + "="*40)
    print("📚 LIBRARY MANAGEMENT SYSTEM 📚")
    print("="*40)
    print("1. Add Book")
    print("2. Search Book")
    print("3. Display Inventory")
    print("4. Remove Book")
    print("5. Exit")
    print("="*40)

def get_user_choice():
    """Function to get and validate user's menu choice"""
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("Invalid choice! Please enter a number between 1-5.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            return '5'
        except:
            print("Invalid input! Please enter a number between 1-5.")

def initialize_sample_data():
    """Function to add some sample books for demonstration"""
    sample_books = [
        {'title': 'Atomic Habits', 'author': 'James Clear'},
        {'title': 'Clean Code', 'author': 'Robert C. Martin'},
        {'title': 'The Pragmatic Programmer', 'author': 'David Thomas'},
        {'title': 'Python Crash Course', 'author': 'Eric Matthes'}
    ]
    
    response = input("Would you like to load sample books? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        library_inventory.extend(sample_books)
        print(f"Loaded {len(sample_books)} sample books into the inventory!")

def main():
    """Main function to run the library management system"""
    print("Welcome to the Library Management System!")
    
    initialize_sample_data()
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            search_book()
        elif choice == '3':
            display_inventory()
        elif choice == '4':
            remove_book()
        elif choice == '5':
            print("\nThank you for using the Library Management System!")
            print("Goodbye! 👋")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
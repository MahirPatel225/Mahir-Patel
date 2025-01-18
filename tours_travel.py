import mysql.connector

# Database Connection
mycon = mysql.connector.connect(host='localhost', user='root', password='80492', database='travel_management')
mycur = mycon.cursor()

# Admin Menu
def admin_menu():
    print("\n-- Admin Menu --\n")
    print("1. View Packages")
    print("2. Add Package")
    print("3. Edit Package")
    print("4. Delete Package")
    print("5. View Bookings")
    print("6. Add Booking")
    print("7. Delete Booking")
    print("8. Edit Booking")
    print("9. View Feedback for Package")
    print("10. Log Out")
    choice = input("Enter your choice: ")

    if choice == "1":
        view_package()
    elif choice == "2":
        add_package()
    elif choice == "3":
        edit_package()
    elif choice == "4":
        delete_package()
    elif choice == "5":
        view_booking()
    elif choice == "6":
        add_booking()
    elif choice == "7":
        delete_booking()
    elif choice == "8":
        edit_booking()
    elif choice == "9":
        view_feedback_for_package()
    elif choice == "10":
        main_menu()
    else:
        print("Invalid choice! Please try again.")
        admin_menu()

# Customer Menu
def customer_menu():
    print("\n-- Customer Menu --\n")
    print("1. View Packages")
    print("2. Provide Feedback on Trip")
    print("3. View Feedback for Package")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        view_package()
    elif choice == "2":
        provide_feedback()
    elif choice == "3":
        view_feedback_for_package()
    elif choice == "4":
        print("Thank you for using the system. Goodbye!")
    else:
        print("Invalid choice! Please try again.")
        customer_menu()

# Add Package
def add_package():
    print("\n-- Add Package --\n")
    name = input("Enter Package Name: ")
    description = input("Enter Package Description: ")
    price = float(input("Enter Package Price: "))
    duration = int(input("Enter Package Duration (in days): "))
    location = input("Enter Package Location: ")

    mycur.execute("INSERT INTO packages (name, description, price, duration, location) VALUES (%s, %s, %s, %s, %s)",
                  (name, description, price, duration, location))
    mycon.commit()
    print("Package added successfully!")
    
    input("\nPress Enter to return to Admin Menu...")
    admin_menu()

# Edit Package
def edit_package():
    print("\n-- Edit Package --\n")
    package_id = int(input("Enter Package ID to edit: "))
    name = input("Enter new Package Name: ")
    description = input("Enter new Package Description: ")
    price = float(input("Enter new Package Price: "))
    duration = int(input("Enter new Package Duration (in days): "))
    location = input("Enter new Package Location: ")

    mycur.execute("""
        UPDATE packages
        SET name = %s, description = %s, price = %s, duration = %s, location = %s
        WHERE id = %s
    """, (name, description, price, duration, location, package_id))
    mycon.commit()
    print("Package updated successfully!")
    
    input("\nPress Enter to return to Admin Menu...")
    admin_menu()

# Delete Package
def delete_package():
    print("\n-- Delete Package --\n")
    package_id = int(input("Enter Package ID to delete: "))
    
    mycur.execute("DELETE FROM packages WHERE id = %s", (package_id,))
    mycon.commit()
    print("Package deleted successfully!")
    
    input("\nPress Enter to return to Admin Menu...")
    admin_menu()

# View Tour Packages
def view_package():
    print("\n-- View Tour Packages --\n")
    mycur.execute("SELECT * FROM packages")
    packages = mycur.fetchall()

    if not packages:
        print("No packages available.\n")
    else:
        for package in packages:
            print(f"Package ID: {package[0]}")
            print(f"Name: {package[1]}")
            print(f"Description: {package[2]}")
            print(f"Price: {package[3]}")
            print(f"Duration: {package[4]} days")
            print(f"Location: {package[5]}")
            print("-" * 30)

    input("\nPress Enter to return to the previous menu...")
    admin_menu()

# View Bookings (Admin)
def view_booking():
    print("\n-- View Bookings --\n")
    
    mycur.execute("""
        SELECT b.id, b.package_id, b.customer_name, b.contact_info, b.booking_date, p.description
        FROM bookings b
        JOIN packages p ON b.package_id = p.id
    """)
    bookings = mycur.fetchall()

    if not bookings:
        print("No bookings found.\n")
    else:
        for booking in bookings:
            print(f"Booking ID: {booking[0]}")
            print(f"Package ID: {booking[1]}")
            print(f"Package Description: {booking[5]}") 
            print(f"Customer Name: {booking[2]}")
            print(f"Contact Info: {booking[3]}")
            print(f"Booking Date: {booking[4]}")
            print("-" * 30)

    input("\nPress Enter to return to the Admin Menu...")
    admin_menu()

# Add Booking
def add_booking():
    print("\n-- Add Booking --\n")
    package_id = int(input("Enter Package ID for booking: "))
    customer_name = input("Enter Customer Name: ")
    contact_info = input("Enter Customer Contact Info: ")
    booking_date = input("Enter Booking Date (YYYY-MM-DD): ")

    if package_id and customer_name and contact_info and booking_date:
        mycur.execute("""
            INSERT INTO bookings (package_id, customer_name, contact_info, booking_date)
            VALUES (%s, %s, %s, %s)
        """, (package_id, customer_name, contact_info, booking_date))
        mycon.commit()
        print("Booking added successfully!")
    else:
        print("Please provide all details.")
    
    input("\nPress Enter to return to Admin Menu...")
    admin_menu()

# Edit Booking
def edit_booking():
    print("\n-- Edit Booking --\n")
    booking_id = int(input("Enter Booking ID to edit: "))
    package_id = int(input("Enter new Package ID: "))
    customer_name = input("Enter new Customer Name: ")
    contact_info = input("Enter new Contact Info: ")
    booking_date = input("Enter new Booking Date (YYYY-MM-DD): ")

    if package_id and customer_name and contact_info and booking_date:
        mycur.execute("""
            UPDATE bookings
            SET package_id = %s, customer_name = %s, contact_info = %s, booking_date = %s
            WHERE id = %s
        """, (package_id, customer_name, contact_info, booking_date, booking_id))
        mycon.commit()
        print("Booking updated successfully!")
    else:
        print("Please provide all details.")
    
    input("\nPress Enter to return to Admin Menu...")
    admin_menu()

# Delete Booking
def delete_booking():
    print("\n-- Delete Booking --\n")
    booking_id = int(input("Enter Booking ID to delete: "))
    
    mycur.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    mycon.commit()
    print("Booking deleted successfully!")
    
    input("\nPress Enter to return to Admin Menu...")
    admin_menu()

# Provide Feedback (Customer)
def provide_feedback():
    print("\n-- Provide Feedback --\n")
    package_id = int(input("Enter Package ID to provide feedback: "))
    feedback = input("Enter your feedback: ")

    if package_id and feedback:
        mycur.execute("INSERT INTO feedback (package_id, feedback) VALUES (%s, %s)", (package_id, feedback))
        mycon.commit()
        print("Feedback submitted successfully!")
    else:
        print("Please provide all details.")
    
    input("\nPress Enter to return to the Customer Menu...")
    customer_menu()

# View Feedback for Package (Admin & Customer)
def view_feedback_for_package():
    print("\n-- View Feedback for Package --\n")
    package_id = int(input("Enter Package ID to view feedback: "))

    mycur.execute("SELECT * FROM feedback WHERE package_id = %s", (package_id,))
    feedback = mycur.fetchall()

    if not feedback:
        print("No feedback available for this package.\n")
    else:
        for item in feedback:
            print(f"Feedback ID: {item[0]}")
            print(f"Package ID: {item[1]}")
            print(f"Feedback: {item[2]}")
            print("-" * 30)

    input("\nPress Enter to return to the previous menu...")
    admin_menu()

# Admin Login
def admin_login():
    print("\n-- Admin Login --\n")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    mycur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = mycur.fetchone()

    if user:
        print("\nLogin successful! Redirecting to Admin Menu...")
        admin_menu()
    else:
        print("Invalid username or password! Please try again.")
        main_menu()

# Main Menu
def main_menu():
    while True:
        print("\n-- Tours and Travel Management System --\n")
        print("1. Admin")
        print("2. Customer Menu")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            # admin_login()
            admin_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

# Start the Program
main_menu()

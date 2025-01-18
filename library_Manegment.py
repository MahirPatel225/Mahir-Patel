import mysql.connector

mycon = mysql.connector.connect(host='localhost', user='root', password='80492', database='library')
mycur = mycon.cursor()

def input_int(prompt):
    value = input(prompt)
    while not value.isdigit():
        print("Invalid input. Please enter a valid number.")
        value = input(prompt)
    return int(value)

def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    qty = input_int("Enter Quantity: ")
    # inseart
    mycur.execute("INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)", (title, author, qty))
    mycon.commit()
    print("Book added successfully!")

def update_book():
    book_id = input_int("Enter Book ID to update: ")
    title = input("Enter New Title: ")
    for book in mycur.fetchall():
        if book_id not in book():
            print("Give valid ID")
            book_mang()
    author = input("Enter New Author: ")
    qty = input_int("Enter New Quantity: ")
    # update
    mycur.execute("UPDATE books SET title = %s, author = %s, quantity = %s WHERE id = %s", (title, author, qty, book_id))
    mycon.commit()
    print("Book updated successfully!")

def delete_book():
    book_id = input_int("Enter Book ID to delete: ")
    # delete
    mycur.execute("DELETE FROM books WHERE id = %s", (book_id,))
    mycon.commit()
    print("Book deleted successfully!")

def display_books():
    # select all
    mycur.execute("SELECT * FROM books")
    for book in mycur.fetchall():
        print(book)

def add_mem():
    name = input("Enter Member Name: ")
    email = input("Enter Email: ")
    mycur.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
    mycon.commit()
    print("Member added successfully!")

def update_mem():
    mem_id = input_int("Enter Member ID to update: ")
    name = input("Enter New Name: ")
    email = input("Enter New Email: ")
    mycur.execute("UPDATE members SET name = %s, email = %s WHERE id = %s", (name, email, mem_id))
    mycon.commit()
    print("Member updated successfully!")

def delete_mem():
    mem_id = input_int("Enter Member ID to delete: ")
    mycur.execute("DELETE FROM members WHERE id = %s", (mem_id))
    mycon.commit()
    print("Member deleted successfully!")

def display_members():
    mycur.execute("SELECT * FROM members")
    for member in mycur.fetchall():
        print(member)

def issue_book():
    # issue book
    book_id = input_int("Enter Book ID to issue: ")
    mem_id = input_int("Enter Member ID: ")
    mycur.execute("SELECT quantity FROM books WHERE id = %s", (book_id,))
    qty = mycur.fetchone()
    if qty and qty[0] > 0:
        # math
        mycur.execute("INSERT INTO issued_books (book_id, member_id) VALUES (%s, %s)", (book_id, mem_id))
        mycur.execute("UPDATE books SET quantity = quantity - 1 WHERE id = %s", (book_id,))
        mycon.commit()
        print("Book issued successfully!")
    else:
        print("Book not available")

def return_book():
    # return book
    issue_id = input_int("Enter Issue ID to return: ")
    mycur.execute("SELECT book_id FROM issued_books WHERE id = %s", (issue_id,))
    book_id = mycur.fetchone()
    if book_id:
        mycur.execute("DELETE FROM issued_books WHERE id = %s", (issue_id,))
        mycur.execute("UPDATE books SET quantity = quantity + 1 WHERE id = %s", (book_id[0],))
        mycon.commit()
        print("Book returned successfully!")
    else:
        print("Invalid Issue ID.")

def book_mang():
    while True:
        print("\n1. Add Book\n2. Update Book\n3. Delete Book\n4. Display All Books\n5. Exit")
        ch = input_int("Enter your choice: ")
        if ch == 1:
            add_book()
        elif ch == 2:
            update_book()
        elif ch == 3:
            delete_book()
        elif ch == 4:
            display_books()
        elif ch == 5:
            break

def member_mang():
    while True:
        print("\n1. Add Member\n2. Update Member\n3. Delete Member\n4. Display All Members\n5. Exit")
        ch = input_int("Enter your choice: ")
        if ch == 1:
            add_mem()
        elif ch == 2:
            update_mem()
        elif ch == 3:
            delete_mem()
        elif ch == 4:
            display_members()
        elif ch == 5:
            break

def issue_return():
    while True:
        print("\n1. Issue Book\n2. Return Book\n3. Exit")
        ch = input_int("Enter your choice: ")
        if ch == 1:
            issue_book()
        elif ch == 2:
            return_book()
        elif ch == 3:
            break

def lib_menu():
    while True:
        print("\t\t\tWelcome to Library Management System\n")
        print("1. Book Management\n2. Member Management\n3. Issue/Return Book\n4. Exit")
        ch = input_int("Enter your choice: ")
        if ch == 1:
            book_mang()
        elif ch == 2:
            member_mang()
        elif ch == 3:
            issue_return()
        elif ch == 4:
            print("Bye! Meet you next time!")
            break

lib_menu()

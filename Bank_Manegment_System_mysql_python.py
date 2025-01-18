import mysql.connector

# Database connection
mycon = mysql.connector.connect(host='localhost', user='root', password='80492', database='bank')
mycur = mycon.cursor()

def Admin():
    admin_id = input("Type your ID: ")
    admin_pass = input("Type Your Password: ")
    if admin_id == "Admin@login" and admin_pass == "Admin@123":
        print("\n\t\t\tADMIN MENU")
        print("1. Print All User Data")
        print("2. Print One User Data")
        print("3. Update User Data")
        print("4. Delete User Data")
        print("5. Exit")
        while True:
            a = int(input("Enter your choice: "))
            if a == 1:
                All_Data()
            elif a == 2:
                One_User_Data()
            elif a == 3:
                update()
            elif a == 4:
                delete()
            elif a == 5:
                break
            else:
                print("Invalid choice! Try again.")
    else:
        print("Invalid Admin credentials.")

def All_Data():
    mycur.execute("SELECT * FROM customer")
    data = mycur.fetchall()
    if data:
        for row in data:
            print(row)
    else:
        print("No user data found.")

def One_User_Data():
    user_id = input("Enter the User ID: ")
    mycur.execute("SELECT * FROM customer WHERE cust_id = %s", (user_id,))
    data = mycur.fetchone()
    if data:
        print(data)
    else:
        print("User not found.")

def delete():
    user_id = input("Enter the User ID to delete: ")
    mycur.execute("DELETE FROM customer WHERE cust_id = %s", (user_id,))
    mycon.commit()
    print("User data deleted successfully.")

def update():
    user_id = input("Enter the User ID to update: ")
    mycur.execute("SELECT * FROM customer WHERE cust_id = %s", (user_id,))
    data = mycur.fetchone()
    if data:
        print("1. Update Name")
        print("2. Update Password")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            new_name = input("Enter new name: ")
            mycur.execute("UPDATE customer SET cust_name = %s WHERE cust_id = %s", (new_name, user_id))
        elif choice == 2:
            new_pass = input("Enter new password: ")
            mycur.execute("UPDATE customer SET cust_pass = %s WHERE cust_id = %s", (new_pass, user_id))
        else:
            print("Invalid choice!")
        mycon.commit()
        print("User data updated successfully.")
    else:
        print("User not found.")

def User():
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    u = int(input("Enter your choice: "))
    if u == 1:
        login()
    elif u == 2:
        register()
    elif u == 3:
        print("Exiting User menu.")
    else:
        print("Invalid choice! Try again.")

def login():
    user_id = input("Type Your ID: ")
    user_pass = input("Type Your Password: ")
    mycur.execute("SELECT * FROM customer WHERE cust_id = %s AND cust_pass = %s", (user_id, user_pass))
    user = mycur.fetchone()
    if user:
        print("Login Success!")
        print("1. Check Balance")
        print("2. Withdraw Money")
        print("3. Deposit Money")
        print("4. Exit")
        while True:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                print("Your balance is:", user[2])  # Assuming balance is the 3rd column
            elif choice == 2:
                withdraw(user[3])  # Assuming cust_id is the 4th column
            elif choice == 3:
                deposit(user[3])  # Assuming cust_id is the 4th column
            elif choice == 4:
                break
            else:
                print("Invalid choice! Try again.")
    else:
        print("Invalid credentials!")

def register():
    cust_id = input("Enter Customer ID: ")
    cust_name = input("Enter Customer Name: ")
    cust_pass = input("Enter Your Password: ")
    balance = float(input("Enter Initial Balance: "))
    mycur.execute("INSERT INTO customer (cust_id, cust_name, cust_pass, balance) VALUES (%s, %s, %s, %s)",(cust_id, cust_name, cust_pass, balance))
    mycon.commit()
    print("\nAccount Registered Successfully!!!\n\n\n")
    login()

def withdraw(user_id):
    amount = float(input("Enter amount to withdraw: "))
    mycur.execute("SELECT balance FROM customer WHERE cust_id = %s", (user_id,))
    balance = mycur.fetchone()[0]
    if balance >= amount:
        new_balance = balance - amount
        mycur.execute("UPDATE customer SET balance = %s WHERE cust_id = %s", (new_balance, user_id))
        mycon.commit()
        print("Withdrawal successful! New balance:", new_balance)
    else:
        print("Insufficient funds.")
    
def deposit(user_id):
    amount = float(input("Enter amount to deposit: "))
    mycur.execute("SELECT balance FROM customer WHERE cust_id = %s", (user_id,))
    balance = mycur.fetchone()[0]
    new_balance = balance + amount
    mycur.execute("UPDATE customer SET balance = %s WHERE cust_id = %s", (new_balance, user_id))
    mycon.commit()
    print("Deposit successful! New balance:", new_balance)

def Bank():
    while True:
        print("\n--- Welcome to Bank Management System ---")
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        f = int(input("Enter your choice: "))
        if f == 1:
            Admin()
        elif f == 2:
            User()
        elif f == 3:
            print("Exiting the system.")
            break
        else:
            print("Invalid choice! Try again.")

Bank()

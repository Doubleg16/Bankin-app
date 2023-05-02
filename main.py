import sqlite3
from datetime import datetime

conn = sqlite3.connect('bank.db')
c = conn.cursor()



def login():
    while True:
        name = input("Enter your name: ")
        pin = input("Enter your 4-digit PIN: ")

        # check if user exists in database
        c.execute("SELECT * FROM accounts WHERE name = ? AND pin = ?", (name, pin))
        account = c.fetchone()

        if account:
            print(f"Welcome back, {name}!")
            return account
        else:
            print("Incorrect name or PIN. Please try again.\n")

def create_account():
    print("\nLet's create a new account.")

    while True:
        name = input("Enter your name: ")
        pin = input("Enter a 4-digit PIN: ")
        dob = input("Enter your date of birth (YYYY-MM-DD): ")

        # check if account already exists
        c.execute("SELECT * FROM accounts WHERE name = ?", (name,))
        account = c.fetchone()

        if account:
            print("An account with that name already exists. Please try again.\n")
        elif len(pin) != 4 or not pin.isnumeric():
            print("PIN must be a 4-digit number. Please try again.\n")
        elif not datetime.strptime(dob, '%Y-%m-%d'):
            print("Invalid date format. Please enter a valid date in the format YYYY-MM-DD.\n")
        else:
            c.execute("INSERT INTO accounts (name, pin, dob, balance) VALUES (?, ?, ?, ?)", (name, pin, dob, 0.0))
            conn.commit()
            print(f"\nAccount created successfully, {name}! Please login to continue.")
            return login()

def deposit(account):
    amount = input("Enter amount to deposit: ")

    if not amount.isnumeric():
        print("Invalid input. Amount must be a number.")
    elif float(amount) <= 0:
        print("Invalid input. Amount must be greater than zero.")
    else:
        balance = account[4] + float(amount)
        c.execute("UPDATE accounts SET balance = ? WHERE id = ?", (balance, account[0]))
        conn.commit()
        print(f"${amount} has been deposited into your account. Your new balance is ${balance:.2f}.\n")

def withdraw(account):
    amount = input("Enter amount to withdraw: ")

    if not amount.isnumeric():
        print("Invalid input. Amount must be a number.")
    elif float(amount) <= 0:
        print("Invalid input. Amount must be greater than zero.")
    elif float(amount) > account[4]:
        print("Insufficient funds.")
    else:
        balance = account[4] - float(amount)
        c.execute("UPDATE accounts SET balance = ? WHERE id = ?", (balance, account[0]))
        conn.commit()
        print(f"${amount} has been withdrawn from your account. Your new balance is ${balance:.2f}.\n")

def check_balance(account):
    print(f"Your current balance is ${account[4]:.2f}.\n")

# main program
print("Welcome to the bank!")

while True:
    print("1. Login\n2. Create account\n3. Quit")
    choice = input("What would you like to do? ")

    if choice == "1":
        account = login

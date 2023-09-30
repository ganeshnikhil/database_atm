# database_atm

**README.md**

## Overview

This is a Python program for managing bank accounts. It allows users to create new accounts, deposit and withdraw money, transfer money between accounts, and check account balances. The program also includes a transaction log for each account.

## Requirements

* Python 3.6 or higher
* Fernet
* Sqlite3
* PrettyTable

## Installation

To install the required dependencies, you can use the following command:

```
pip install -r requirements.txt
```

## Usage

To run the program, simply execute the following command:

```
python atm.py
```

This will display a menu of options for users to choose from.

## Options

The following options are available:

* **Check account:** Check the balance of an account.
* **Deposit account:** Deposit money into an account.
* **Delete account:** Delete an account.
* **Withdraw account:** Withdraw money from an account.
* **Create account:** Create a new account.
* **Transaction account:** Transfer money from one account to another.

## Example

The following example shows how to use the program to create a new account, deposit money into the account, and then withdraw money from the account:

```
python atm.py

[1.] Check account: check the balance of an account
[2.] Deposit account: deposit money into an account
[3.] Delete account: delete an account
[4.] Withdraw account: withdraw money from an account
[5.] Create account: create a new account
[6.] Transaction account: transfer money from one account to another

[*] Enter your option: 5

Enter your name: John Doe
Enter initial amount: 100

[+] Your username is: John Doe
[+] Your Account ID is: 123

[1.] Check account: check the balance of an account
[2.] Deposit account: deposit money into an account
[3.] Delete account: delete an account
[4.] Withdraw account: withdraw money from an account
[5.] Create account: create a new account
[6.] Transaction account: transfer money from one account to another

[*] Enter your option: 2

Enter the amount: 50

[+] 123 deposited 50 to the account

[1.] Check account: check the balance of an account
[2.] Deposit account: deposit money into an account
[3.] Delete account: delete an account
[4.] Withdraw account: withdraw money from an account
[5.] Create account: create a new account
[6.] Transaction account: transfer money from one account to another

[*] Enter your option: 4

Enter the amount: 25

[+] 123 Withdraw 25 to the account

[1.] Check account: check the balance of an account
[2.] Deposit account: deposit money into an account
[3.] Delete account: delete an account
[4.] Withdraw account: withdraw money from an account
[5.] Create account: create a new account
[6.] Transaction account: transfer money from one account to another

[*] Enter your option: 1

ID: 123
NAME: John Doe
DATE AND TIME OF CREATION: 2023-09-30 19:46:07 PST
AMOUNT: 75

Type      | Date      | Time      | ID        | Amount
------- | -------- | -------- | -------- | --------
          | 2023-09-30 | 19:46:07 |           | 100
Deposit  | 2023-09-30 | 19:46:07 |           | 50
Withdraw | 2023-09-30 | 19:46:07 |           | 25

Would you like to continue? (y/n)
```

**Requirements.txt**

The following is a requirements.txt file for the program:

```
Fernet
Sqlite3
PrettyTable
```

To install the required dependencies, you can use the following command:

Sure, here is more information about the functions inside the `atm.py` code:

**`sql_file()`**

This function creates a new SQLite3 database file if it does not already exist. If the database file already exists, it opens it and returns a connection to the database.

**`load_data()`**

This function loads the data from a JSON file into a Python object. The JSON file is encrypted using Fernet, so the function decrypts the file before loading the data.

**`save_data()`**

This function saves the data from a Python object to a JSON file. The JSON file is encrypted using Fernet, so the function encrypts the file before saving it.

**`name_validater()`**

This function validates the user's name. It returns `True` if the name is valid and `False` if it is not.

**`create_account()`**

This function creates a new bank account for the user. It generates a unique account ID and a Fernet key for the account. It also creates a new JSON file for the account and saves the initial account balance to the file.

**`check_account()`**

This function checks the balance of the user's bank account. It retrieves the account data from the JSON file and displays the account balance to the user.

**`deposit_account()`**

This function deposits money into the user's bank account. It retrieves the account data from the JSON file, adds the deposit amount to the account balance, and saves the updated account data to the file.

**`withdraw_account()`**

This function withdraws money from the user's bank account. It retrieves the account data from the JSON file, subtracts the withdrawal amount from the account balance, and saves the updated account data to the file.

**`transaction_account()`**

This function transfers money from one bank account to another. It retrieves the account data for both accounts from the JSON files, transfers the specified amount from one account to the other, and saves the updated account data to both files.

**`delete_account()`**

This function deletes the user's bank account. It deletes the account data from the JSON file and the JSON file itself.

**`main()`**

This function is the main function of the program. It displays a menu of options to the user and allows them to choose an option. The function then calls the appropriate function to perform the selected operation.

I hope this additional information is helpful. Please let me know if you have any other questions.

from cryptography.fernet import Fernet as f
import sqlite3
import random 
from datetime import datetime
import json 
import os 
from prettytable import PrettyTable
import re 

#cur.execute("CREATE TABLE Bank(id, name , date , password)"
def sql_file(name='bank.db'):
   if not os.path.exists(name):
      con = sqlite3.connect(name)
      cur = con.cursor()
     
      cur.execute('''
      CREATE TABLE Bank (
         id INTEGER PRIMARY KEY,
         name TEXT,
         date TEXT, -- or INTEGER for timestamps
         password BLOB -- for binary encryption keys
      )
      ''')
      con.commit()
      return con
   else:
      con = sqlite3.connect(name)
      #cur = con.cursor()
      return con

## load the data of file and return it as json 
def load_data(path,key):
   with open(path, "rb") as info:
      data=info.read()
      content=f(key).decrypt(data).decode()
      return json.loads(content)

## write the json data in file as return nothing
def save_data(path,data,key):
   content = json.dumps(data)
   contents_encrypted=f(key).encrypt(content.encode())
   with open(path, "wb") as file:
      file.write(contents_encrypted)
   return 

def name_validater(name):
   name_pattern = r"^[A-Za-z\s'-]+$"
   return re.match(name_pattern, name) is not None

'''
create account . save his  id , name , date of creation , fernet key in sql db 
thne create file with the  name of his id then encrypt that data using fernet key 
store amount and transaction details in json format . saved in txt file 
'''
def create_account():
   con=sql_file()
   cur=con.cursor()
   cur.execute("SELECT id FROM Bank;")
   data = cur.fetchall()
   id_list = [result[0] for result in data]
   id_no = random.randint(100, 999)
   
   while str(id_no) in id_list:
      id_no = random.randint(100, 999)
      
   name = input("Enter your name: ")
   while not name_validater(name):
      print("[+] correctly enter your name")
      name = input("Enter your name: ")
   
   amount = abs(int(input("[=] Enter initial amount: ")))
   date=f"{datetime.now():%Y-%m-%d %I:%M:%S%p}"
   key=f.generate_key()
   

   account = {
      "total_money": amount,
      "transaction_date": []
   }
   save_data(F'{id_no}.txt',account,key)
   
   new_data = (id_no , name , date, key)
   cur.execute("INSERT INTO Bank (id, name, date, password) VALUES (?, ?, ?, ?);", new_data)
   
   print(f"[+] Your username is: {name}")
   print(f"[+] Your Account ID is: {id_no}")
   
   con.commit()
   con.close()

'''
take input as id_no then check is this id exist in sql db . if yes 
retrive the fernet key from the sql then open the file name as id_no.txt 
decrypt file using fernet key from sql then show the details using preety table 
'''
def check_account():
   con=sql_file()
   cur=con.cursor()
   id_no = int(input("Enter your ID: "))
   
   cur.execute("SELECT id FROM Bank;")
   data = cur.fetchall()
   id_list = [result[0] for result in data]

   if id_no not in id_list:
      print("[+] This account doesn't exist")
      con.commit()
      con.close()
      return
   
   cur.execute("SELECT * FROM Bank WHERE id = ?;", (id_no,))
   content = cur.fetchone()
   
   name=content[1]
   date=content[2]
   key=content[3]

   #account = data[id_no]
   print("\n")
   print(f"ID: {id_no}")
   print(f"NAME: {name}")
   print(f"DATE AND TIME OF CREATION: {date}")
   
   account=load_data(F'{id_no}.txt',key)
   
   print(f"AMOUNT: {account['total_money']}")

   table = PrettyTable()
   table.field_names = ["Type", "Date", "Time", "ID", "Amount"]
   table.align = "r"
   table.align["Type"] = "l"
   table.align["ID"] = "l"
   
   transaction_dates = account["transaction_date"]
   print("\n")
   if len(transaction_dates) != 0:
      for dtime in transaction_dates:
         data = dtime.split()
         if "W" in dtime:
            data[0] = "Withdraw"
         elif "T" in dtime:
            data[0] = "Transaction"
         elif "R" in dtime:
            data[0] = "Received"
         elif "D" in dtime:
            data[0] = "Deposit"
         table.add_row(data)
      print(table)
   else:
      print("[+] No withdrawals, transactions, or deposits have been made for this account.")
   con.commit()
   con.close()
   

'''
take id_no as input and then check thid id_no exist in sql db 
retrive the fernet key of given id then open id_no.txt file then 
add the money in the previous amount then again encrypt that json 
and save the file in id_no.txt
'''
def deposit_account():
   con=sql_file()
   cur=con.cursor()
   id_no = int(input("Enter your ID: "))
   
   cur.execute("SELECT id FROM Bank;")
   data = cur.fetchall()
   
   id_list = [result[0] for result in data]
   if id_no not in id_list:
      print("[+] This account doesn't exist")
      con.commit()
      con.close()
      return
   
   cur.execute("SELECT password  FROM Bank WHERE id = ?;", (id_no,))
   content = cur.fetchone()
   key=content[0]
   
   account=load_data(F'{id_no}.txt',key)
   amount = abs(int(input("[=] Enter the amount: ")))
   account["total_money"] += amount
   account["transaction_date"].append(f"D {datetime.now():%Y-%m-%d %I:%M:%S%p} {None} {amount}")

   save_data(F'{id_no}.txt',account,key)
   print(f"[+] {id_no} deposited {amount} to the account")
   
   con.commit()
   con.close()
   

'''
take id_no as input and then check thid id_no exist in sql db 
retrive the fernet key of given id then open id_no.txt file then 
if you have enough amount then minus the money in the previous amount then again encrypt that json 
and save the file in id_no.txt
'''
def withdraw_account():
   con=sql_file()
   cur=con.cursor()
   id_no = int(input("Enter your ID: "))
   
   cur.execute("SELECT id FROM Bank;")
   data = cur.fetchall()
   
   id_list = [result[0] for result in data]
   if id_no not in id_list:
      print("[+] This account doesn't exist")
      con.commit()
      con.close()
      return
   
   cur.execute("SELECT password  FROM Bank WHERE id = ?;", (id_no,))
   content = cur.fetchone()
   key=content[0]

   account=load_data(F'{id_no}.txt',key)
   amount = abs(int(input("[=] Enter the amount: ")))
   
   account_amount=account["total_money"]
   if account_amount >= amount:
      account["total_money"] -= amount
      account["transaction_date"].append(f"W {datetime.now():%Y-%m-%d %I:%M:%S%p} {None} {amount}")
      save_data(F'{id_no}.txt',account,key)
      print(f"[+] {id_no} Withdraw {amount} to the account")
   else:
      print("[+] Not enough amount in account...")
   con.commit()
   con.close()
   
   


def transaction_account():
   con=sql_file()
   cur=con.cursor()
   
   tran_id = int(input("Enter your ID: "))
   recv_id = int(input("Enter receiver ID: "))
   
   cur.execute("SELECT id FROM Bank;")
   data = cur.fetchall()
   
   id_list = [result[0] for result in data]
   print(id_list)
   if tran_id not in id_list or recv_id not in id_list:
      print("[+] One or both of the accounts don't exist")
      con.commit()
      con.close()
      return

   #amount = int(input("Enter the amount of transaction: "))
   cur.execute("SELECT password  FROM Bank WHERE id = ?;", (tran_id,))
   content = cur.fetchone()
   tran_key=content[0]

   tran_account=load_data(F'{tran_id}.txt',tran_key)
   amount = abs(int(input("[=] Enter the amount: ")))
   
   account_amount=tran_account["total_money"]
   
   if account_amount >= amount:
      cur.execute("SELECT password  FROM Bank WHERE id = ?;", (recv_id,))
      recv_content = cur.fetchone()
      recv_key=recv_content[0]
      recv_account=load_data(F'{recv_id}.txt',recv_key)
      
      tran_account["total_money"] -= amount
      tran_account["transaction_date"].append(f"T {datetime.now():%Y-%m-%d %I:%M:%S%p} {recv_id} {amount}")
      
      recv_account["total_money"]+=amount
      recv_account["transaction_date"].append(f"R {datetime.now():%Y-%m-%d %I:%M:%S%p} {tran_id} {amount}")
      
      save_data(F'{tran_id}.txt',tran_account,tran_key)
      save_data(F'{recv_id}.txt',recv_account,recv_key)
      
      print(f"[-] {tran_id} transacted {amount} to {recv_id} from the ATM")
   else:
      print("[+] Not enough money in account....")
   con.commit()
   con.close()



def delete_account():
   con=sql_file()
   cur=con.cursor()
   id_no = int(input("Enter your ID: "))
   
   cur.execute("SELECT id FROM Bank;")
   data = cur.fetchall()
   
   id_list = [result[0] for result in data]
   
   if id_no not in id_list:
      print("[+] This account doesn't exist")
      con.commit()
      con.close()
      return
   
   cur.execute("DELETE FROM Bank WHERE id = ?;",(id_no,))
   con.commit()
   con.close()
   
   file_path=f"{id_no}.txt"
   try:
      os.remove(file_path)
      print(f"File '{file_path}' has been deleted successfully.")
      
   except OSError as e:
      print(f"Error deleting file: {e}")

   print(f"[+] {id_no} has been deleted from the ATM")


def main():
   
   print('''
   [1.] Check account: check the balance of an account
   [2.] Deposit account: deposit money into an account
   [3.] Delete account: delete an account
   [4.] Withdraw account: withdraw money from an account
   [5.] Create account: create a new account
   [6.] Transaction account: transfer money from one account to another
    ''')

   user = int(input('[*] Enter your option: '))

   if user == 1:
      check_account()
   elif user == 2:
      deposit_account()
   elif user == 3:
      delete_account()
   elif user == 4:
      withdraw_account()
   elif user == 5:
      create_account()
   elif user == 6:
      transaction_account()
   else:
      print("[-] Invalid option.")


if __name__ == "__main__":
   main()

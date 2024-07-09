#a Simple Bank Account Class 

class BankAccount:
    def __init__(self, balance=0):
        self.account_balance = balance
    
    def deposit(self, amount):
        balance = self.account_balance
        if amount != 0:
            balance += amount
       # print(f"Deposited: ${amount}")

    def withdraw(self, amount):
        balance = self.account_balance
        if balance >= amount and balance != 0:
            self.account_balance -= amount
          #  print(f"Withdrew: ${amount}")
            return True    
        else:
           # print('Insufficient funds.')
            return False   
        
    def display_balance(self):
        return print(f"Current Balance: ${float(self.account_balance)}")
    
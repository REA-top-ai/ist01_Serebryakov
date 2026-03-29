from abc import ABC, abstractmethod

class BankAccountInterface(ABC):
    @abstractmethod
    def set_add_balance(self, amount):
        pass

class BankAccount:
    def __init__(self, name):
        self.__name = name
        self.__balance = 0

    def set_add_balance(self, amount):
        self.__balance += amount
        print(f'{self.__name} add {amount}, Now balance is {self.__balance}')

    def get_balance(self):
        print(f'{self.__name} balance is {self.__balance}')
        return self.__balance

    def payment(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            print(f'{self.__name} pay {amount}, Now balance is {self.__balance}')
        else:
            print(f'Not enough,  balance: {self.__balance}')

class Client:
    def __init__(self, name):
        self.__name = name
        self.__accounts = []
    
    def create_account(self):
        new_account = BankAccount(self.__name)
        self.__accounts.append(new_account)
        return new_account

class DepositBankAccount(BankAccount):
    def __init__(self, name, interest_rate):
        super().__init__(name)
        self.__interest_rate = interest_rate

    def add_interest(self):
        interest = self.get_balance() * self.__interest_rate
        self.set_add_balance(interest)
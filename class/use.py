from OOP import BankAccount
def main():
    client_1 = BankAccount('Alice')
    client_2 = BankAccount('Bob')

    client_1.set_add_balance(400)
    client_2.set_add_balance(200)
    print(client_1.get_balance())
    client_2.payment(400)

main()
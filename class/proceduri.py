def add_money(amount, client, balance):
    balance += amount
    print(f'{client} add {amount}, Now balance is {balance}')
    return balance

def payment(amount, client, balance):
    if balance >= amount:
        balance -= amount
        print(f'{client} pay {amount}, Now balance is {balance}')
    else:
        print(f'Not enough,  balance: {balance}')
    return balance

if __name__ == '__main__':
    client_1 = 'Alice'
    client_1_balance = 1000

    client_2 = 'Bob'
    client_2_balance = 500

    client_1_balance = add_money(400, client_1, client_1_balance)
    client_2_balance = add_money(200, client_2, client_2_balance)
    client_2_balance = payment(400, client_2, client_2_balance)



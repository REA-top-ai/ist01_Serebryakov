client_1 = 'Alice'
client_1_balance = 1000

client_2 = 'Bob'
client_2_balance = 500

amount = 200
client_1_balance += amount
print(f'{client_1} add {amount}, Now balance is {client_1_balance}')

amount = 400
client_2_balance += amount
print(f'{client_2} add {amount}, Now balance is {client_2_balance}')

amount = 200
if client_1_balance >= amount:
    client_1_balance += amount
    print(f'{client_1} add {amount}, Now balance is {client_1_balance}')
else:
    print(f'Not enough,  balance: {client_1_balance}')


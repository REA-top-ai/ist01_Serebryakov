first_name = input()
last_name = input()

def account_generator(first_name, last_name):
    new_account = first_name[:3] + last_name[:3]
    return new_account
def password_generator(first_name, last_name):
    new_password = first_name[-3:] + last_name[-3:]
    return new_password

print(account_generator(first_name, last_name), password_generator(first_name, last_name))


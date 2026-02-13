def check_user(user_name):
    if user_name == "Дмитрий":
        return "Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!"
    else:
        return "Добро пожаловать"

print(check_user("Дмитрий"))
print(check_user("Ангелина"))

def NAME_ARM(user_name, arm):
    allowed_arms = {"Дмитрий": 1,
                    "Ангелина": 2,
                    "Василий": 3,
                    "Екатерина": 4}
    if user_name in allowed_arms and allowed_arms[user_name] == arm:
        return "Добро пожаловать!"
    else:
        if user_name == "Дмитрий":
            return "Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!"
        else:
            return "Логин или пароль не верный, попробуйте еще раз"

print(NAME_ARM("Дмитрий", 1))
print(NAME_ARM("Дмитрий", 2))
print(NAME_ARM("Ангелина", 2))
print(NAME_ARM("Ангелина", 1))
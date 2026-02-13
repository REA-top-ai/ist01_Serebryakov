#1
statement_one = (2 + 2 + 2 >= 6) and (-1 * -1 < 0)
statement_two = (4 * 2 <= 8) and (7 - 1 == 6)
print(statement_one, statement_two)
#2
user_name = input("name")
ARM = int(input("num"))
Dmitriy_check = "Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!"
welcome = "Добро пожаловать!"
if user_name == "Дмитрий" and ARM != 1:
    print(Dmitriy_check)
if user_name == "Дмитрий" and ARM == 1:
    print(welcome)
if user_name == "Ангелина" and ARM == 2:
    print(welcome)
if user_name == "Василий" and ARM == 3:
    print(welcome)
if user_name == "Екатерина" and ARM == 4:
    print(welcome)
if user_name == "Ангелина" and ARM != 2:
    print("Логин или пароль неверный, попробуйте еще раз")
if user_name == "Василий" and ARM != 3:
    print("Логин или пароль неверный, попробуйте еще раз")
if user_name == "Екатерина" and ARM != 4:
    print("Логин или пароль неверный, попробуйте еще раз")

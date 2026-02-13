user_name = input("name")
ARM = int(input("num"))
Dmitriy_check = "Дмитрий, твое рабочее место находится в другой комнате. Отойди от чужого компьютера и займись работой!"
welcome = "Добро пожаловать!"
if user_name == "Дмитрий" and ARM != 1:
    print(Dmitriy_check)
if user_name == "Дмитрий" and ARM == 1 or user_name == "Ангелина" and ARM == 2 or user_name == "Василий" and ARM == 3 or user_name == "Екатерина" and ARM == 4:
    print(welcome)
if user_name == "Ангелина" and ARM != 2 or user_name == "Василий" and ARM != 3 or user_name == "Екатерина" and ARM != 4:
    print("Логин или пароль неверный, попробуйте еще раз")

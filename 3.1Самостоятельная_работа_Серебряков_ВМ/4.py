age = int(input("Введите возраст "))
drive_expirience = int(input("Введите опыт вождения "))
car = str(input("Какая у вас машина? "))
reputation = "1"

jams = "3"
duration = "30"

first_age = [20, 21, 22, 23, 24, 25, 26, 27]
second_age = [28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
exp_first = [2, 3, 4, 5, 6, 7, 8, 9]
exp_second = [10, 11, 12, 13, 14, 15]

p_price = 0
b_price = 0

if age in first_age:
    if drive_expirience in exp_first:
        if reputation in "12":
            if jams in "123":
                p_price = 8 * int(duration)
                b_price = 12 * int(duration)
            elif jams in "4567":
                p_price = 8.5 * int(duration)
                b_price = 12.5 * int(duration)
        elif reputation in "345":
            if jams in "123":
                p_price = 7.5 * int(duration)
                b_price = 11.6 * int(duration)
            elif jams in "4567":
                p_price = 7.4 * int(duration)
                b_price = 11.3 * int(duration)
if age in second_age:
    if drive_expirience in exp_first:
        if reputation in "12":
            if jams in "123":
                p_price = 7.2 * int(duration)
                b_price = 11.4 * int(duration)
            elif jams in "4567":
                p_price = 7.2 * int(duration)
                b_price = 11.9 * int(duration)
        elif reputation in "345":
            if jams in "123":
                p_price = 0
                b_price = 0
            elif jams in "4567":
                p_price = 7.2 * int(duration)
                b_price = 11.9 * int(duration)
    elif reputation in exp_second:
        if reputation in "12":
            if jams in "123":
                p_price = 6.9 * int(duration)
                b_price = 10.8 * int(duration)
            elif jams in "4567":
                p_price = 6.7 * int(duration)
                b_price = 11 * int(duration)
        elif reputation in "345":
            if jams in "123":
                p_price = 0
                b_price = 0
            elif jams in "4567":
                p_price = 6.6 * int(duration)
                b_price = 10.9 * int(duration)

if car == "фольц даз авто":
    print("Стоимость за поездку: ", p_price)
elif car == "биэмви":
    print("Стоимость за поездку: ", b_price)

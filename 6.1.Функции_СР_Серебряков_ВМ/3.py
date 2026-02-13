time = input("когда?")
clothes = "домашняя одежда"
meal = "хлопья"
print("У меня большой гардероб")
def cloth(time, clothes):
    return f"{time} лучше всего подходит {clothes}"

def eda(time, meal):
    return f"{time} мои предпочтения в еде {meal}"
print(cloth(time, clothes), eda(time, meal))
import random 
name = input()
question = input("вопрос, на которой можно ответить только да или нет «Да» или «Нет»")
answer = ""
random_number = random.randint(1, 9)

if random_number == 1:
    answer = "Да, безусловно"
elif random_number == 2:
    answer = "Совершенно верно"
elif random_number == 3:
    answer = "Без сомнения"
elif random_number == 4:
    answer = "Ответ туманный, попробуйте еще раз"
elif random_number == 5:
    answer = "Спросите еще раз позже"
elif random_number == 6:
    answer = "Лучше не говорить вам сейчас"
elif random_number == 7:
    answer = "Мои источники говорят «нет»"
elif random_number == 8:
    answer = "Прогноз не очень хороший"
elif random_number == 9:
    answer = "Очень сомнительно"
else:
    answer = "Ошибка"
print(name + " спрашивает: " + question)


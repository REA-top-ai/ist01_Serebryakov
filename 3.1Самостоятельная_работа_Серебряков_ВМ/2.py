l = list(map(int, input().split()))
maxi = l[0]
avg = l[1]
mini = l[2]
st = l[3]
if (maxi - avg) > 3*st or (avg - mini) > 3*st:
    print("В ваших данных имеются выбросы и требуют предобработки")
elif (maxi - avg) > 5*st or (avg - mini) > 5*st:
    print("В ваших данных имеются экстремальные значения и требуют предобработки")
else:
    print("Ваши данные пригодны для анализа")
    
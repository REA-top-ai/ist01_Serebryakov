import random

adm_number = random.randint(1,9)

def sum_numbers(num):
    num= str(num)
    return sum(map(int, list(num)))
def lott(n):
    ww = []
    for i in n:
        if sum_numbers(i) % adm_number == 0:
            ww.append(i)
            if len(ww) == 5:
                break
    return ww
print(adm_number)
print(*lott(list(range(100))))

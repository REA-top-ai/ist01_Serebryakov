def rec(num):
    if num in (0, 1): 
        return 1
    return num * rec(num - 1)
def bez_rec(num):
    if num  in (0, 1): 
        return 1
    res = 1
    for i in range(2, num + 1):
        res *= i
    return res
def pw2(l):
    return list(num**2 for num in l)
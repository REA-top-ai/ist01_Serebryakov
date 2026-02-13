import random
n=int(input())
alph = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
passw = ""
for i in range(n):
    x = random.randint(0, len(alph)-1)
    passw+=alph[x]
print(passw)
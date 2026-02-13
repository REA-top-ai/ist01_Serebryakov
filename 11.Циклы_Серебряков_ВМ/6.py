single_digits=list(range(0, 10))
squares=[]
cubes=[]
for single in single_digits:
    squares.append(single**2)
    cubes.append(single**3)
    print(single)
print(squares)
print(cubes)

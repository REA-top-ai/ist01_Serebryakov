def ggrade(grade):
    if grade >= 4.0:
        return "A"
    elif grade >= 3.0:
        return "B"
    elif grade >= 2.0:
        return "C"
    elif grade >= 1.0:
        return "D"
    else:
        return "F"
grade = float(input())
print(ggrade(grade))
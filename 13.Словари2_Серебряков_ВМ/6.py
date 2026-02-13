total_exercises = 0
num_exercises = {"functions": 10, "syntax": 13, "control flow": 15, "loops": 22, "lists": 19, "classes": 18, "dictionaries": 18}
for val in num_exercises.values():
    total_exercises += val
print(total_exercises)
#ФОКУС
print(sum(num_exercises.values()))
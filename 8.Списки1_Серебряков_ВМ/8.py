first_names=["Эйнсли","Бен","Чани","Депак"]
age=[]
age.append(42)
all_ages=[32, 41, 29]+ age
name_and_age=list(zip(first_names, all_ages))
print(name_and_age)
ids=list(range(4))
print(ids)
name_age_ids=list(zip(first_names, all_ages, ids,))
print(name_age_ids)
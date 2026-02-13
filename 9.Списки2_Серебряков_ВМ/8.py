inventory = ["двухспальная кровать", "двухспальная кровать", "изголовье", "двуспальная кровать",
"двуспальная кровать", "комод", "комод", "стол", "стол", "тумбочка", "тумбочка", "королевский кровать", "двуспальная кровать", "две односпальные кровати", "две односпальные кровати",
"простыни", "простыни", "подушка", "подушка"]
inventory_len=len(inventory)
print(inventory)
first=inventory[0]
last=inventory[-1]
inventory_2_6=inventory[2:6]
first_3=inventory[0:3]
twin_beds=inventory.count("две односпальные кровати") *2
inventory.sort()
print(first)
print(last)
print(twin_beds)
print(inventory_2_6)
print(first_3)
print(inventory)
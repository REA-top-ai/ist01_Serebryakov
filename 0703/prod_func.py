tables1 = { 
    1: ["Jiho", False], 
    2: [], 
    3: [], 
    4: [], 
    5: [], 
    6: [], 
    7: [], 
} 
"""def assign_table(table_num, name, vip_status=False):
    tables[table_num].append(name)
    tables[table_num].append(vip_status)
    return tables"""
def assign_table1(table_num, name, *order, vip_status=False, ):
    keys = ["name", "vip_status"]
    tables1[table_num] = {key: value for key, value in zip(keys, [name,  vip_status])}
    return tables1

assign_table1(6, "Yohi", vip_status=False)
assign_table1(4, "Karla")
print(tables1)
"""def print_order(*order_items):
    print(order_items)

print_order('Orange Juice','Apple Juice', 'Scrambled Eggs','Pancakes')
"""

tables = {
1: {
"name": "Jiho",
"vip_status": False,
"order": ("Orange Juice","Apple Juice")
},
2: {},
3: {},
4: {},
5: {},
6: {},
7: {},
}

def assign_table(table_num, name, *order, vip_status=False, ):
    keys = ["name", "vip_status"]
    tables[table_num] = {key: value for key, value in zip(keys, [name,  vip_status])}
    return tables

def assign_and_print_order(table_num, *order_items):
    if "order" not in tables[table_num]:
        tables[table_num]["order"] = ()
    if not tables[table_num]["order"]:
        tables[table_num]["order"] = order_items
    for i in tables[table_num]["order"]:
        print(i)

assign_table(2, "Arwa", vip_status=True)
assign_and_print_order(2, "Стейк"," Морской окунь", "Бутылка вина")
print(tables)

tables2 = { 
    1: { 
        'name': 'Chioma', 
        'vip_status': False, 
        'order': { 
            'drinks': 'Orange Juice, Apple Juice', 
            'food_items': 'Pancakes' 
        } 
        }, 
        2: {}, 
        3: {}, 
        4: {}, 
        5: {}, 
        6: {}, 
        7: {}, 
} 
def assign_food_items(table_num, **order_items):
    if "order" not in tables2[table_num]:
        tables2[table_num]["order"] = {}
    
    food = order_items.get("food")
    drinks = order_items.get("drinks")
    
    if food:
        tables2[table_num]["order"]["food"] = food
    if drinks:
        tables2[table_num]["order"]["drinks"] = drinks
assign_food_items(3, food="Pancakes, Poached Egg", drinks="Water")
print(tables2)

def calculate_price_per_person(total, tip, split): 
    total_tip = total * (tip/100) 
    split_price = (total + total_tip) / split 
    print(split_price) 
               
table_7_total = [534.5, 20, 5]

calculate_price_per_person(*table_7_total)


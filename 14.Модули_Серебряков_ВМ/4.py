from datetime import datetime

employees = {
    "Иванов Иван Иванович": {
        "должность": "Менеджер",
        "дата_приема": "22.10.2013",
        "зарплата": 250000
    },
    "Сорокина Екатерина Матвеевна": {
        "должность": "Аналитик",
        "дата_приема": "12.03.2020",
        "зарплата": 75000
    },
    "Струков Иван Сергеевич": {
        "должность": "Старший программист",
        "дата_приема": "23.04.2012",
        "зарплата": 150000
    },
    "Корнеева Анна Игоревна": {
        "должность": "Ведущий программист",
        "дата_приема": "22.02.2015",
        "зарплата": 120000
    },
    "Старчиков Сергей Анатольевич": {
        "должность": "Младший программист",
        "дата_приема": "12.11.2021",
        "зарплата": 50000
    },
    "Бутенко Артем Андреевич": {
        "должность": "Архитектор",
        "дата_приема": "12.02.2010",
        "зарплата": 200000
    },
    "Савченко Алина Сергеевна": {
        "должность": "Старший аналитик",
        "дата_приема": "13.04.2016",
        "зарплата": 100000
    }
}

def bonus1(employees):
    bonus = {}
    """ впринципе можно и без проверки на дату
    if "09-13" in str(datetime.today()):
        for name in employees.items():
            if "программист" in name[1]["должность"]:
                bonus[name[0]] = name[1]["зарплата"]*0.03
            else:
                bonus[name[0]] = 0
        return bonus
    else:
        return 0"""
    for name in employees.items():
        if "программист" in name[1]["должность"]:
            bonus[name[0]] = name[1]["зарплата"]*0.03
        else:
            bonus[name[0]] = 0
    return bonus
    
print(bonus1(employees))
print("########")

def bonus2(employees):
    bonus = {}
    for name in employees.items():
        bonus[name[0]]=2000
    return bonus
print(bonus2(employees))
print("#########")

def bonus3(employees):
    current_date = list(map(int, str(datetime.today())[:11].split("-")))
    indexation_dict = {}
    for name in employees.items():
        hire_date = list(map(int, str(datetime.strptime(name[1]["дата_приема"],"%d.%m.%Y"))[:11].split("-")))
        if (current_date[0] -hire_date[0]  == 10 and hire_date[1] < current_date[1] and hire_date[2] < current_date[2]) or (current_date[0] - hire_date[0] >= 11):
            indexation_percent = 0.07
        else:
            indexation_percent = 0.05
        name[1]["зарплата"] = name[1]["зарплата"] * indexation_percent + name[1]["зарплата"]
        
    return employees
print(bonus3(employees))
print("#######")

#попробовали через костыль своими руками без подсказок из файла, можно и по-человечески
def vacation(employees):
    eligible_employees = []
    current_date = datetime.now()
    
    for employee in employees:
        hire_date = datetime.strptime(employee["Дата найма"], '%d.%m.%Y')
        days_worked = (current_date - hire_date).days 
        
        if days_worked > 6 * 30:
            eligible_employees.append(employee["ФИО"])
    
    return eligible_employees
print(vacation(employees))




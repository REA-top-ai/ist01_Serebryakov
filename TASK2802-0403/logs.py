import json
import os


def check(ls):
    a = []
    for i in ls:
        if i:
            a.append(i)
    return a
def check_name():
    s = 0
    filename = "logs"
    while True:
        check = filename+str(s)
        if os.path.exists(f'{check}.json'):
            s+=1
        else:
            return filename+str(s)
def in_int(val):
    try:
        val = int(val)
        return val
    except ValueError:
        return val
def filter_logs(log, level=None, status=None, user=None, action=None):
    ls = [level, status, user, action]
    lss = check(ls)
    s = 0
    #тут условие как фильтр в экселя на разные параметры, то есть ищет пересечение, а не объединение
    for log in parsed_logs:
        if level and log["level"] == level:
            s+=1
        if action and log["action"] == action:
            s+=1
        if status and log["status"] == status:
            s+=1
        if user and log["user"] == user:
            s+=1
        if s == len(lss):
            print(log)
def amount(log, level=None, status=None, user=None, action=None):
    s = 0
    for log in parsed_logs:
        if level and log["level"] == level:
            s+=1
        if action and log["action"] == action:
            s+=1
        if status and log["status"] == status:
            s+=1
        if user and log["user"] == user:
            s+=1
    return s
logs = [
    "2025-02-01 10:15:33|INFO|user=anna action=login status=success ip=10.0.0.1",
    "2025-02-01 10:17:10|ERROR|user=bob action=payment status=fail amount=120",
    "2025-02-01 10:20:01|INFO|user=anna action=logout status=success",
    "2025-02-01 10:22:45|WARNING|user=anna action=payment status=fail amount=300",
    "2025-02-01 10:30:12|ERROR|user=tom action=login status=fail ip=10.0.0.5"
]
def edit(logs):
    parsed_logs = []
    for line in logs:
        parts = line.split("|")
        date = parts[0]
        level = parts[1]
        message = parts[2]

        fields = message.split(" ")
            
        data = {}

        for f in range(len(fields)):
            kv = fields[f].split("=")
            data[kv[0]] = in_int(kv[1])

        data["date"] = date
        data["level"] = level

        parsed_logs.append(data)
        return parsed_logs
if __name__ == '__main__':
    parsed_logs = []
    for line in logs:
        parts = line.split("|")
        date = parts[0]
        level = parts[1]
        message = parts[2]

        fields = message.split(" ")
            
        data = {}

        for f in range(len(fields)):
            kv = fields[f].split("=")
            data[kv[0]] = in_int(kv[1])

        data["date"] = date
        data["level"] = level

        parsed_logs.append(data)
    #parsed_logs = edit(logs)

    print(json.dumps(parsed_logs, indent=4))
    with open(f'{check_name()}.json', "w", encoding="utf-8") as f:
        json.dump(parsed_logs, f, indent=4)

    print("---- FAIL ONLY ----")
    filter_logs(parsed_logs, status="fail")

    print("---- ONLY ERRORS ----")
    filter_logs(parsed_logs, level="ERROR")

    print("---- ONLY anna ----")
    filter_logs(parsed_logs, user="anna", action="payment")
    

    print("---- COUNT BY LEVEL ----")
    print(amount(parsed_logs, level="INFO"), amount(parsed_logs, level="ERROR"), amount(parsed_logs, level="WARNING"))


class Employee:
    new_id = 1
    def __init__(self):
        self.id = Employee.new_id
        Employee.new_id += 1
    def say_id(self):
        print(f"My id is {self.id}")

e1 = Employee()
e2 = Employee()
e1.say_id()
e2.say_id()

"""class Admin(Employee):
    def say_id(self):
        print("I am an Admin")"""

class User:
    def __init__(self, id, role):
        self.id = id
        self.role = role
    def say_user_info(self):
        print(f"User id: {self.id}, role: {self.role}")
class Admin(Employee, User):
    def __init__(self):
        Employee.__init__(self)
        User.__init__(self, self.id, "Admin")
    def say_id(self):
        super().say_id()
        print("I am an Admin")

e3 = Admin()
e3.say_id()

class Manager(Admin):
    def say_id(self):
        super().say_id()
        print("I am in charge!")

e4 = Manager()
e4.say_id()



class Admin(Employee, User):
    def __init__(self):
        Employee.__init__(self)
        User.__init__(self, self.id, "Admin")
    
    def say_id(self):
        super().say_id()
        print("I am an Admin")

e3 = Admin()
e3.say_user_info()

class Manager(Admin):
    def say_id(self):
        super().say_id()
        print("I am in charge!")

meeting = [Employee(), Admin(), Manager()]
for dude in meeting:
    dude.say_id()

class Meeting:
    def __init__(self):
        self.attendees = []
    
    def __add__(self, employee):
        self.attendees.append(employee)
        return self
    
    def __len__(self):
        return len(self.attendees)
    
e1 = Employee()
e2 = Employee()
e3 = Employee()
m1 = Meeting()
m1 += e1
m1 += e2
m1 += e3
print(len(m1))

from abc import ABC, abstractmethod
class AbstractEmployee(ABC):
    new_id = 1
    
    def __init__(self):
        self.id = AbstractEmployee.new_id
        AbstractEmployee.new_id += 1
    
    @abstractmethod
    def say_id(self):
        pass

class Employee(AbstractEmployee):
    def say_id(self):
        print(f"My id is {self.id}")

e1 = Employee()
e1.say_id()

class Employee1:
    def __init__(self):
        self.id = 52
        self._id =67
        self.__id = 97

e43 = Employee1()
print(dir(e43))

class Employee2:
    def __init__(self):
        self._name = None
    
    def get_name(self):
        return self._name
    
    def set_name(self, new_name):
        self._name = new_name
    
    def del_name(self):
        del self._name

e63 = Employee2()
e63.set_name("John")
print(e63.get_name())
e63.del_name()
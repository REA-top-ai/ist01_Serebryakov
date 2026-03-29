class Person: 
    def __init__(self, name, age): 
        self.__name = name 
        self.__age = age 

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age
    
    def get_role_name(self):
        return f"Person with name {self.__name} and age {self.__age}"
    
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.__student_id = student_id
        self.__grades = []

    def add_grades(self, grade):
        if 0 <= grade <= 100:
            self.__grades.append(grade)
        else:
            raise ValueError("Grade must be between 0 and 100")

    def get_student_id(self):
        return self.__student_id
    
    def get_role_name(self):
        return f"Student with name {self.get_name()}, age {self.get_age()} and student ID {self.__student_id}"

    def avg_grade(self):
        if len(self.__grades) == 0:
            return 0
        return sum(self.__grades) / len(self.__grades)

    def get_role_name(self):
        return f"STUDENT with name {self.get_name()} and age {self.get_age()} and student ID {self.__student_id} and avg grade {self.avg_grade()}"

class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.__subject = subject
        self.salary = 0

    def set_salary(self, amount):
        if amount < 0:
            raise ValueError("Salary cannot be negative")
        self.salary = amount
    
    def get_subject(self):
        return self.__subject
    
    def get_role_name(self):
        return f"TEACHER with name {self.get_name()} and age {self.get_age()} and subject {self.__subject} and salary {self.salary}"

p1 = Person("Prepod", 30)
s1 = Student('sergey', 99, 12345)
t1 = Teacher("Ivan", 40, "Math")
print(p1.get_role_name())
print(s1.get_role_name())
print(t1.get_role_name())
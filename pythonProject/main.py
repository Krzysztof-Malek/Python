from Tools.i18n.makelocalealias import pprint


class Employee:

    def __init__(self, name, lastname, salary):
        self.name = name
        self.lastname = lastname
        self.salary = salary
        self.email = self.name + self.lastname + "@example.pl"

    def give_email(self, email):
        self.email = email

class Accountant(Employee):
    
    def __init__(self, name, lastname, salary, position, experience):
        super().__init__(name, lastname, salary)
        self.position = position
        self.experience = experience

    def add_experience(self, experience):
        self.experience += [experience]

employee1 = Employee("Jan", "Kowalski", 4700)
print(employee1.salary)

employeeAcc = Accountant("Zbigniew", "Nowy", 33333, "Main", ["1", "Dada", 23])
print(employeeAcc.experience)

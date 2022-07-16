from msilib.schema import Class


class Employee:
    salary = 0

    def __init__(self, yoe, level):
        self.level = level
        self.yoe = yoe
        self.calculateSalary()

    def calculateSalary(self):

        if self.yoe == 0:
            salary = 10000
            self.salary = salary
            return salary

        if self.yoe != 0:
            salary = (self.yoe * self.level) * 10000
            self.salary = salary
            return salary

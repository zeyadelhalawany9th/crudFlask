class Employee:

    salary = 0
    level = 0
    yoe = 0

    def __init__(self, level, yoe):
        self.level = level
        self.yoe = yoe
        self.calculateSalary()

    def calculateSalary(self):

        salary = self.yoe * self.level * 10000
        self.salary = salary
        return salary

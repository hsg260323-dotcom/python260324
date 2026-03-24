# Person 클래스 정의
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

# Manager 클래스: Person 상속, title 추가
class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")

# Employee 클래스: Person 상속, skill 추가
class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")

# 테스트 코드
if __name__ == "__main__":
    # Person 테스트
    p1 = Person(1, "Alice")
    p1.printInfo()
    print()

    p2 = Person(2, "Bob")
    p2.printInfo()
    print()

    # Manager 테스트
    m1 = Manager(3, "Charlie", "Senior Manager")
    m1.printInfo()
    print()

    m2 = Manager(4, "Diana", "Project Manager")
    m2.printInfo()
    print()

    # Employee 테스트
    e1 = Employee(5, "Eve", "Python Programming")
    e1.printInfo()
    print()

    e2 = Employee(6, "Frank", "Data Analysis")
    e2.printInfo()
    print()

    e3 = Employee(7, "Grace", "Web Development")
    e3.printInfo()
    print()

    e4 = Employee(8, "Henry", "Machine Learning")
    e4.printInfo()
    print()

    e5 = Employee(9, "Ivy", "Database Management")
    e5.printInfo()
    print()

    e6 = Employee(10, "Jack", "UI/UX Design")
    e6.printInfo()
    print()
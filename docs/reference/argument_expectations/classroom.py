class Person:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


class Classroom:
    def __init__(self, people: list):
        self._people = people

    def enter_original(self, student):
        self._people.append(student)

    def enter_copy(self, student):
        self._people.append(Person(student.name))

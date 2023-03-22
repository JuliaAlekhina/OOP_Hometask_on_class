def calc_average_value(dictionary):
    average_value = 0
    list_of_grades = []
    for key in dictionary:
        list_of_grades.extend(dictionary[key])
    if len(list_of_grades) != 0:
        average_value += sum(list_of_grades)/len(list_of_grades)
    return average_value


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def average_grade(self):
        average_grade = calc_average_value(self.grades)
        return average_grade

    def rate_lecturer(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
           and (course in self.courses_in_progress or course in self.finished_courses)
           and course in lecturer.courses_attached
           and (0 <= grade <= 10)):

            if course in lecturer.students_reports:
                lecturer.students_reports[course] += [grade]
            else:
                lecturer.students_reports[course] = [grade]
        else:
            return 'Evaluation error'

    def __str__(self):
        res = f'Student \n' \
              f'Name: {self.name} \n' \
              f'Surname: {self.surname} \n' \
              f'Average homework grade: {round(self.average_grade(), 2)} \n' \
              f'Courses in progress: {", ".join(self.courses_in_progress)} \n' \
              f'Accomplished courses: {", ". join(self.finished_courses)}'
        return res

    def __ge__(self, other):
        if not isinstance(other, Student):
            print('Incorrect comparison!')
            return
        return self.average_grade() > other.average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.students_reports = {}

    def average_report(self):
        average_report = calc_average_value(self.students_reports)
        return average_report

    def __str__(self):
        res = f'Lecturer \n' \
              f'Name: {self.name} \n'\
              f'Surname: {self.surname} \n'\
              f'Average lecture report: {round(self.average_report(), 2)}'
        return res

    def __ge__(self, other):
        if not isinstance(other, Lecturer):
            print('Incorrect comparison!')
            return
        return self.average_report() > other.average_report()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Evaluation error'

    def __str__(self):
        res = f'Reviewer \n' \
              f'Name: {self.name} \n' \
              f'Surname: {self.surname}'
        return res


harry_potter = Student("Harry", "Potter", "Male")
harry_potter.courses_in_progress.extend(["Defence against the Dark Arts", "Potions", "History of Magic"])
ron_weasley = Student("Ron", "Weasley", "Male")
ron_weasley.courses_in_progress.extend(["Defence against the Dark Arts", "Herbology", "Charms"])
hermione_granger = Student("Hermione", "Granger", "Female")
hermione_granger.courses_in_progress.extend(["Defence against the Dark Arts", "Potions", "History of Magic",
                                             "Muggle Studies", "Studies of Ancient Runes"])
hermione_granger.finished_courses.extend(["Astronomy", "Transfigurations", "Care of Magical Creatures"])


severus_snape = Lecturer("Severus", "Snape")
severus_snape.courses_attached.extend(["Defence against the Dark Arts", "Potions"])
gideon_lockheart = Lecturer("Gideon", "Lockheart")
gideon_lockheart.courses_attached.extend(["Defence against the Dark Arts", "Charms"])

minerva_mcgonagall = Reviewer("Minerva", "McGonagall")
minerva_mcgonagall.courses_attached.extend(["History of Magic", "Muggle Studies", "Studies of Ancient Runes"])
albus_dumbledore = Reviewer("Albus", "Dumbledore")
albus_dumbledore.courses_attached.extend(["Defence against the Dark Arts", "Charms", "Potions", "Herbology"])

print("Initial state:")

print(harry_potter.__str__())
print(hermione_granger.__str__())
print(ron_weasley.__str__())
print(severus_snape.__str__())
print(gideon_lockheart.__str__())
print(minerva_mcgonagall.__str__())
print(albus_dumbledore.__str__())

print("_______________________________________________________________")

harry_potter.rate_lecturer(severus_snape, "Defence against the Dark Arts", 2)
ron_weasley.rate_lecturer(severus_snape, "Defence against the Dark Arts", 1)
harry_potter.rate_lecturer(gideon_lockheart, "Defence against the Dark Arts", 2)
ron_weasley.rate_lecturer(severus_snape, "Potions", 3)
hermione_granger.rate_lecturer(severus_snape, "Defence against the Dark Arts", 2)
# contain errors for check
hermione_granger.rate_lecturer(minerva_mcgonagall, "Transfiguration", 10)
hermione_granger.rate_lecturer(severus_snape, "Defence against the Dark Arts", -5)


albus_dumbledore.rate_hw(harry_potter, "Defence against the Dark Arts", 9)
albus_dumbledore.rate_hw(ron_weasley, "Defence against the Dark Arts", 7)
albus_dumbledore.rate_hw(hermione_granger, "Defence against the Dark Arts", 10)
albus_dumbledore.rate_hw(hermione_granger, "Potions", 10)
# contain errors for check
albus_dumbledore.rate_hw(harry_potter, "Herbology", 10)
albus_dumbledore.rate_hw(harry_potter, "History of Magic", 10)

minerva_mcgonagall.rate_hw(harry_potter, "History of Magic", 8)
minerva_mcgonagall.rate_hw(hermione_granger, "Muggle Studies", 10)
# contain errors for check
minerva_mcgonagall.rate_hw(harry_potter, "Muggle Studies", 7)
minerva_mcgonagall.rate_hw(ron_weasley, "Charms", 2)

print("After grading:")

print(harry_potter.__str__())
print(hermione_granger.__str__())
print(ron_weasley.__str__())
print(severus_snape.__str__())
print(gideon_lockheart.__str__())
print(minerva_mcgonagall.__str__())
print(albus_dumbledore.__str__())

print("____________________________________________________________________________")

print(f"Hermione Granger studies better than Ron Weasley: {hermione_granger.__ge__(ron_weasley)}")
print(f"Hermione Granger studies better than Harry Potter: {hermione_granger.__ge__(harry_potter)}")
print(f"Ron Weasley studies better than Harry Potter: {ron_weasley.__ge__(harry_potter)}")
print(f"Severus Snape studies better than Gideon Lockheart: {severus_snape.__ge__(gideon_lockheart)}")
# contain errors for check
print(f"Severus Snape studies better than Minerva Mcgonagall: {severus_snape.__ge__(minerva_mcgonagall)}")

print("______________________________________________________________________________")

list_of_students = [harry_potter, hermione_granger, ron_weasley]
course_for_students = "Herbology"


def average_grade_of_students_in_subject(students, subject):
    grades = []
    for student in students:
        if isinstance(student, Student) and subject in student.grades:
            grades.extend(student.grades[subject])
    if len(grades) != 0:
        average_student_grade = sum(grades)/len(grades)
    else:
        average_student_grade = 0
    return average_student_grade


print(f"Average grade of students in {course_for_students} "
      f"is {round(average_grade_of_students_in_subject(list_of_students, course_for_students), 2)}")

list_of_lecturers = [severus_snape, gideon_lockheart, minerva_mcgonagall]
course_for_lecturers = "Defence against the Dark Arts"


def average_report_of_lecturers_in_subject(lecturers, subject):
    reports = []
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and subject in lecturer.students_reports:
            reports.extend(lecturer.students_reports[subject])
    if len(reports) != 0:
        average_student_report = sum(reports)/len(reports)
    else:
        average_student_report = 0
    return average_student_report


print(f"Average report of lecturers in {course_for_lecturers} "
      f"is {round(average_report_of_lecturers_in_subject(list_of_lecturers, course_for_lecturers), 2)}")

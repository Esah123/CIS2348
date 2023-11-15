#############################################
#     Name: Esah Bukhari                    #
#     ID: 2083147                           #
#                                           #
#                                           #
#############################################
# Create a class called Object to house all the attributes of the Student
class Student:
    def __init__(self, student_id, last_name, first_name, major, gpa=None, graduation_date=None, disciplinary_action=False):
        self.student_id = student_id
        self.last_name = last_name
        self.first_name = first_name
        self.major = major
        self.gpa = gpa
        self.graduation_date = graduation_date
        self.disciplinary_action = disciplinary_action

# Read StudentMajors CSV file
def read_students_majors_list(file_path):
    students = {}
    with open(file_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
            # split each line by the , delimieter to get individual records
            parts = line.strip().split(',')
            student_id, last_name, first_name, major = parts[:4]
            disciplinary_action = len(parts) == 5
            students[student_id] = Student(student_id, last_name, first_name, major, disciplinary_action=disciplinary_action)
    return students
# Read GPAList CSV file
def read_gpa_list(file_path, students):
    with open(file_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
            # split each line by the , delimieter to get individual records
            student_id, gpa = line.strip().split(',')
            if student_id in students:
                students[student_id].gpa = float(gpa)
# Read GraduationDates CSV file
def read_graduation_dates_list(file_path, students):
    with open(file_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
            # split each line by the , delimieter to get individual records
            student_id, graduation_date = line.strip().split(',')
            # if the student id is in the STUDENT objects, then set the graduation date
            if student_id in students:
                students[student_id].graduation_date = graduation_date

# Generate the output FULLROSTER CSV file
def write_full_roster(students, file_path):
    sorted_students = sorted(students.values(), key=lambda s: s.last_name)
    with open(file_path, 'w') as file:
        file.write('Student ID,Major,First Name,Last Name,GPA,Graduation Date,Disciplinary Action\n')
        for student in sorted_students:
            line = f"{student.student_id},{student.major},{student.first_name},{student.last_name},{student.gpa},{student.graduation_date},{student.disciplinary_action}\n"
            file.write(line)
# Sort students by last name
def sort_students_by_lastname(student):
    return student.last_name
# Create full roster
def write_full_roster(students, file_path):
    sorted_students = sorted(students.values(), key=sort_students_by_lastname)
    with open(file_path, 'w') as file:
        file.write('Student ID,Major,First Name,Last Name,GPA,Graduation Date,Disciplinary Action\n')
        for student in sorted_students:
            line = f"{student.student_id},{student.major},{student.first_name},{student.last_name},{student.gpa},{student.graduation_date},{student.disciplinary_action}\n"
            file.write(line)
# Sort students by id
def sort_students_by_id(student):
    return student.student_id
# Writer major lists
def write_major_lists(students):
    majors = {}
    for student in students.values():
        major = student.major.replace(" ", "")
        if major not in majors:
            majors[major] = []
        majors[major].append(student)

    for major, students in majors.items():
        file_path = f"{major}Students.csv"
        with open(file_path, 'w') as file:
            file.write('Student ID,Last Name,First Name,Graduation Date,Disciplinary Action\n')
            for student in sorted(students, key=sort_students_by_id):
                line = f"{student.student_id},{student.last_name},{student.first_name},{student.graduation_date},{student.disciplinary_action}\n"
                file.write(line)
# Eligible for scholorship
def is_eligible_for_scholarship(student):
    return student.gpa and student.gpa > 3.8 and not student.disciplinary_action and not student.graduation_date
# Sort by GPA
def sort_by_gpa(student):
    return -student.gpa
# Write scholorship candidates
def write_scholarship_candidates(students, file_path):
    eligible_students = filter(is_eligible_for_scholarship, students.values())
    with open(file_path, 'w') as file:
        file.write('Student ID,Last Name,First Name,Major,GPA\n')
        for student in sorted(eligible_students, key=sort_by_gpa):
            line = f"{student.student_id},{student.last_name},{student.first_name},{student.major},{student.gpa}\n"
            file.write(line)
# Is disciplined
def is_disciplined(student):
    return student.disciplinary_action
# sort by graduation
def sort_by_graduation_date(student):
    return student.graduation_date
# Write disciplined students
def write_disciplined_students(students, file_path):
    disciplined_students = filter(is_disciplined, students.values())
    with open(file_path, 'w') as file:
        file.write('Student ID,Last Name,First Name,Graduation Date\n')
        for student in sorted(disciplined_students, key=sort_by_graduation_date):
            line = f"{student.student_id},{student.last_name},{student.first_name},{student.graduation_date}\n"
            file.write(line)

# Main function used to ENTER the program 
def main():
    students = read_students_majors_list('StudentsMajorsList.csv')
    read_gpa_list('GPAList.csv', students)
    read_graduation_dates_list('GraduationDatesList.csv', students)

    write_full_roster(students, 'FullRoster.csv')
    write_major_lists(students)
    write_scholarship_candidates(students, 'ScholarshipCandidates.csv')
    write_disciplined_students(students, 'DisciplinedStudents.csv')

if __name__ == "__main__":
    main()

#############################################
#     Name: Esah Bukhari                    #
#     ID: 2083147                           #
#                                           #
#                                           #
#############################################

import csv

def read_csv(file_name):
    """Reads a CSV file and returns a list of dictionaries."""
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def merge_data(students, gpas, graduation_dates):
    """Merges student, GPA, and graduation date data into a single dictionary."""
    merged_data = {}
    for student in students:
        student_id = student['StudentID']
        student_data = {
            'StudentID': student_id,
            'LastName': student['LastName'],
            'FirstName': student['FirstName'],
            'Major': student['Major'],
            'DisciplinaryAction': student.get('DisciplinaryAction', None)
        }

        # Add GPA to student data
        student_gpa = next((gpa['GPA'] for gpa in gpas if gpa['StudentID'] == student_id), None)
        student_data['GPA'] = student_gpa

        # Add graduation date
        student_grad_date = next((grad['GraduationDate'] for grad in graduation_dates if grad['StudentID'] == student_id), None)
        student_data['GraduationDate'] = student_grad_date

        merged_data[student_id] = student_data

    return merged_data

def find_closest_gpa_student(major, target_gpa, data):
    """Finds the student with the closest GPA to the target within the specified major."""
    closest_student = None
    smallest_diff = None
    for student_id, student in data.items():
        if student['Major'] == major and 'GraduationDate' not in student and 'DisciplinaryAction' not in student:
            gpa_diff = abs(float(student['GPA']) - float(target_gpa))
            if closest_student is None or gpa_diff < smallest_diff:
                closest_student = student
                smallest_diff = gpa_diff
    return closest_student

def query_data(data):
    """Handles querying the data based on user input."""
    while True:
        user_input = input("Enter a major and GPA, or 'q' to quit: ")
        if user_input.lower() == 'q':
            break

        # Splitting user input to get major and GPA
        try:
            major, gpa = user_input.rsplit(maxsplit=1)
            gpa = float(gpa)
        except ValueError:
            print("Invalid input. Please enter a major followed by a GPA.")
            continue

        # Finding students matching the criteria
        matching_students = [student for student_id, student in data.items() if student['Major'] == major 
                             and 'GraduationDate' not in student and 'DisciplinaryAction' not in student
                             and abs(float(student['GPA']) - gpa) <= 0.1]

        # Finding students within a broader range
        consider_students = [student for student_id, student in data.items() if student['Major'] == major 
                             and 'GraduationDate' not in student and 'DisciplinaryAction' not in student
                             and abs(float(student['GPA']) - gpa) <= 0.25 and student not in matching_students]

        if matching_students:
            print("Your student(s):")
            for student in matching_students:
                print(f"{student['StudentID']}, {student['FirstName']} {student['LastName']}, GPA: {student['GPA']}")

            if consider_students:
                print("You may, also, consider:")
                for student in consider_students:
                    print(f"{student['StudentID']}, {student['FirstName']} {student['LastName']}, GPA: {student['GPA']}")
        else:
            closest_student = find_closest_gpa_student(major, gpa, data)
            if closest_student:
                print("Closest GPA match:")
                print(f"{closest_student['StudentID']}, {closest_student['FirstName']} {closest_student['LastName']}, GPA: {closest_student['GPA']}")
            else:
                print("No such student")

def main():
    """Main function to run the program."""
    students = read_csv('StudentsMajorsList.csv')
    gpas = read_csv('GPAList.csv')
    graduation_dates = read_csv('GraduationDatesList.csv')

    merged_data = merge_data(students, gpas, graduation_dates)
    query_data(merged_data)

if __name__ == "__main__":
    main()

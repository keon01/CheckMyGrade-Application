import csv
import os
import pandas as pd
from statistics import mean, median
from encdyc import TextSecurity  # Encryption class

# Default file paths
STUDENT_FILE = "students.csv"
COURSE_FILE = "courses.csv"
PROFESSOR_FILE = "professors.csv"
LOGIN_FILE = "login.csv"

# Encryption handler
cipher = TextSecurity(4)  # Using Caesar cipher with shift of 4


class Base:
    """Base class for handling CSV file operations"""

    @staticmethod
    def initialize_csv(file, headers):
        """Creates a CSV file with headers if it doesn't exist or is empty"""
        if not os.path.exists(file) or os.stat(file).st_size == 0:
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

    @staticmethod
    def read_csv(file):
        """Reads data from a CSV file."""
        if not os.path.exists(file):
            return []
        with open(file, mode="r", newline="") as f:
            return list(csv.reader(f))

    @staticmethod
    def write_csv(file, data):
        """Writes data to a CSV file."""
        with open(file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    @classmethod
    def set_file_paths(cls, student_file, course_file, professor_file, login_file):
        """Allows test cases to override file paths"""
        global STUDENT_FILE, COURSE_FILE, PROFESSOR_FILE, LOGIN_FILE
        STUDENT_FILE, COURSE_FILE, PROFESSOR_FILE, LOGIN_FILE = student_file, course_file, professor_file, login_file


# Ensure all CSV files exist
Base.initialize_csv(STUDENT_FILE, ["email", "first_name", "last_name", "course_id", "professor_email", "grade", "marks"])
Base.initialize_csv(COURSE_FILE, ["course_id", "course_name", "description"])
Base.initialize_csv(PROFESSOR_FILE, ["email", "name", "rank", "course_id"])
Base.initialize_csv(LOGIN_FILE, ["email", "password", "role"])


class Student(Base):
    def __init__(self, email, first_name, last_name, course_id, professor_email, grade, marks):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.professor_email = professor_email
        self.grade = grade
        self.marks = int(marks)

    def save(self, silent=False):
        """Saves student data to students.csv but prevents duplicates"""
        students = self.read_csv(STUDENT_FILE)

        for row in students:
            if row and row[0] == self.email:
                if not silent:
                    print(f"Student {self.first_name} {self.last_name} already exists. Skipping save.")
                return  # Prevent duplicate student addition

        with open(STUDENT_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.email, self.first_name, self.last_name, self.course_id, self.professor_email, self.grade, str(self.marks)])

        if not silent:  # Only print if not in test mode
            print(f"Student {self.first_name} {self.last_name} added successfully.")




    @classmethod
    def search(cls, email):
        """Search for a student by email"""
        students = cls.read_csv(STUDENT_FILE)
        for row in students:
            if row and row[0] == email:
                return row
        return None

    @classmethod
    def delete_student(cls, email):
        """Delete a student by email"""
        students = cls.read_csv(STUDENT_FILE)
        new_students = [row for row in students if row and row[0] != email]
        cls.write_csv(STUDENT_FILE, new_students)
        print(f"Student {email} deleted successfully.")

    @classmethod
    def update_student(cls, email, new_course=None, new_grade=None, new_marks=None):
        """Update student record"""
        students = cls.read_csv(STUDENT_FILE)
        updated = False

        for row in students:
            if row and row[0] == email:
                if new_course: row[3] = new_course
                if new_grade: row[5] = new_grade
                if new_marks: row[6] = str(new_marks)
                updated = True

        if updated:
            cls.write_csv(STUDENT_FILE, students)
            print(f"Student {email} record updated successfully.")
        else:
            print(f"Student {email} not found.")

    @classmethod
    def sort_students(cls):
        """Sort students by marks"""
        students = cls.read_csv(STUDENT_FILE)
        if len(students) > 1:
            header = students[0]
            sorted_students = sorted(students[1:], key=lambda x: int(x[6]), reverse=True)
            students = [header] + sorted_students
        cls.write_csv(STUDENT_FILE, students)

    @classmethod
    def generate_grade_report(cls, file_path="students.csv", limit=10):
        """Generate a course-wise, professor-wise, and student-wise grade report with limited entries."""
        students = cls.read_csv(file_path)
        professors = Professor.read_csv("professors.csv")
        courses = Course.read_csv("courses.csv")

        if len(students) <= 1:
            print("\nNo student records available to generate reports.")
            return

        print("\n--- Course-Wise Report (First {} Records) ---".format(limit))
        course_wise = {}
        course_map = {row[0]: row[1] for row in courses[1:]}  # Map course_id to course_name
        for row in students[1:limit+1]:  # Limit number of records
            course_name = course_map.get(row[3], "Unknown Course")
            course_wise.setdefault(course_name, []).append(f"{row[1]} {row[2]}: {row[5]} ({row[6]})")
        for course, grades in course_wise.items():
            print(f"{course}: {', '.join(grades)}")

        print("\n--- Professor-Wise Report (First {} Records) ---".format(limit))
        professor_wise = {}
        professor_map = {row[0]: row[1] for row in professors[1:]}  # Map professor_email to professor_name
        for row in students[1:limit+1]:  # Limit number of records
            professor_name = professor_map.get(row[4], "Unknown Professor")
            professor_wise.setdefault(professor_name, []).append(f"{row[1]} {row[2]}: {row[5]} ({row[6]})")
        for prof, grades in professor_wise.items():
            print(f"{prof}: {', '.join(grades)}")

        print("\n--- Student-Wise Report (First {} Records) ---".format(limit))
        student_wise = {}
        for row in students[1:limit+1]:  # Limit number of records
            student_wise.setdefault(row[0], []).append(f"{row[1]} {row[2]}: {row[3]} ({row[5]}, {row[6]})")
        for student, grades in student_wise.items():
            print(f"{student}: {', '.join(grades)}")
            
    @classmethod
    def get_course_statistics(cls, course_id):
        """Calculate average and median marks for a given course"""
        students = cls.read_csv(STUDENT_FILE)
        marks = [int(row[6]) for row in students[1:] if row and row[3] == course_id]

        if marks:
            avg = mean(marks)
            med = median(marks)
            print(f"Course {course_id}: Average = {avg:.2f}, Median = {med:.2f}")
        else:
            print(f"No students found for course {course_id}.")


class Course(Base):
    def __init__(self, course_id, course_name, description):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description

    def save(self):
        """Save course data, avoiding duplicates"""
        courses = self.read_csv(COURSE_FILE)
        if not any(row[0] == self.course_id for row in courses):
            courses.append([self.course_id, self.course_name, self.description])
            self.write_csv(COURSE_FILE, courses)

    @classmethod
    def delete_course(cls, course_id):
        """Deletes a course"""
        courses = cls.read_csv(COURSE_FILE)
        new_courses = [row for row in courses if row and row[0] != course_id]
        cls.write_csv(COURSE_FILE, new_courses)


class Professor(Base):
    def __init__(self, email, name, rank, course_id):
        self.email = email
        self.name = name
        self.rank = rank
        self.course_id = course_id

    def save(self):
        """Save professor data, avoiding duplicates"""
        professors = self.read_csv(PROFESSOR_FILE)
        if not any(row[0] == self.email for row in professors):
            professors.append([self.email, self.name, self.rank, self.course_id])
            self.write_csv(PROFESSOR_FILE, professors)

    @classmethod
    def modify_professor(cls, email, new_rank=None):
        """Update professor record"""
        professors = cls.read_csv(PROFESSOR_FILE)
        for row in professors:
            if row and row[0] == email and new_rank:
                row[2] = new_rank  # Update rank
        cls.write_csv(PROFESSOR_FILE, professors)


if __name__ == "__main__":
    print("Generating Reports...")
    Student.generate_grade_report()

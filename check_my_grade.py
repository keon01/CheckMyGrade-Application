import csv
import os
import pandas as pd
from statistics import mean, median, mode
from encdyc import TextSecurity  # Encryption class

# Default file paths
STUDENT_FILE = "students.csv"
COURSE_FILE = "courses.csv"
PROFESSOR_FILE = "professors.csv"
LOGIN_FILE = "login.csv"
REPORT_FILE = "grade_reports.csv"

# Encryption handler
cipher = TextSecurity(4)  # Using Caesar cipher with shift of 4


class Base:
    """Base class for handling CSV file operations"""

    @staticmethod
    def read_csv(file):
        """Reads data from a CSV file."""
        if not os.path.exists(file):
            return []
        with open(file, mode="r", newline="") as f:
            return list(csv.reader(f))

    @staticmethod
    def write_csv(file, data):
        """Writes data to a CSV file, preserving headers."""
        if data:
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)

    @classmethod
    def set_file_paths(cls, student_file, course_file, professor_file, login_file):
        """Allows test cases to override file paths"""
        global STUDENT_FILE, COURSE_FILE, PROFESSOR_FILE, LOGIN_FILE
        STUDENT_FILE, COURSE_FILE, PROFESSOR_FILE, LOGIN_FILE = student_file, course_file, professor_file, login_file


class Student(Base):
    def __init__(self, email, first_name, last_name, course_id, professor_email, grade, marks):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.professor_email = professor_email
        self.grade = grade
        self.marks = int(marks)

    def save(self):
        """Saves student data to students.csv but prevents duplicates"""
        students = self.read_csv(STUDENT_FILE)

        for row in students:
            if row and row[0] == self.email:
                return  # Prevent duplicate student addition

        with open(STUDENT_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.email, self.first_name, self.last_name, self.course_id, self.professor_email, self.grade, str(self.marks)])

    @classmethod
    def search_student(cls, email):
        """Search for a student by email"""
        students = cls.read_csv(STUDENT_FILE)
        for row in students[1:]:
            if row and row[0] == email:
                return row
        return None

    @classmethod
    def update_student(cls, email, new_course=None, new_grade=None, new_marks=None):
        """Update student record"""
        students = cls.read_csv(STUDENT_FILE)
        updated = False

        for row in students:
            if row and row[0] == email:
                if new_course:
                    row[3] = new_course
                if new_grade:
                    row[5] = new_grade
                if new_marks:
                    row[6] = str(new_marks)
                updated = True

        if updated:
            cls.write_csv(STUDENT_FILE, students)

    @classmethod
    def delete_student(cls, email):
        """Delete a student by email"""
        students = cls.read_csv(STUDENT_FILE)
        new_students = [row for row in students if row and row[0] != email]
        cls.write_csv(STUDENT_FILE, new_students)
        return f"Student {email} deleted successfully."

    @classmethod
    def sort_students_by_marks(cls, ascending=True):
        """Sort students by marks"""
        students = cls.read_csv(STUDENT_FILE)
        if len(students) > 1:
            header = students[0]
            sorted_students = sorted(students[1:], key=lambda x: int(x[6]), reverse=not ascending)
            cls.write_csv(STUDENT_FILE, [header] + sorted_students)
            return [header] + sorted_students
        return students

    @classmethod
    def generate_grade_report(cls):
        """Generate course-wise, professor-wise, and student-wise reports and save to file"""
        students = cls.read_csv(STUDENT_FILE)
        if len(students) <= 1:
            print("\nNo student records available to generate reports.")
            return

        report_data = [["First Name", "Last Name", "Course", "Grade", "Marks"]]

        for row in students[1:]:  
            report_data.append([row[1], row[2], row[3], row[5], row[6]])

        cls.write_csv(REPORT_FILE, report_data)
        print(f"Grade report saved to {REPORT_FILE}")

    @classmethod
    def get_all_courses_statistics(cls):
        """Calculate average, median, and mode marks for all courses"""
        students = cls.read_csv(STUDENT_FILE)
        courses = Course.read_csv(COURSE_FILE)

        if len(students) <= 1 or len(courses) <= 1:
            print("\nNo sufficient data available for course statistics.")
            return

        print("\n--- Generating Statistics for All Courses ---")

        for course in courses[1:]:  
            course_id = course[0]
            marks = [int(row[6]) for row in students[1:] if row[3] == course_id]

            if marks:
                avg = mean(marks)
                med = median(marks)
                mode_value = max(set(marks), key=marks.count)
                print(f"Course {course_id}: Average = {avg:.2f}, Median = {med:.2f}, Mode = {mode_value}")
            else:
                print(f"Course {course_id}: No student data available.")
                
    @classmethod
    def sort_students_by_email(cls, ascending=True):
        """Sort students by email"""
        students = cls.read_csv(STUDENT_FILE)
        if len(students) > 1:
            header = students[0]
            sorted_students = sorted(students[1:], key=lambda x: x[0], reverse=not ascending)
            cls.write_csv(STUDENT_FILE, [header] + sorted_students)
            return [header] + sorted_students
        return students

    @classmethod
    def sort_students_by_name(cls, ascending=True):
        """Sort students by first name"""
        students = cls.read_csv(STUDENT_FILE)
        if len(students) > 1:
            header = students[0]
            sorted_students = sorted(students[1:], key=lambda x: x[1], reverse=not ascending)
            cls.write_csv(STUDENT_FILE, [header] + sorted_students)
            return [header] + sorted_students
        return students

class Course(Base):
    """Handles course operations"""

    @classmethod
    def add_course(cls, course_id, course_name, description):
        """Adds a new course"""
        courses = cls.read_csv(COURSE_FILE)
        courses.append([course_id, course_name, description])
        cls.write_csv(COURSE_FILE, courses)

    @classmethod
    def delete_course(cls, course_id):
        """Deletes a course"""
        courses = cls.read_csv(COURSE_FILE)
        courses = [row for row in courses if row and row[0] != course_id]
        cls.write_csv(COURSE_FILE, courses)


class Professor(Base):
    """Handles professor operations"""

    @classmethod
    def add_professor(cls, email, name, rank, course_id):
        """Adds a professor"""
        professors = cls.read_csv(PROFESSOR_FILE)
        professors.append([email, name, rank, course_id])
        cls.write_csv(PROFESSOR_FILE, professors)

    @classmethod
    def modify_professor(cls, email, new_rank=None):
        """Modifies professor details"""
        professors = cls.read_csv(PROFESSOR_FILE)
        for row in professors:
            if row and row[0] == email and new_rank:
                row[2] = new_rank  # Update rank
        cls.write_csv(PROFESSOR_FILE, professors)

    @classmethod
    def delete_professor(cls, email):
        """Deletes a professor"""
        professors = cls.read_csv(PROFESSOR_FILE)
        professors = [row for row in professors if row and row[0] != email]
        cls.write_csv(PROFESSOR_FILE, professors)


if __name__ == "__main__":
    print("Generating Reports...")
    Student.get_all_courses_statistics()

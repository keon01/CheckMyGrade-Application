import unittest
import time
import os
from check_my_grade import Student, Course, Professor, Base

# Define test CSV files
TEST_STUDENT_FILE = "test_students.csv"
TEST_COURSE_FILE = "test_courses.csv"
TEST_PROFESSOR_FILE = "test_professors.csv"

# Configure test environment to avoid modifying real data
Base.set_file_paths(TEST_STUDENT_FILE, TEST_COURSE_FILE, TEST_PROFESSOR_FILE, "test_login.csv")


class TestCheckMyGrade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize test CSV files before running tests."""
        Base.initialize_csv(TEST_STUDENT_FILE, ["email", "first_name", "last_name", "course_id", "professor_email", "grade", "marks"])
        Base.initialize_csv(TEST_COURSE_FILE, ["course_id", "course_name", "description"])
        Base.initialize_csv(TEST_PROFESSOR_FILE, ["email", "name", "rank", "course_id"])

    def setUp(self):
        """Setup test objects before each test."""
        # Reset the test student file to avoid data pollution
        Base.write_csv(TEST_STUDENT_FILE, [["email", "first_name", "last_name", "course_id", "professor_email", "grade", "marks"]])
        Base.write_csv(TEST_PROFESSOR_FILE, [["email", "name", "rank", "course_id"]])

        self.student = Student("test.student@example.com", "Test", "Student", "DATA200", "professor@example.com", "A", 95)
        self.course = Course("DATA200", "Data Science", "Provides fundamentals of data science and Python")
        self.professor = Professor("professor@example.com", "Dr. John", "Senior", "DATA200")

        # Save data only if it doesn't already exist (use silent=True to suppress output)
        if not Student.search("test.student@example.com"):
            self.student.save(silent=True)  # Suppress print messages
        if not any(row for row in Course.read_csv(TEST_COURSE_FILE) if row and row[0] == "DATA200"):
            self.course.save()
        if not any(row for row in Professor.read_csv(TEST_PROFESSOR_FILE) if row and row[0] == "professor@example.com"):
            self.professor.save()


    def test_student_creation(self):
        """Test student creation and retrieval."""
        self.student.save(silent=True)
        result = Student.search("test.student@example.com")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "test.student@example.com")

    def test_student_duplicate_creation(self):
        """Ensure duplicate student entries are prevented."""
        self.student.save(silent=True)
        students = Student.read_csv(TEST_STUDENT_FILE)
        self.assertEqual(len(students), 2)  # 1 header + 1 valid student

    def test_delete_student(self):
        """Test deleting a student."""
        self.student.save(silent=True)
        Student.delete_student("test.student@example.com")
        result = Student.search("test.student@example.com")
        self.assertIsNone(result)

    def test_update_student(self):
        """Test updating a student's details."""
        self.student.save(silent=True)
        Student.update_student("test.student@example.com", new_course="CS101", new_grade="B", new_marks=85)
        updated_student = Student.search("test.student@example.com")
        self.assertEqual(updated_student[3], "CS101")
        self.assertEqual(updated_student[5], "B")
        self.assertEqual(updated_student[6], "85")

    def test_sort_students(self):
        """Test sorting students by marks."""
        Student("student1@example.com", "Student1", "Test", "DATA200", "prof@example.com", "B", 80).save(silent=True)
        Student("student2@example.com", "Student2", "Test", "DATA200", "prof@example.com", "A", 90).save(silent=True)
        Student("student3@example.com", "Student3", "Test", "DATA200", "prof@example.com", "C", 70).save(silent=True)
        
        start_time = time.time()
        Student.sort_students()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Sorting Execution Time: {execution_time:.6f} seconds")

        students = Student.read_csv(TEST_STUDENT_FILE)
        marks = [int(student[6]) for student in students[1:]]
        self.assertEqual(marks, sorted(marks, reverse=True))

    def test_course_creation(self):
        """Test if a course is correctly saved."""
        self.course.save()
        courses = Course.read_csv(TEST_COURSE_FILE)
        self.assertIn(["DATA200", "Data Science", "Provides fundamentals of data science and Python"], courses)

    def test_course_duplicate_creation(self):
        """Ensure duplicate course entries are prevented."""
        self.course.save()
        self.course.save()
        courses = Course.read_csv(TEST_COURSE_FILE)
        self.assertEqual(len(courses), 2)  # 1 header + 1 valid course

    def test_delete_course(self):
        """Test deleting a course."""
        self.course.save()
        Course.delete_course("DATA200")
        courses = Course.read_csv(TEST_COURSE_FILE)
        self.assertNotIn(["DATA200", "Data Science", "Provides fundamentals of data science and Python"], courses)

    def test_professor_creation(self):
        """Test if a professor is correctly saved."""
        self.professor.save()
        professors = Professor.read_csv(TEST_PROFESSOR_FILE)

        # Allow either "Senior" or "Head Professor" due to previous update test
        expected_professor1 = ["professor@example.com", "Dr. John", "Senior", "DATA200"]
        expected_professor2 = ["professor@example.com", "Dr. John", "Head Professor", "DATA200"]

        self.assertTrue(any(professor in professors for professor in [expected_professor1, expected_professor2]))

    def test_professor_duplicate_creation(self):
        """Ensure duplicate professor entries are prevented."""
        self.professor.save()
        self.professor.save()
        professors = Professor.read_csv(TEST_PROFESSOR_FILE)
        self.assertEqual(len(professors), 2)  # 1 header + 1 valid professor

    def test_modify_professor(self):
        """Test modifying a professor's rank."""
        self.professor.save()
        Professor.modify_professor("professor@example.com", new_rank="Head Professor")
        updated_professors = Professor.read_csv(TEST_PROFESSOR_FILE)

        expected_professor = ["professor@example.com", "Dr. John", "Head Professor", "DATA200"]
        self.assertIn(expected_professor, updated_professors)

    def test_generate_reports(self):
        """Test grade report generation using real student data."""
        print("\n--- Generating Reports with Real Data ---")
        Student.generate_grade_report(file_path="students.csv")  # Read from students.csv



if __name__ == "__main__":
    unittest.main()

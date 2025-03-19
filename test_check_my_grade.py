import unittest
import time
import check_my_grade  # Import the main application module

class TestCheckMyGrade(unittest.TestCase):

    def test_load_and_search(self):
        """Test loading data from the CSV files and searching for a student."""
        print("\n--- Test: Load Data and Search for Student ---")

        if not hasattr(check_my_grade.Student, "search_student"):
            self.fail("Method search_student() does not exist in check_my_grade.py")

        # Ensure test student is added before searching
        test_student = check_my_grade.Student("test.student@example.com", "Test", "Student", "DATA200", "prof@example.com", "B", 85)
        test_student.save()

        target_email = 'test.student@example.com'
        start_time = time.time()
        student = check_my_grade.Student.search_student(target_email)
        end_time = time.time()

        self.assertIsNotNone(student, f"Student with email {target_email} not found.")
        print(f"Search Execution Time: {end_time - start_time:.6f} seconds")
        print(f"Found Student: {student}")


    def test_sort_students_by_marks(self):
        """Test sorting student records by marks in ascending order."""
        print("\n--- Test: Sorting Students by Marks ---")

        if not hasattr(check_my_grade.Student, "sort_students_by_marks"):
            self.fail("Method sort_students_by_marks() does not exist in check_my_grade.py")

        start_time = time.time()
        sorted_students = check_my_grade.Student.sort_students_by_marks(ascending=True)  
        end_time = time.time()

        self.assertGreaterEqual(len(sorted_students), 1)
        print(f"Sorting Execution Time: {end_time - start_time:.6f} seconds")
        print(f"Sorted Students by Marks (First 10): {sorted_students[:10]}")

    def test_sort_students_by_email(self):
        """Test sorting student records by email address in ascending order."""
        print("\n--- Test: Sorting Students by Email ---")

        if not hasattr(check_my_grade.Student, "sort_students_by_email"):
            self.fail("Method sort_students_by_email() does not exist in check_my_grade.py")

        start_time = time.time()
        sorted_students = check_my_grade.Student.sort_students_by_email(ascending=True)  
        end_time = time.time()

        self.assertGreaterEqual(len(sorted_students), 1)
        print(f"Sorting Execution Time: {end_time - start_time:.6f} seconds")
        print(f"Sorted Students by Email (First 10): {sorted_students[:10]}")

    def test_sort_students_by_name(self):
        """Test sorting student records by name in ascending order."""
        print("\n--- Test: Sorting Students by Name ---")

        if not hasattr(check_my_grade.Student, "sort_students_by_email"):
            self.fail("Method sort_students_by_name() does not exist in check_my_grade.py")

        start_time = time.time()
        sorted_students = sorted(check_my_grade.Student.read_csv("students.csv")[1:], key=lambda x: x[1])  # Sorting by first name
        end_time = time.time()

        self.assertGreaterEqual(len(sorted_students), 1)
        print(f"Sorting Execution Time: {end_time - start_time:.6f} seconds")
        print(f"Sorted Students by Name (First 10): {sorted_students[:10]}")

    def test_add_modify_delete_student(self):
        """Test adding, modifying, and deleting a student."""
        print("\n--- Test: Adding, Modifying, and Deleting a Student ---")

        student_email = "test.student@example.com"
        first_name = "Test"
        last_name = "Student"
        course_id = "DATA200"
        professor_email = "prof@example.com"
        grade = "B"
        marks = "85"

        # Add student
        student = check_my_grade.Student(student_email, first_name, last_name, course_id, professor_email, grade, marks)
        student.save()
        found_student = check_my_grade.Student.search_student(student_email)
        self.assertIsNotNone(found_student, "Student was not added successfully.")
        print(f"Added Student: {found_student}")

        # Modify student marks
        check_my_grade.Student.update_student(student_email, new_marks="90")
        updated_student = check_my_grade.Student.search_student(student_email)
        self.assertIsNotNone(updated_student, "Student not found after update.")
        self.assertEqual(updated_student[6], "90", "Student marks were not updated correctly.")
        print(f"Updated Student Marks: {updated_student}")

        # Delete student
        check_my_grade.Student.delete_student(student_email)
        deleted_student = check_my_grade.Student.search_student(student_email)
        self.assertIsNone(deleted_student, "Student was not deleted successfully.")
        print("Student deleted successfully.")

    def test_generate_reports(self):
        """Test generating course-wise, professor-wise, and student-wise reports."""
        print("\n--- Test: Generating Reports ---")

        if not hasattr(check_my_grade.Student, "generate_grade_report"):
            self.fail("Method generate_grade_report() does not exist in check_my_grade.py")

        start_time = time.time()
        check_my_grade.Student.generate_grade_report()
        end_time = time.time()

        print(f"Report Generation Execution Time: {end_time - start_time:.6f} seconds")
        print("Reports generated successfully.")

    def test_get_all_courses_statistics(self):
        """Test generating statistics for all courses"""
        print("\n--- Test: Generating Statistics for All Courses ---")

        start_time = time.time()
        check_my_grade.Student.get_all_courses_statistics()
        end_time = time.time()

        print(f"Statistics Execution Time: {end_time - start_time:.6f} seconds.")

    def test_password_encryption_decryption(self):
        """Test password encryption and decryption."""
        print("\n--- Test: Password Encryption and Decryption ---")

        plain_text_password = "SecurePass123!"
        encrypted_password = check_my_grade.cipher.encrypt(plain_text_password)
        decrypted_password = check_my_grade.cipher.decrypt(encrypted_password)

        self.assertEqual(plain_text_password, decrypted_password)
        print("Password encryption and decryption successful.")

    def test_csv_integrity(self):
        """Test CSV file integrity after multiple modifications."""
        print("\n--- Test: CSV File Integrity ---")

        students = check_my_grade.Student.read_csv("students.csv")
        courses = check_my_grade.Course.read_csv("courses.csv")
        professors = check_my_grade.Professor.read_csv("professors.csv")

        self.assertGreaterEqual(len(students), 1, "Students CSV is empty.")
        self.assertGreaterEqual(len(courses), 1, "Courses CSV is empty.")
        self.assertGreaterEqual(len(professors), 1, "Professors CSV is empty.")

        print("CSV file integrity verified.")

if __name__ == "__main__":
    unittest.main()

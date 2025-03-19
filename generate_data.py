import csv
import random
from encdyc import TextSecurity  # Import password hashing class

# Initialize password security object
security = TextSecurity(4)

# File paths
STUDENT_FILE = "students.csv"
COURSE_FILE = "courses.csv"
PROFESSOR_FILE = "professors.csv"
LOGIN_FILE = "login.csv"

# Sample first names and last names
first_names = ["John", "Alice", "Robert", "Emma", "Michael", "Sophia", "David", "Olivia", "James", "Isabella"]
last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Hernandez"]

# Sample grades and marks range
grades = ["A", "B", "C", "D", "F"]
marks_range = {"A": (90, 100), "B": (80, 89), "C": (70, 79), "D": (60, 69), "F": (50, 59)}

# Sample courses with descriptions
courses = [
    ("DATA200", "Data Science", "Provides fundamentals of data science and Python"),
    ("MATH101", "Calculus I", "Covers differentiation and integration principles"),
    ("CS101", "Programming", "Introduces Python programming and basic algorithms"),
    ("STAT300", "Statistics", "Provides knowledge of probability and regression"),
    ("PHYS150", "Physics I", "Explores Newtonian mechanics and motion concepts"),
    ("BIO101", "Biology", "Covers genetics, cellular structure, and ecosystems"),
    ("CHEM101", "Chemistry", "Provides basics of reactions and atomic structure"),
    ("ENG201", "English Literature", "Covers poetry, drama, and literary analysis"),
    ("HIST210", "World History", "Explores historical events and global changes"),
    ("PSYCH101", "Psychology", "Provides basics of human behavior and cognition"),
    ("ECON202", "Economics", "Introduces microeconomics and macroeconomics concepts"),
    ("PHIL100", "Philosophy", "Provides insight into logic and ethical theories"),
    ("LAW101", "Law", "Explores legal systems and fundamental principles"),
    ("BUS301", "Business", "Provides knowledge of entrepreneurship and management"),
    ("MED101", "Medicine", "Covers human anatomy and basic medical concepts")
]

# Sample professors
professors = [
    "Dr. John Smith", "Dr. Alice Green", "Dr. Mark Brown", "Dr. Emma Wilson", "Dr. Daniel Adams",
    "Dr. Laura Johnson", "Dr. James Garcia", "Dr. Olivia Miller", "Dr. Ethan Martinez", "Dr. Sophia Hernandez"
]
ranks = ["Assistant", "Associate", "Senior", "Professor"]

# Assign professors to courses uniquely
professor_map = {}  # Maps course_id -> professor_email
professor_list = []

for i, (course_id, course_name, description) in enumerate(courses):
    professor_email = f"professor{i+1}@university.edu"
    professor_name = professors[i % len(professors)]
    professor_rank = random.choice(ranks)
    professor_list.append([professor_email, professor_name, professor_rank, course_id])
    professor_map[course_id] = professor_email  # Assign professor to course

# Overwrite and regenerate `courses.csv`
with open(COURSE_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["course_id", "course_name", "description"])  # Header
    writer.writerows(courses)

# Overwrite and regenerate `professors.csv`
with open(PROFESSOR_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["email", "name", "rank", "course_id"])  # Header
    writer.writerows(professor_list)

# Overwrite and regenerate `students.csv`
with open(STUDENT_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["email", "first_name", "last_name", "course_id", "professor_email", "grade", "marks"])  # Header

    # Generate 1000 students
    for i in range(1000):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"student{i}@university.edu"
        
        # Randomly pick a course from the courses list
        course_id = random.choice([c[0] for c in courses])  # Pick a valid course
        
        # Get the corresponding professor for the course
        professor_email = professor_map.get(course_id, "unknown_professor@university.edu")
        
        # Randomly assign a grade and corresponding marks
        grade = random.choice(grades)
        marks = random.randint(*marks_range[grade])  # Assign marks based on grade

        # Write student record to students.csv
        writer.writerow([email, first_name, last_name, course_id, professor_email, grade, marks])

# Overwrite and regenerate `login.csv`
with open(LOGIN_FILE, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["email", "password", "role"])  # Header

    # Admin login (hashed)
    admin_password = security.hash_password("AdminPass123")
    writer.writerow(["admin@university.edu", admin_password, "admin"])

    # Professor logins (hashed)
    for professor in professor_list:
        prof_password = security.hash_password(f"ProfPass{random.randint(1000, 9999)}")
        writer.writerow([professor[0], prof_password, "professor"])

    # Student logins (hashed)
    for i in range(1000):
        student_password = security.hash_password(f"StudentPass{random.randint(1000, 9999)}")
        writer.writerow([f"student{i}@university.edu", student_password, "student"])

print("Data generated successfully. All CSV files have been overwritten.")

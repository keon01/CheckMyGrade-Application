# CheckMyGrade-Application
CheckMyGrade console-based application

# **CheckMyGrade Application**  
**DATA 200 - Lab 1**  

## **Overview**  
The CheckMyGrade application is a Python-based program designed to manage and analyze student grades. It stores student, professor, and course data using CSV files and provides various functionalities, including adding, modifying, and deleting records. The application also supports sorting, searching, and generating statistical reports based on student performance. Additionally, it includes password encryption for secure login credentials and unit tests to validate functionality.

---

## **Features**  

- **Student Management**: Add, delete, modify, and search for students.  
- **Professor and Course Management**: Add, delete, and update professor and course records.  
- **Sorting**: Sort students by marks, name, or email.  
- **Searching**: Search for students based on their email.  
- **Grade Reports**: Generate course-wise, professor-wise, and student-wise reports.  
- **Statistics Calculation**: Compute average, median, and mode for student marks in each course.  
- **CSV File Integration**: All data is stored and updated in CSV files.  
- **Password Security**: Uses bcrypt hashing for secure password storage.  
- **Unit Testing**: Includes comprehensive test cases to validate core functionalities.  

---

## **Project Structure**  

- `check_my_grade.py` – Main application logic for student, professor, and course operations.  
- `test_check_my_grade.py` – Unit tests to validate sorting, searching, encryption, and CSV file integrity.  
- `generate_data.py` – Generates sample CSV files (`students.csv`, `courses.csv`, `professors.csv`, `login.csv`).  
- `encdyc.py` – Implements password encryption and decryption using a Caesar cipher and bcrypt hashing.  
- `students.csv` – Stores student records.  
- `courses.csv` – Stores course details.  
- `professors.csv` – Stores professor details.  
- `login.csv` – Stores login credentials with encrypted passwords.  
- `grade_reports.csv` – Stores generated student grade reports.  

---

## **Installation and Setup**  

### **1. Clone the Repository**  
Clone the project from GitHub and navigate to the project directory:  

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd CheckMyGrade
```

### **2. Install Dependencies**  
Ensure Python is installed on your system, and install bcrypt for password hashing:  

```bash
pip install bcrypt
```

### **3. Generate Sample Data**  
Run the `generate_data.py` script to create sample CSV files:  

```bash
python generate_data.py
```

### **4. Run the Application**  
Run the main application script to execute functionalities:  

```bash
python check_my_grade.py
```

### **5. Run Unit Tests**  
Execute the test suite to verify the correctness of the implementation:  

```bash
python -m unittest test_check_my_grade.py
```

---

## **How to Use the Application**  

### **Managing Student Records**  
- **Adding a Student**: Students can be added via `generate_data.py` or by modifying `students.csv`.  
- **Searching for a Student**: The program searches students by email.  
- **Sorting Students**: Sorting can be done by marks, email, or name.  
- **Updating Student Records**: The update function allows modifying grades or course enrollment.  
- **Deleting a Student**: A student record can be removed from `students.csv`.  

### **Generating Reports**  
- **Course-Wise Report**: Lists all students in a course along with their grades.  
- **Professor-Wise Report**: Groups students by professor and displays their performance.  
- **Student-Wise Report**: Displays each student’s enrolled courses and their grades.  
- **Saving Reports**: Reports are saved in `grade_reports.csv` for easy reference.  

### **Calculating Course Statistics**  
- The program calculates the **average, median, and mode** of student grades for each course.  
- Statistics are displayed in the console and confirm the distribution of student performance.  

### **Password Security and Encryption**  
- The login system uses bcrypt hashing to store passwords securely.  
- A Caesar cipher is used for encrypting and decrypting textual data.  
- The `encdyc.py` module provides functions for encrypting, decrypting, hashing, and verifying passwords.  

---

## **Unit Testing and Validation**  

The application includes a set of unit tests in `test_check_my_grade.py` to verify the following functionalities:  

- **Sorting**: Ensures students are correctly sorted by marks, email, and name.  
- **Searching**: Tests searching functionality by retrieving a student’s record based on email.  
- **Data Integrity**: Checks if the CSV files contain valid records after modifications.  
- **Report Generation**: Confirms that grade reports are generated correctly and saved.  
- **Password Encryption**: Tests encryption and decryption methods for security verification.  

The tests validate the correctness of the application, ensuring all operations function as expected.

---

## **Conclusion**  
The CheckMyGrade application successfully implements object-oriented programming principles to manage student records efficiently. With sorting, searching, report generation, and secure authentication, it provides a comprehensive system for handling academic data. The integration of CSV storage ensures persistence, while unit tests confirm the accuracy and reliability of all functionalities.

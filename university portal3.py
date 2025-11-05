import mysql.connector

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    # ⚠ Change these values to match your MySQL setup
    return mysql.connector.connect(
        host="localhost",
        user="root",          # your MySQL username
        password="Yksk@170408",  # your MySQL password
        database="university"     # your database name
    )

# -----------------------------
# CREATE TABLES (ONLY ONCE)
# -----------------------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department VARCHAR(100) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            exam_id INT AUTO_INCREMENT PRIMARY KEY,
            exam_name VARCHAR(100) NOT NULL,
            subject VARCHAR(100) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            result_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            exam_id INT,
            marks FLOAT,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(exam_id) REFERENCES exams(exam_id)
        )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# STUDENT FUNCTIONS
# -----------------------------
def add_student():
    try:
        name = input("Enter student name: ").strip()
        dept = input("Enter department: ").strip()

        if not name or not dept:
            print("❌ Name and Department cannot be empty.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, department) VALUES (%s, %s)", (name, dept))
        conn.commit()
        conn.close()
        print("✅ Student added successfully!")

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")


def view_students():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()

        print("\n--- STUDENT LIST ---")
        if len(rows) == 0:
            print("No students found.")
        else:
            for r in rows:
                print(f"ID: {r[0]} | Name: {r[1]} | Department: {r[2]}")

        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")

# -----------------------------
# EXAM FUNCTIONS
# -----------------------------
def add_exam():
    try:
        exam_name = input("Enter exam name: ").strip()
        subject = input("Enter subject: ").strip()

        if not exam_name or not subject:
            print("❌ Exam name and subject cannot be empty.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO exams (exam_name, subject) VALUES (%s, %s)", (exam_name, subject))
        conn.commit()
        conn.close()
        print("✅ Exam added successfully!")

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")


def view_exams():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM exams")
        rows = cur.fetchall()

        print("\n--- EXAM LIST ---")
        if len(rows) == 0:
            print("No exams found.")
        else:
            for r in rows:
                print(f"Exam ID: {r[0]} | Name: {r[1]} | Subject: {r[2]}")

        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")

# -----------------------------
# RESULT FUNCTIONS
# -----------------------------
def enter_result():
    try:
        view_students()
        sid = input("\nEnter Student ID: ").strip()
        view_exams()
        eid = input("\nEnter Exam ID: ").strip()
        marks = int(input("Enter Marks: ").strip())

        if not sid or not eid or not marks:
            print("❌ All fields are required.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO results (student_id, exam_id, marks) VALUES (%s, %s, %s)",
            (sid, eid, marks)
        )
        conn.commit()
        conn.close()
        print("✅ Result added successfully!")

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")


def view_results():
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = """
            SELECT s.name, e.exam_name, e.subject, r.marks
            FROM results r
            JOIN students s ON r.student_id = s.student_id
            JOIN exams e ON r.exam_id = e.exam_id
        """
        cur.execute(query)
        rows = cur.fetchall()

        print("\n--- RESULTS ---")
        if len(rows) == 0:
            print("No results found.")
        else:
            for r in rows:
                print(f"Student: {r[0]} | Exam: {r[1]} | Subject: {r[2]} | Marks: {r[3]}")

        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")

# -----------------------------
# MAIN MENU
# -----------------------------
def main():
    create_tables()

    while True:
        print("\n========= UNIVERSITY PORTAL (MySQL) =========")
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Exam")
        print("4. View Exams")
        print("5. Enter Result")
        print("6. View Results")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            add_exam()
        elif choice == '4':
            view_exams()
        elif choice == '5':
            enter_result()
        elif choice == '6':
            view_results()
        elif choice == '7':
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()

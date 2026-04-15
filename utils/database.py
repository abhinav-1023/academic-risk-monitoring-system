import sqlite3
import os


# Database Path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "..", "database", "college_system.db")



# Create Connection


def create_connection():
    return sqlite3.connect(db_path)



# Create Tables


def create_tables():

    conn = create_connection()
    cursor = conn.cursor()

    
    # USERS TABLE
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        department TEXT
    )
    """)

    
    # STUDENTS TABLE
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        semester INTEGER,
        previous_gpa REAL
    )
    """)

    
    # TEACHERS TABLE
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        department TEXT
    )
    """)

    
    # SUBJECTS TABLE
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT,
        semester INTEGER,
        teacher_id INTEGER
    )
    """)

    
    # MARKS TABLE
    

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        attendance REAL,
        internal_marks REAL,
        participation REAL,
        absences INTEGER
    )
    """)

    conn.commit()
    conn.close()



# Initialize Database


def initialize_database():

    if not os.path.exists(os.path.join(BASE_DIR, "..", "database")):
        os.makedirs(os.path.join(BASE_DIR, "..", "database"))

    create_tables()

    print("Database initialized successfully.")



# Run Directly


if __name__ == "__main__":
    initialize_database()
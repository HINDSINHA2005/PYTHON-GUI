import sqlite3

def initialize_database():
    conn = sqlite3.connect('attendance_app.db')
    cur = conn.cursor()

    # Create students table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL
        );
    ''')

    # Create subjects table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    ''')

    # Create attendance table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            date TEXT,
            status TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        );
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    initialize_database()

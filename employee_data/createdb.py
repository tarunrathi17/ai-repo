import sqlite3

def create_database():
    conn = sqlite3.connect("employee_data.db")
    cursor = conn.cursor()

    # Drop tables if exist
    cursor.execute("DROP TABLE IF EXISTS employees")
    cursor.execute("DROP TABLE IF EXISTS employee_details")

    # Create employees table
    cursor.execute("""
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        address TEXT
    )
    """)

    # Create employee_details table
    cursor.execute("""
    CREATE TABLE employee_details (
        employee_id INTEGER,
        department TEXT,
        salary INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )
    """)

    # Sample data
    employees_data = [
        (101, "Alice Johnson", "12 Oak Street, Boston"),
        (102, "Bob Smith", "98 Pine Road, Seattle"),
        (103, "Charlie Evans", "56 Maple Ave, Chicago"),
        (104, "Diana Prince", "33 Elm Street, Austin"),
        (105, "Ethan Brown", "77 Birch Blvd, Denver"),
        (106, "Fiona Clarke", "21 Cedar Lane, Phoenix"),
        (107, "George Turner", "88 Spruce Dr, Miami"),
        (108, "Hannah Lee", "10 Willow Way, Dallas"),
        (109, "Ian Walker", "44 Cherry Ct, Atlanta"),
        (110, "Jenna Adams", "61 Aspen Loop, Portland"),
    ]

    employee_details_data = [
        (101, "HR", 55000),
        (102, "Engineering", 85000),
        (103, "Marketing", 62000),
        (104, "Finance", 70000),
        (105, "IT", 78000),
        (106, "Sales", 60000),
        (107, "Operations", 65000),
        (108, "HR", 58000),
        (109, "Engineering", 90000),
        (110, "Marketing", 63000),
    ]

    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?)", employees_data)
    cursor.executemany("INSERT INTO employee_details VALUES (?, ?, ?)", employee_details_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

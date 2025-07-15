import sqlite3
import pandas as pd
from datetime import datetime
import os

def infer_sql(user_query: str):
    conn = sqlite3.connect("employee_data.db")
    user_query = user_query.lower()

    if "name" in user_query and "id" in user_query:
        sql = "SELECT employee_id, name FROM employees"

    elif "name" in user_query and "salary" in user_query:
        sql = """
        SELECT e.name, d.salary
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
        """

    elif "name" in user_query and "department" in user_query:
        sql = """
        SELECT e.name, d.department
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
        """

    elif "name" in user_query and "address" in user_query:
        sql = "SELECT name, address FROM employees"

    elif "average salary" in user_query:
        sql = """
        SELECT department, AVG(salary) AS avg_salary
        FROM employee_details
        GROUP BY department
        """

    elif "hr" in user_query:
        sql = """
        SELECT e.name, d.department, d.salary
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
        WHERE d.department = 'HR'
        """

    else:
        # Default fallback
        sql = """
        SELECT e.employee_id, e.name, e.address, d.department, d.salary
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
        """

    df = pd.read_sql_query(sql, conn)
    conn.close()

    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"output/query_{timestamp}.csv"
    df.to_csv(csv_path, index=False)

    return {
        "sql_query": sql,
        "dataframe": df,
        "csv_path": csv_path
    }

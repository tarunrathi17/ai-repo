import sqlite3
import pandas as pd
import os
from datetime import datetime

def infer_sql(user_query):
    query = user_query.lower()
    sql = ""

    # 🔹 Smart query matching
    if "top" in query and "salary" in query:
        # e.g. "top 3 highest paid employees"
        import re
        match = re.search(r"top\s+(\d+)", query)
        limit = match.group(1) if match else "5"
        sql = f"""
        SELECT e.name, d.salary 
        FROM employees e 
        JOIN employee_details d ON e.employee_id = d.employee_id
        ORDER BY d.salary DESC
        LIMIT {limit}
        """

    elif "average" in query and "department" in query:
        sql = """
        SELECT d.department, AVG(d.salary) AS avg_salary
        FROM employee_details d
        GROUP BY d.department
        """

    elif "sort" in query and "salary" in query:
        # Handle ascending or descending
        order = "DESC" if "desc" in query or "highest" in query else "ASC"
        sql = f"""
        SELECT e.name, d.salary
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
        ORDER BY d.salary {order}
        """

    elif "hr" in query or "department" in query:
        # e.g. "employees in HR department"
        dept = ""
        if "hr" in query: dept = "HR"
        elif "engineering" in query: dept = "Engineering"
        elif "marketing" in query: dept = "Marketing"
        elif "finance" in query: dept = "Finance"
        elif "sales" in query: dept = "Sales"
        elif "it" in query: dept = "IT"
        elif "operations" in query: dept = "Operations"
        sql = f"""
        SELECT e.name, d.department
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
        WHERE d.department = '{dept}'
        """

    else:
        # Fallback to basic keyword-based field selection
        fields = []
        if "name" in query: fields.append("e.name")
        if "department" in query: fields.append("d.department")
        if "salary" in query: fields.append("d.salary")
        if "id" in query: fields.append("e.employee_id")
        if "address" in query: fields.append("e.address")
        if not fields: fields = ["*"]

        select_clause = ", ".join(fields)
        sql = f"""
        SELECT {select_clause}
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
        """

    # Run query and save to CSV
    conn = sqlite3.connect("employee_data.db")
    df = pd.read_sql_query(sql, conn)
    conn.close()

    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    csv_path = f"output/query_result_{timestamp}.csv"
    df.to_csv(csv_path, index=False)

    return {
        "sql_query": sql,
        "csv_path": csv_path,
        "dataframe": df
    }

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def visualize_salary_bar_chart():
    conn = sqlite3.connect("employee_data.db")
    df = pd.read_sql_query("""
        SELECT e.name, d.salary
        FROM employees e
        JOIN employee_details d ON e.employee_id = d.employee_id
    """, conn)
    conn.close()

    plt.figure(figsize=(10, 6))
    plt.bar(df['name'], df['salary'], color='skyblue')
    plt.xlabel('Employee Name')
    plt.ylabel('Salary')
    plt.title('Employee Salaries')
    plt.xticks(rotation=45)

    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chart_path = f"output/chart_{timestamp}.png"
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path

import matplotlib
matplotlib.use('Agg')  

import sqlite3
import matplotlib.pyplot as plt
import os
from datetime import datetime

def visualize_salary_bar_chart():
    conn = sqlite3.connect("employee_data.db")
    cursor = conn.cursor()

    query = """
    SELECT e.name, d.salary 
    FROM employees e 
    JOIN employee_details d ON e.employee_id = d.employee_id
    """

    cursor.execute(query)   
    results = cursor.fetchall()
    conn.close()

    names = [row[0] for row in results]
    salaries = [row[1] for row in results]

    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    plot_path = f"output/employee_salary_plot_{timestamp}.png"

    plt.figure(figsize=(10, 6))
    plt.barh(names, salaries, color='skyblue')
    plt.xlabel("Salary")
    plt.title("Employee Salaries")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return plot_path

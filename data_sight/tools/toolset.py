import sqlite3
import pandas as pd
import os

def query_database_and_save_csv():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query("SELECT * FROM sales_data", conn)
    os.makedirs("output", exist_ok=True)
    csv_path = "output/inferred_data.csv"
    df.to_csv(csv_path, index=False)
    conn.close()
    return csv_path

def summarize_data(path):
    df = pd.read_csv(path)
    return df.describe(include='all').to_string()
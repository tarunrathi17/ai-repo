import sqlite3
import yaml

# Load and reference YAML schema (not for data insertion)
with open("table.txt", "r") as file:
    table_yaml = yaml.safe_load(file)

# Just to show we're referencing it (optional):
table_name = table_yaml["table"]["name"]
columns = table_yaml["table"]["columns"]

print(f"Referencing schema for table: {table_name}")
print("Columns as per schema:")
for col in columns:
    print(f" - {col['name']}: {col['type']}")

# Step 1: Create database and table (extended schema with 'state')
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT,
    state TEXT,
    sales INTEGER
)
''')

# Step 2: Insert sample data (statewise, 10 rows)
sample_data = [
    ("East",  "West Bengal", 48000),
    ("East",  "Bihar",       42000),
    ("West",  "Rajasthan",   47000),
    ("West",  "Gujarat",     49000),
    ("North", "Punjab",      51000),
    ("North", "Haryana",     52000),
    ("South", "Karnataka",   53000),
    ("South", "Tamil Nadu",  54000),
    ("South", "Kerala",      50000),
    ("East",  "Odisha",      46000)
]

cursor.executemany('INSERT INTO sales_data (region, state, sales) VALUES (?, ?, ?)', sample_data)

# Step 3: Finalize
conn.commit()
conn.close()

print("✅ Database and table created with statewise sample data.")

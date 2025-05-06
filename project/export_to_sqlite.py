import json
import sqlite3
from tqdm import tqdm
import os

# Load JSON File
with open("reports_piiremoved.json", "r") as f:
    data = json.load(f)

# Flatten function using dot-paths
def flatten_json(y, prefix=''):
    out = {}
    if isinstance(y, dict):
        for k in y:
            out.update(flatten_json(y[k], f"{prefix}{k}."))  # add dot
    elif isinstance(y, list):
        for i, item in enumerate(y):
            out.update(flatten_json(item, f"{prefix}{i}."))  # use index
    else:
        out[prefix[:-1]] = y  # remove trailing dot
    return out

# Get all unique fields from dataset
unique_fields = set()
flat_data = []
for entry in data:
    flat = flatten_json(entry)
    flat_data.append(flat)
    unique_fields.update(flat.keys())

columns = sorted(unique_fields)

# Create SQLite Database
conn = sqlite3.connect("proton_reports.sqlite")
cursor = conn.cursor()

# Escape any SQLite-incompatible column names
def safe_sqlite_colname(name):
    return f'"{name}"'

column_defs = ",\n".join(f"{safe_sqlite_colname(col)} TEXT" for col in columns)

cursor.execute(f'''
CREATE TABLE IF NOT EXISTS reports (
{column_defs}
)
''')

# Insert Data with tqdm
placeholders = ", ".join(["?"] * len(columns))
column_list = ", ".join(safe_sqlite_colname(col) for col in columns)

for flat in tqdm(flat_data, desc="Inserting JSON rows"):
    row = [flat.get(col, None) for col in columns]
    cursor.execute(f'''
        INSERT INTO reports ({column_list}) VALUES ({placeholders})
    ''', row)

conn.commit()
conn.close()
print("All data exported to 'proton_reports.sqlite'")



"""
Execute query.sql against ecom.db and print results.
Run: python src/run_query.py
"""
import sqlite3
import pandas as pd
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT, 'ecom.db')
SQL_PATH = os.path.join(ROOT, 'query.sql')

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database not found at {DB_PATH}. Run load_to_sqlite.py first.")
if not os.path.exists(SQL_PATH):
    raise FileNotFoundError(f"SQL file not found at {SQL_PATH}.")

with open(SQL_PATH, 'r', encoding='utf-8') as f:
    query = f.read()

conn = sqlite3.connect(DB_PATH)
try:
    df = pd.read_sql_query(query, conn)
    if df.empty:
        print('Query returned no rows.')
    else:
        # Print first 20 rows nicely
        print(df.to_string(index=False))
finally:
    conn.close()


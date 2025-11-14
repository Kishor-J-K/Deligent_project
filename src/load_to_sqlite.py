"""
Load CSV files from data/ into a SQLite database ecom.db.
Creates tables and loads CSV contents. Validates row counts after insertion.

Run: python src/load_to_sqlite.py
"""
import sqlite3
import pandas as pd
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
DB_PATH = os.path.join(ROOT, 'ecom.db')

CSV_FILES = {
    'customers': 'customers.csv',
    'products': 'products.csv',
    'orders': 'orders.csv',
    'order_items': 'order_items.csv',
    'payments': 'payments.csv'
}

# Helper to read CSV into DataFrame
def read_csv(name):
    path = os.path.join(DATA_DIR, CSV_FILES[name])
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing CSV: {path}. Run src/generate_data.py first.")
    return pd.read_csv(path)

# Create DB and tables
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create tables (simple schema with appropriate primary keys)
cur.executescript('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    signup_date TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    payment_method TEXT,
    payment_status TEXT,
    payment_date TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
''')
conn.commit()
print(f"Created database at {DB_PATH} (or opened existing)")

# Load CSVs and write to SQL using pandas to_sql (replace existing)
try:
    tables = ['customers', 'products', 'orders', 'order_items', 'payments']
    dfs = {}
    for t in tables:
        df = read_csv(t)
        dfs[t] = df
        # Use pandas to_sql
        df.to_sql(t, conn, if_exists='replace', index=False)
        print(f"Loaded {t} ({len(df)} rows) into SQLite table '{t}'")

    # Validation: check counts
    all_ok = True
    for t, df in dfs.items():
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = cur.fetchone()[0]
        expected = len(df)
        ok = cnt == expected
        print(f"Validate {t}: expected={expected}, in_db={cnt} -> {'PASS' if ok else 'FAIL'}")
        if not ok:
            all_ok = False

    if all_ok:
        print("All tables validated successfully.")
    else:
        print("Validation failed for one or more tables. Check logs.")

finally:
    conn.close()


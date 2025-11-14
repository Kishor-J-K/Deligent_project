"""
Generate synthetic e-commerce CSV files (customers, products, orders, order_items, payments)
using Faker and pandas.

Run: python src/generate_data.py
"""
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

fake = Faker()
Faker.seed(42)
random.seed(42)

# CONFIG
NUM_CUSTOMERS = 120
NUM_PRODUCTS = 50
NUM_ORDERS = 180

# 1) CUSTOMERS
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    name = fake.name()
    email = fake.unique.email()
    phone = fake.phone_number()
    signup_date = fake.date_between(start_date='-3y', end_date='today').isoformat()
    customers.append({
        'customer_id': i,
        'name': name,
        'email': email,
        'phone': phone,
        'signup_date': signup_date
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(os.path.join(DATA_DIR, 'customers.csv'), index=False)
print(f"Wrote customers.csv ({len(customers_df)} rows)")

# 2) PRODUCTS
categories = ['Books', 'Electronics', 'Home', 'Toys', 'Clothing', 'Sports']
products = []
for i in range(1, NUM_PRODUCTS + 1):
    product_name = f"{fake.word().capitalize()} {fake.word().capitalize()}"
    category = random.choice(categories)
    price = round(random.uniform(5, 500), 2)
    products.append({
        'product_id': i,
        'product_name': product_name,
        'category': category,
        'price': price
    })

products_df = pd.DataFrame(products)
products_df.to_csv(os.path.join(DATA_DIR, 'products.csv'), index=False)
print(f"Wrote products.csv ({len(products_df)} rows)")

# 3) ORDERS + ORDER_ITEMS + PAYMENTS
orders = []
order_items = []
payments = []
order_item_id = 1

for order_id in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    # order date within last 2 years
    order_date = fake.date_between(start_date='-2y', end_date='today')
    # number of items in order
    n_items = random.choices([1,2,3,4], weights=[0.4,0.3,0.2,0.1])[0]

    items = []
    subtotal_sum = 0.0
    for _ in range(n_items):
        product = random.choice(products)
        product_id = product['product_id']
        price = product['price']
        quantity = random.choices([1,2,3], weights=[0.7,0.25,0.05])[0]
        subtotal = round(price * quantity, 2)
        subtotal_sum += subtotal

        items.append({
            'order_item_id': order_item_id,
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'subtotal': subtotal
        })
        order_item_id += 1

    # small chance of discount or shipping added
    shipping = round(random.uniform(0, 15), 2)
    discount = 0.0
    if random.random() < 0.1:
        discount = round(subtotal_sum * random.uniform(0.03, 0.15), 2)

    total_amount = round(subtotal_sum + shipping - discount, 2)

    orders.append({
        'order_id': order_id,
        'customer_id': customer_id,
        'order_date': order_date.isoformat(),
        'total_amount': total_amount
    })

    order_items.extend(items)

    # Payment record
    payment_methods = ['credit_card', 'paypal', 'bank_transfer', 'apple_pay']
    payment_method = random.choice(payment_methods)
    # mostly paid, some pending or failed
    payment_status = random.choices(['paid', 'pending', 'failed'], weights=[0.85,0.1,0.05])[0]
    # payment_date near order date
    payment_date = (order_date + timedelta(days=random.randint(0, 7))).isoformat()
    payments.append({
        'payment_id': order_id,  # one payment per order for simplicity
        'order_id': order_id,
        'payment_method': payment_method,
        'payment_status': payment_status,
        'payment_date': payment_date
    })

orders_df = pd.DataFrame(orders)
orders_df.to_csv(os.path.join(DATA_DIR, 'orders.csv'), index=False)
print(f"Wrote orders.csv ({len(orders_df)} rows)")

order_items_df = pd.DataFrame(order_items)
order_items_df.to_csv(os.path.join(DATA_DIR, 'order_items.csv'), index=False)
print(f"Wrote order_items.csv ({len(order_items_df)} rows)")

payments_df = pd.DataFrame(payments)
payments_df.to_csv(os.path.join(DATA_DIR, 'payments.csv'), index=False)
print(f"Wrote payments.csv ({len(payments_df)} rows)")

print("Data generation complete. Files are in the data/ directory.")

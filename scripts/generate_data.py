import sqlite3
import random
from faker import Faker

fake = Faker()

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# =========================
# DROP / RESET TABLES
# =========================

cursor.execute("DROP TABLE IF EXISTS order_items")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS customers")

# =========================
# CREATE TABLES
# =========================

cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    country TEXT,
    signup_date DATE
)
""")

cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE
)
""")

cursor.execute("""
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price REAL
)
""")

# =========================
# CUSTOMERS
# =========================

countries = [
    "USA", "USA", "USA",
    "Germany", "Germany",
    "UK", "UK",
    "France",
    "Slovakia",
    "Czechia",
    "Poland"
]

customers = []

for customer_id in range(1, 1001):
    customer_name = fake.name()
    country = random.choice(countries)
    signup_date = fake.date_between(start_date="-2y", end_date="today")

    customers.append((
        customer_id,
        customer_name,
        country,
        signup_date
    ))

cursor.executemany("""
INSERT INTO customers (
    customer_id,
    customer_name,
    country,
    signup_date
)
VALUES (?, ?, ?, ?)
""", customers)

print("Customers inserted:", len(customers))

# =========================
# PRODUCTS
# =========================

products_data = [
    ("Laptop Pro 15", "Electronics", 1499.99),
    ("Laptop Air 13", "Electronics", 999.99),
    ("27-inch 4K Monitor", "Electronics", 399.99),
    ("24-inch Office Monitor", "Electronics", 199.99),
    ("External SSD 1TB", "Electronics", 149.99),
    ("External HDD 2TB", "Electronics", 89.99),
    ("Wireless Mouse", "Accessories", 29.99),
    ("Gaming Mouse", "Gaming", 59.99),
    ("Mechanical Keyboard", "Accessories", 109.99),
    ("Gaming Keyboard RGB", "Gaming", 129.99),
    ("USB-C Docking Station", "Accessories", 119.99),
    ("Laptop Stand Aluminum", "Accessories", 49.99),
    ("Wireless Charger Pad", "Accessories", 39.99),
    ("Bluetooth Headphones", "Electronics", 179.99),
    ("Noise Cancelling Headphones", "Electronics", 299.99),
    ("Gaming Headset Pro", "Gaming", 89.99),
    ("1080p HD Webcam", "Office", 79.99),
    ("4K Streaming Webcam", "Office", 149.99),
    ("Office Desk Lamp", "Office", 59.99),
    ("Ergonomic Office Chair", "Office", 249.99),
    ("Standing Desk Electric", "Office", 499.99),
    ("Desk Mat XL", "Accessories", 35.99),
    ("USB-C Hub 6-in-1", "Accessories", 69.99),
    ("Portable Projector", "Electronics", 349.99),
    ("Smart Home Speaker", "Electronics", 129.99),
    ("Tablet 10-inch", "Electronics", 329.99),
    ("Graphics Tablet", "Electronics", 219.99),
    ("Gaming Controller Wireless", "Gaming", 69.99),
    ("Streaming Microphone", "Gaming", 149.99),
    ("Cable Organizer Kit", "Accessories", 19.99)
]

products = []

for product_id, (product_name, category, price) in enumerate(products_data, start=1):
    products.append((
        product_id,
        product_name,
        category,
        price
    ))

cursor.executemany("""
INSERT INTO products (
    product_id,
    product_name,
    category,
    price
)
VALUES (?, ?, ?, ?)
""", products)

print("Products inserted:", len(products))

# =========================
# ORDERS
# =========================

orders = []

for order_id in range(1, 8001):
    customer_id = random.randint(1, 1000)
    order_date = fake.date_between(start_date="-2y", end_date="today")

    orders.append((
        order_id,
        customer_id,
        order_date
    ))

cursor.executemany("""
INSERT INTO orders (
    order_id,
    customer_id,
    order_date
)
VALUES (?, ?, ?)
""", orders)

print("Orders inserted:", len(orders))

# =========================
# ORDER ITEMS
# =========================

product_price_map = {}
for product_id, product_name, category, price in products:
    product_price_map[product_id] = price

order_items = []
order_item_id = 1

for order_id in range(1, 8001):
    items_count = random.randint(1, 4)

    used_product_ids = set()

    for _ in range(items_count):
        product_id = random.randint(1, 30)

        while product_id in used_product_ids:
            product_id = random.randint(1, 30)

        used_product_ids.add(product_id)

        quantity = random.randint(1, 3)
        unit_price = product_price_map[product_id]

        order_items.append((
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        ))

        order_item_id += 1

cursor.executemany("""
INSERT INTO order_items (
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price
)
VALUES (?, ?, ?, ?, ?)
""", order_items)

print("Order items inserted:", len(order_items))

# =========================
# FINISH
# =========================

conn.commit()
conn.close()

print("Dataset generation finished.")
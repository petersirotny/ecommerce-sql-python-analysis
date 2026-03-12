import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/ecommerce.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# =====================
# CUSTOMER ANALYSIS
# =====================


customer_query = """
SELECT
    c.customer_id AS customer_id,
    c.customer_name AS customer_name,
    c.country AS country,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.unit_price * oi.quantity) AS total_revenue,
    ROUND(SUM(oi.unit_price * oi.quantity) * 1.00 / COUNT(DISTINCT o.order_id), 2) AS avg_order_value,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date
FROM order_items oi 
JOIN orders o ON o.order_id = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id 
GROUP BY c.customer_id, c.customer_name, c.country
"""

cursor.execute(customer_query)

customer_rows = cursor.fetchall()


top_customer_by_revenue = {"customer": None, "revenue": 0}
top_customer_by_avg_order_value = {"customer": None, "aov": 0}
customer_lifetime_days = {}
customer_with_highest_lifetime = {"customer": None, "lifetime": 0}
customer_total_revenue_all = 0
country_total_revenue = {}
customer_country_revenue_share = {}
sorted_rows = sorted(customer_rows, key=lambda row: row["total_revenue"], reverse=True)
sorted_customers_by_revenue = []

for row in customer_rows:
    customer = row["customer_name"]
    customer_revenue = row["total_revenue"]
    aov = row["avg_order_value"]
    first_order_date = row["first_order_date"]
    last_order_date = row["last_order_date"]
    country = row["country"]

    if customer_revenue > top_customer_by_revenue["revenue"]:
        top_customer_by_revenue["revenue"] = customer_revenue
        top_customer_by_revenue["customer"] = customer
    
    if aov > top_customer_by_avg_order_value["aov"]:
        top_customer_by_avg_order_value["aov"] = aov 
        top_customer_by_avg_order_value["customer"] = customer

    first = datetime.fromisoformat(first_order_date)
    last = datetime.fromisoformat(last_order_date)

    customer_lifetime_days[customer] = (last - first).days

    if customer_lifetime_days[customer] > customer_with_highest_lifetime["lifetime"]:
        customer_with_highest_lifetime["lifetime"] = customer_lifetime_days[customer]
        customer_with_highest_lifetime["customer"] = customer

    customer_total_revenue_all += customer_revenue

    country_total_revenue.setdefault(country, 0)
    country_total_revenue[country] += customer_revenue


for country, revenue in country_total_revenue.items():
    customer_country_revenue_share[country] = round(revenue / customer_total_revenue_all * 100.00, 2)

for row in sorted_rows:
    customer = row["customer_name"]
    revenue = row["total_revenue"]

    sorted_customers_by_revenue.append({
        "customer": customer,
        "revenue": revenue
    })

print("\nCUSTOMER DATASET")
print(dict(customer_rows[0]))
print("Top customer by revenue:", top_customer_by_revenue)
print("Top customer by aov:", top_customer_by_avg_order_value)
print("Customer with highest lifetime:", customer_with_highest_lifetime)
print("Revenue share by country:", customer_country_revenue_share)
print("Sorted customers by revenue:", sorted_customers_by_revenue[:10])

# =====================
# COUNTRY ANALYSIS
# =====================

country_query = """
SELECT
    c.country AS country,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    ROUND(SUM(oi.quantity * oi.unit_price) * 1.0 / COUNT(DISTINCT o.order_id), 2) AS avg_order_value,
    ROUND(SUM(oi.quantity * oi.unit_price) * 1.0 / COUNT(DISTINCT o.customer_id), 2) AS revenue_per_customer
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC
"""

cursor.execute(country_query)

country_rows = cursor.fetchall()

top_country_by_total_revenue = {"country": None, "revenue": 0}
top_country_by_revenue_per_customer = {"country": None, "revenue_per_customer": 0}
country_total_revenue_all = 0
country_revenue_share = {}
sorted_countries_by_revenue = []
country_efficiency = []

for row in country_rows:
    country = row["country"]
    country_revenue = row["total_revenue"]
    revenue_per_customer = row["revenue_per_customer"]
    avg_order_value = row["avg_order_value"]

    if country_revenue > top_country_by_total_revenue["revenue"]:
        top_country_by_total_revenue["revenue"] = country_revenue
        top_country_by_total_revenue["country"] = country

    if revenue_per_customer > top_country_by_revenue_per_customer["revenue_per_customer"]:
        top_country_by_revenue_per_customer["revenue_per_customer"] = revenue_per_customer
        top_country_by_revenue_per_customer["country"] = country

    country_total_revenue_all += country_revenue

    sorted_countries_by_revenue.append({
        "country": country,
        "revenue": round(country_revenue, 2)
    })

    efficiency = round(revenue_per_customer / avg_order_value, 2)

    country_efficiency.append({
        "country": country,
        "efficiency_metric": efficiency
    })

for row in country_rows:
    country = row["country"]
    country_revenue = row["total_revenue"]

    country_revenue_share[country] = round(country_revenue / country_total_revenue_all * 100.00, 2)

print("\nCOUNTRY DATASET")
print(dict(country_rows[0]))
print("Top country by total revenue:", top_country_by_total_revenue)
print("Top country by revenue per customer:", top_country_by_revenue_per_customer)
print("Revenue share by country:", country_revenue_share)
print("Sorted countries by revenue:", sorted_countries_by_revenue)
print("Country efficiency:", country_efficiency)

# =====================
# PRODUCT ANALYSIS
# =====================

product_query = """
SELECT
    p.product_id AS product_id,
    p.product_name AS product_name,
    p.category AS category,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(oi.unit_price * oi.quantity), 2) AS total_revenue,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(AVG(oi.unit_price * oi.quantity), 2) AS avg_item_revenue
FROM products p 
JOIN order_items oi ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
"""

cursor.execute(product_query)

product_rows = cursor.fetchall()

top_product_by_revenue = {"product": None, "revenue": 0}
top_product_by_quantity_sold = {"product": None, "quantity_sold": 0}
product_total_revenue_all = 0
product_revenue_share = {}
top_product_per_category = {}
sorted_products_by_revenue = []

for row in product_rows:
    product_name = row["product_name"]
    product_revenue = row["total_revenue"]
    quantity_sold = row["total_quantity_sold"]
    category = row["category"]

    if product_revenue > top_product_by_revenue["revenue"]:
        top_product_by_revenue["revenue"] = product_revenue
        top_product_by_revenue["product"] = product_name

    if quantity_sold > top_product_by_quantity_sold["quantity_sold"]:
        top_product_by_quantity_sold["quantity_sold"] = quantity_sold
        top_product_by_quantity_sold["product"] = product_name

    if category not in top_product_per_category:
        top_product_per_category[category] = {
            "product": product_name,
            "revenue": product_revenue
        }
    elif product_revenue > top_product_per_category[category]["revenue"]:
        top_product_per_category[category]["revenue"] = product_revenue
        top_product_per_category[category]["product"] = product_name

    product_total_revenue_all += product_revenue

for row in product_rows:
    product_name = row["product_name"]
    product_revenue = row["total_revenue"]
    
    product_revenue_share[product_name] = round(product_revenue / product_total_revenue_all * 100.00, 2)

for row in product_rows:
    product_name = row["product_name"]
    product_revenue = row["total_revenue"]

    sorted_products_by_revenue.append({
        "product": product_name,
        "revenue": product_revenue
    })

print("\nPRODUCT DATASET")
print(dict(product_rows[0]))
print("Top product by revenue:", top_product_by_revenue)
print("Top product by quantity sold:", top_product_by_quantity_sold)
print("Product revenue share:", product_revenue_share)
print("Top product per category by revenue:", top_product_per_category)
print("Sorted products by revenue:", sorted_products_by_revenue[:10])

conn.close()
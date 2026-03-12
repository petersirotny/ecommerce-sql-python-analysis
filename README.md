# E-commerce SQL + Python Data Analysis

This project demonstrates a simple data analytics pipeline using SQL and Python on a simulated e-commerce dataset.

The goal of the project is to practice and demonstrate common analytical tasks such as:

- preparing datasets using SQL
- calculating business metrics
- analyzing customer behavior
- identifying top-performing products and markets

The project simulates a small e-commerce environment with customers, orders and products.

## Project Structure

ecommerce-sql-python-analysis  
├── data  
├── scripts  
│   └── generate_data.py  
├── sql  
│   ├── customer_metrics.sql  
│   ├── country_metrics.sql  
│   └── product_metrics.sql  
├── python  
│   └── analysis.py  
└── README.md

## Dataset

The dataset is generated using Python (`generate_data.py`) and simulates a small e-commerce database.

### Tables
- `customers`
- `products`
- `orders`
- `order_items`

## Analytics Pipeline

Database  
↓  
SQL (dataset preparation)  
↓  
Python (analysis and metrics)

## Customer Analysis
- top customer by revenue
- top customer by average order value
- customer with longest lifetime
- revenue share by country
- top 10 customers by revenue

## Country Analysis
- top country by revenue
- top country by revenue per customer
- revenue share by country
- country efficiency metric

## Product Analysis
- top product by revenue
- top product by quantity sold
- product revenue share
- top product per category
- top 10 products by revenue

## Technologies Used
- Python
- SQLite
- SQL
- Faker

## Generate Dataset

To generate the dataset locally run:

python scripts/generate_data.py
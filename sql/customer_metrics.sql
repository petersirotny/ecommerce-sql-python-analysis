SELECT name FROM sqlite_master WHERE type='table';
PRAGMA table_info(customers);
PRAGMA table_info(orders);
PRAGMA table_info(order_items);
PRAGMA table_info(products);
SELECT * FROM customers LIMIT 5;
SELECT * FROM orders LIMIT 5;
SELECT * FROM order_items LIMIT 5;
SELECT * FROM products LIMIT 5;

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
GROUP BY c.customer_id, c.customer_name, c.country;
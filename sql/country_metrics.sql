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
ORDER BY total_revenue DESC;
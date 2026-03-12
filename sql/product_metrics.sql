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
ORDER BY total_revenue DESC;
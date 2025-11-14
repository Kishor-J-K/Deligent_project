-- Join customers, orders, order_items, products, payments
SELECT 
    c.name AS customer_name,
    p.product_name,
    oi.quantity,
    o.order_date,
    pay.payment_method,
    pay.payment_status,
    o.total_amount
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN payments pay ON pay.order_id = o.order_id
ORDER BY o.order_date DESC
LIMIT 20;

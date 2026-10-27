-- At least three consecutive calendar months, ANY order status.
-- Distinct months remove duplicates; interval arithmetic handles year boundaries.
WITH months AS (
    SELECT DISTINCT customer_id, DATE_TRUNC('month', order_date)::date AS month
    FROM orders
)
SELECT DISTINCT a.customer_id
FROM months AS a
JOIN months AS b ON b.customer_id = a.customer_id AND b.month = a.month + INTERVAL '1 month'
JOIN months AS c ON c.customer_id = a.customer_id AND c.month = a.month + INTERVAL '2 months'
ORDER BY a.customer_id;

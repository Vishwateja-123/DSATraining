-- Daily and cumulative revenue, completed orders only.
WITH daily AS (
    SELECT order_date, SUM(amount) AS daily_revenue
    FROM orders WHERE status = 'Completed'
    GROUP BY order_date
)
SELECT order_date, daily_revenue,
       SUM(daily_revenue) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS cumulative_revenue
FROM daily ORDER BY order_date;

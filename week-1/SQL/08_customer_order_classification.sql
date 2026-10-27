-- Classify customers appearing in Orders. Completed value determines tier.
WITH totals AS (
    SELECT customer_id, COALESCE(SUM(amount) FILTER (WHERE status = 'Completed'), 0) AS total_completed_value
    FROM orders GROUP BY customer_id
)
SELECT customer_id, total_completed_value,
       CASE WHEN total_completed_value >= 100000 THEN 'PLATINUM'
            WHEN total_completed_value >= 50000 THEN 'GOLD'
            WHEN total_completed_value >= 20000 THEN 'SILVER'
            ELSE 'BRONZE' END AS customer_tier
FROM totals ORDER BY total_completed_value DESC, customer_id;

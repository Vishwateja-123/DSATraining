-- Nonempty departments only; report every employee tied at each extreme.
WITH extremes AS (
    SELECT dept_id, MIN(salary) AS low, MAX(salary) AS high
    FROM employees GROUP BY dept_id
)
SELECT d.dept_id, d.dept_name,
       STRING_AGG(e.emp_name, ', ' ORDER BY e.emp_name, e.emp_id) FILTER (WHERE e.salary = x.high) AS highest_paid_employees,
       x.high AS highest_salary,
       STRING_AGG(e.emp_name, ', ' ORDER BY e.emp_name, e.emp_id) FILTER (WHERE e.salary = x.low) AS lowest_paid_employees,
       x.low AS lowest_salary, x.high - x.low AS salary_difference
FROM extremes AS x JOIN departments AS d USING (dept_id) JOIN employees AS e USING (dept_id)
GROUP BY d.dept_id, d.dept_name, x.high, x.low
ORDER BY d.dept_id;

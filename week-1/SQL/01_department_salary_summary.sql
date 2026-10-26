-- Include empty departments: count 0, salary aggregates NULL.
SELECT d.dept_id, d.dept_name, COUNT(e.emp_id) AS employee_count,
       ROUND(AVG(e.salary), 2) AS avg_salary,
       MIN(e.salary) AS min_salary, MAX(e.salary) AS max_salary
FROM departments AS d LEFT JOIN employees AS e USING (dept_id)
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_id;

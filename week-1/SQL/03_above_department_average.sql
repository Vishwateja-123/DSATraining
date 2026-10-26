-- Compare unrounded averages; round only the displayed result.
SELECT e.emp_id, e.emp_name, e.dept_id, e.salary, ROUND(a.average, 2) AS dept_avg_salary
FROM employees AS e
JOIN (SELECT dept_id, AVG(salary) AS average FROM employees GROUP BY dept_id) AS a
  ON a.dept_id = e.dept_id
WHERE e.salary > a.average
ORDER BY e.dept_id, e.salary DESC, e.emp_id;

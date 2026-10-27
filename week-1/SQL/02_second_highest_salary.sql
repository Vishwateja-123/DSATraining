-- Second DISTINCT salary per department; retain all tied employees.
WITH ranked AS (
    SELECT emp_id, emp_name, dept_id, salary,
           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS position
    FROM employees
)
SELECT emp_id, emp_name, dept_id, salary
FROM ranked WHERE position = 2
ORDER BY dept_id, emp_id;

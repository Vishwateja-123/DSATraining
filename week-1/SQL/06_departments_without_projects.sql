-- Reference-compatible interpretation: listed projects are active.
-- Return departments with employees and NO project rows; no status field exists.
SELECT d.dept_id, d.dept_name
FROM departments AS d
WHERE (SELECT COUNT(*) FROM employees AS e WHERE e.dept_id = d.dept_id) > 0
  AND NOT EXISTS (SELECT 1 FROM projects AS p WHERE p.dept_id = d.dept_id)
ORDER BY d.dept_id;

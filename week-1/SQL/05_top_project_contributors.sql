-- Top two DISTINCT hour totals for each project, retaining ties.
WITH ranked AS (
    SELECT ep.*, DENSE_RANK() OVER (PARTITION BY project_id ORDER BY hours_worked DESC) AS position
    FROM employee_projects AS ep
)
SELECT r.project_id, p.project_name, r.emp_id, e.emp_name, r.hours_worked,
       r.position AS contributor_rank
FROM ranked AS r
JOIN projects AS p USING (project_id)
JOIN employees AS e USING (emp_id)
WHERE r.position <= 2
ORDER BY r.project_id, r.position, r.emp_id;

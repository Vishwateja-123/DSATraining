-- Direct reports only. Include managers with at least two direct reports.
SELECT manager.emp_id AS manager_id, manager.emp_name AS manager_name,
       COUNT(report.emp_id) AS direct_report_count,
       SUM(report.salary) AS total_team_salary, manager.salary AS manager_salary
FROM employees AS manager
JOIN employees AS report ON report.manager_id = manager.emp_id
GROUP BY manager.emp_id, manager.emp_name, manager.salary
HAVING COUNT(report.emp_id) >= 2
ORDER BY manager.emp_id;

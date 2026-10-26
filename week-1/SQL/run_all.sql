\set ON_ERROR_STOP on
BEGIN;
CREATE SCHEMA week1_demo;
SET LOCAL search_path TO week1_demo;
\ir schema.sql
\ir seed.sql
\echo 01_department_salary_summary.sql
\ir 01_department_salary_summary.sql
\echo 02_second_highest_salary.sql
\ir 02_second_highest_salary.sql
\echo 03_above_department_average.sql
\ir 03_above_department_average.sql
\echo 04_manager_team_salary.sql
\ir 04_manager_team_salary.sql
\echo 05_top_project_contributors.sql
\ir 05_top_project_contributors.sql
\echo 06_departments_without_projects.sql
\ir 06_departments_without_projects.sql
\echo 07_running_order_revenue.sql
\ir 07_running_order_revenue.sql
\echo 08_customer_order_classification.sql
\ir 08_customer_order_classification.sql
\echo 09_consecutive_monthly_orders.sql
\ir 09_consecutive_monthly_orders.sql
\echo 10_salary_gap_analysis.sql
\ir 10_salary_gap_analysis.sql
ROLLBACK; -- Demo leaves no schema/data behind, even on repeat runs.

# Week 1 — Ten PostgreSQL queries

The answer files are numbered below. Schema and sample data are included so results can be reproduced rather than inferred from screenshots. Data is synthetic. SQL was tested against local PostgreSQL; see [validation](../VALIDATION.md).

1. [department salary summary](01_department_salary_summary.sql)
2. [second highest salary](02_second_highest_salary.sql)
3. [above department average](03_above_department_average.sql)
4. [manager team salary](04_manager_team_salary.sql)
5. [top project contributors](05_top_project_contributors.sql)
6. [departments without projects](06_departments_without_projects.sql)
7. [running order revenue](07_running_order_revenue.sql)
8. [customer order classification](08_customer_order_classification.sql)
9. [consecutive monthly orders](09_consecutive_monthly_orders.sql)
10. [salary gap analysis](10_salary_gap_analysis.sql)

## Run

Use PostgreSQL with `psql` on PATH and a database where you can create a temporary test schema. For example, create a dedicated empty database once:

```bash
createdb qn_week1
psql -X -v ON_ERROR_STOP=1 -d qn_week1 -f week-1/SQL/run_all.sql
WEEK1_DATABASE_URL='dbname=qn_week1' python3 -m unittest discover -s week-1/SQL/tests -v
```

Use your normal PostgreSQL authentication settings if your server requires host/user/password configuration. Do not commit passwords. `run_all.sql` creates `week1_demo` inside a transaction and rolls it back; it fails rather than overwriting an existing schema with that name. Tests use unique schemas and roll back every run. No permanent schema/table deletion is performed.

## Interpretation

- Q1 includes empty departments; salary aggregates are NULL when no employee exists. Salaries themselves are NOT NULL in this fixture schema.
- Q2 selects the second distinct salary and returns every tie; departments with one distinct salary yield no row.
- Q3 compares the exact average, rounding only its display.
- Q4 considers direct reports and at least two reports, matching the reference.
- Q5 uses the top two distinct hour totals, including ties. One row per employee/project stores the aggregate hours.
- Q6 follows the reference's actual query: departments with employees and no projects. The phrase “active projects” assumes all rows in `projects` are active; there is no invented project-status column. If the instructor supplies a status field, adjust the predicate explicitly.
- Q7 includes completed orders only, grouped by calendar date. It does not generate zero-revenue dates.
- Q8 includes customers appearing in Orders, even if they have no completed order. Thresholds are 100000/50000/20000. A Customers table was not supplied, so customers with no order at all are outside this query.
- Q9 includes any order status, matching the reference, and requires at least three consecutive calendar months. Duplicate orders in a month do not count twice.
- Q10 returns all tied highest/lowest earners in nonempty departments, with deterministic name ordering.

The schema is reconstructed from columns used in the reference, not an official assignment schema. [schema.sql](schema.sql), [seed.sql](seed.sql), [expected demo output](sample-output.txt) and [tests](tests/test_sql.py) make those choices reviewable.

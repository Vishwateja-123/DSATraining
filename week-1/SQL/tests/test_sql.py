"""Run with standard libpq variables (PGDATABASE/PGSERVICE, PGHOST, PGPORT).
Each query runs inside a new schema in a transaction rolled back on completion.
Requires psql on PATH; Python has no third-party dependencies.
"""
import json
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
import uuid

ROOT = Path(__file__).parents[1]



def run_psql(script):
    # Use standard libpq environment/service settings and .pgpass credentials.
    # No connection settings appear in argv or failure messages.
    env = dict(os.environ, PGCONNECT_TIMEOUT="10")
    try:
        result = subprocess.run(["psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=1"],
                                input=script, text=True, capture_output=True,
                                env=env, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        raise RuntimeError("Database check could not run; verify local connection settings") from None
    if result.returncode:
        raise RuntimeError("Database check failed; verify schema and local connection settings")
    return result


def query(number, seed=True):
    if not (os.environ.get("PGDATABASE") or os.environ.get("PGSERVICE")):
        raise RuntimeError("Set PGDATABASE or PGSERVICE before running SQL tests")
    sql = next(ROOT.glob(f"{number:02}_*.sql")).read_text().strip().rstrip(";")
    schema = f"test_{uuid.uuid4().hex}"
    script = f"BEGIN; CREATE SCHEMA {schema}; SET LOCAL search_path TO {schema};"
    script += (ROOT / "schema.sql").read_text()
    if seed:
        script += (ROOT / "seed.sql").read_text()
    script += f"\nSELECT COALESCE(json_agg(result), '[]'::json) FROM (\n{sql}\n) result;\nROLLBACK;"
    result = run_psql(script)
    return json.loads(result.stdout.strip())


class SqlTests(unittest.TestCase):
    def test_connection_failure_does_not_expose_dsn(self):
        secret = "postgresql://user:example-secret@localhost/db"
        result = subprocess.CompletedProcess([], 1, "", secret)
        with patch.dict(os.environ, {"PGPASSWORD": secret}):
            with patch("subprocess.run", return_value=result) as run:
                with self.assertRaises(RuntimeError) as error:
                    run_psql("SELECT 1")
                self.assertNotIn(secret, str(error.exception))
                self.assertNotIn(secret, str(run.call_args.args))
                self.assertEqual(run.call_args.kwargs["env"]["PGPASSWORD"], secret)

    def test_schema_rejects_self_manager(self):
        schema = "test_" + uuid.uuid4().hex
        script = f"BEGIN; CREATE SCHEMA {schema}; SET LOCAL search_path TO {schema};"
        script += (ROOT / "schema.sql").read_text()
        script += """
        INSERT INTO departments VALUES (99, 'Test');
        DO $$ BEGIN
          BEGIN
            INSERT INTO employees VALUES (99, 'Test', 99, 1, 99);
            RAISE EXCEPTION 'self manager was accepted';
          EXCEPTION WHEN check_violation THEN NULL;
          END;
        END $$;
        ROLLBACK;
        """
        run_psql(script)

    def test_01_summary_includes_empty_department(self):
        rows = query(1)
        self.assertEqual([(r['dept_id'], r['employee_count'], r['avg_salary'], r['min_salary'], r['max_salary']) for r in rows],
                         [(1,4,75,40,100),(2,2,60,60,60),(3,0,None,None,None),(4,2,60,30,90),(5,1,50,50,50)])

    def test_02_second_distinct_ties(self):
        self.assertEqual([(r['emp_id'],r['salary']) for r in query(2)], [(2,80),(3,80),(8,30)])

    def test_03_department_average(self):
        self.assertEqual([(r['emp_id'],r['dept_avg_salary']) for r in query(3)], [(1,75),(2,75),(3,75),(7,60)])

    def test_04_direct_reports_minimum_two(self):
        rows = query(4)
        self.assertEqual([(r['manager_id'],r['direct_report_count'],r['total_team_salary'],r['manager_salary']) for r in rows], [(1,3,200,100)])

    def test_05_contributor_ties_and_single_contributor(self):
        self.assertEqual([(r['project_id'],r['emp_id'],r['contributor_rank']) for r in query(5)], [(1,2,1),(1,3,1),(1,1,2),(2,1,1)])

    def test_06_employees_but_no_projects(self):
        self.assertEqual([r['dept_id'] for r in query(6)], [2,5])

    def test_07_completed_only_and_same_day_aggregation(self):
        self.assertEqual([(r['order_date'],r['daily_revenue'],r['cumulative_revenue']) for r in query(7)],
                         [('2025-11-01',10000,10000),('2025-11-02',1,10001),('2025-12-01',5000,15001),('2026-01-01',55000,70001),('2026-01-02',100001,170002)])

    def test_08_tier_boundaries_and_no_completed_orders(self):
        self.assertEqual([(r['customer_id'],r['total_completed_value'],r['customer_tier']) for r in query(8)],
                         [(103,100000,'PLATINUM'),(102,50000,'GOLD'),(101,20000,'SILVER'),(105,2,'BRONZE'),(104,0,'BRONZE'),(106,0,'BRONZE')])

    def test_09_year_boundary_gap_duplicates_all_statuses(self):
        self.assertEqual([r['customer_id'] for r in query(9)], [101,106])

    def test_10_gap_tied_extremes_and_single_employee(self):
        self.assertEqual([(r['dept_id'],r['highest_paid_employees'],r['lowest_paid_employees'],r['salary_difference']) for r in query(10)],
                         [(1,'Asha','Dev',60),(2,'Esha, Farah','Esha, Farah',0),(4,'Gita','Hari',60),(5,'Ira','Ira',0)])

    def test_empty_tables_all_ten_queries(self):
        for number in range(1, 11):
            with self.subTest(query=number):
                self.assertEqual(query(number, seed=False), [])


if __name__ == "__main__":
    unittest.main()

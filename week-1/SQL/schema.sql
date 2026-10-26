-- PostgreSQL. Use an isolated schema (run_all.sql creates one transactionally).
CREATE TABLE departments (dept_id integer PRIMARY KEY, dept_name text NOT NULL);
CREATE TABLE employees (
    emp_id integer PRIMARY KEY, emp_name text NOT NULL,
    dept_id integer NOT NULL REFERENCES departments,
    salary numeric(12,2) NOT NULL CHECK (salary >= 0),
    manager_id integer REFERENCES employees
);
CREATE TABLE projects (
    project_id integer PRIMARY KEY, project_name text NOT NULL,
    dept_id integer NOT NULL REFERENCES departments
);
CREATE TABLE employee_projects (
    project_id integer REFERENCES projects, emp_id integer REFERENCES employees,
    hours_worked numeric(10,2) NOT NULL CHECK (hours_worked >= 0),
    PRIMARY KEY (project_id, emp_id)
);
CREATE TABLE orders (
    order_id integer PRIMARY KEY, customer_id integer NOT NULL,
    order_date date NOT NULL, amount numeric(12,2) NOT NULL CHECK (amount >= 0),
    status text NOT NULL CHECK (status IN ('Completed', 'Pending', 'Cancelled'))
);

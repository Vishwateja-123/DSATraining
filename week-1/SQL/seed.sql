-- Synthetic data; no real employee or customer records.
INSERT INTO departments VALUES (1,'Engineering'),(2,'HR'),(3,'Empty'),(4,'Sales'),(5,'Support');
INSERT INTO employees VALUES
 (1,'Asha',1,100,NULL),(2,'Bala',1,80,1),(3,'Chitra',1,80,1),(4,'Dev',1,40,1),
 (5,'Esha',2,60,NULL),(6,'Farah',2,60,5),(7,'Gita',4,90,NULL),(8,'Hari',4,30,7),
 (9,'Ira',5,50,NULL);
INSERT INTO projects VALUES (1,'Judge',1),(2,'Dashboard',1),(3,'Sales portal',4);
INSERT INTO employee_projects VALUES (1,1,10),(1,2,20),(1,3,20),(1,4,5),(2,1,0);
INSERT INTO orders VALUES
 (1,101,'2025-11-01',10000,'Completed'),(2,101,'2025-12-01',5000,'Completed'),
 (3,101,'2026-01-01',5000,'Completed'),(4,101,'2026-01-20',999,'Cancelled'),
 (5,102,'2026-01-01',50000,'Completed'),(6,103,'2026-01-02',100000,'Completed'),
 (7,104,'2026-01-03',999999,'Pending'),(8,105,'2025-11-02',1,'Completed'),
 (9,105,'2026-01-02',1,'Completed'),(10,106,'2025-11-03',9,'Cancelled'),
 (11,106,'2025-12-03',9,'Pending'),(12,106,'2026-01-03',9,'Pending');

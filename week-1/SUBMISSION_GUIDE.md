# Practical submission guide

## 1. Review what is new

This work fills the gaps against the requested Varun Suddala week-1 reference: ten DSA solutions, ten SQL answers, parking-lot LLD and coding-assessment HLD. Earlier training is preserved unchanged. New material was prepared with AI assistance; read and understand it before presenting it as your internship submission.

The original official question sheet was not supplied. SQL Q6 and Q9 assumptions are explicit in the SQL README. If the instructor's actual schema/prompt differs, adjust those specific answers rather than silently claiming an exact rubric match.

## 2. Run the demonstrations

From this repository root:

```bash
python3 -m unittest discover -s week-1/DSA/tests -v
python3 -m unittest discover -s week-1/LLD/tests -v
python3 week-1/LLD/demo.py
```

Expected: 13 DSA tests and 15 LLD tests pass. The parking demo prints INR 60 for three hourly car hours and INR 65 for four tiered car hours, followed by rejected invalid operations and occupancy.

With a dedicated PostgreSQL database available:

```bash
psql -X -v ON_ERROR_STOP=1 -d qn_week1 -f week-1/SQL/run_all.sql
PGDATABASE=qn_week1 python3 -m unittest discover -s week-1/SQL/tests -v
```

Expected: 13 SQL tests pass, including ten populated-query assertions and an empty-table check for all ten queries. Follow the SQL README for initial database setup.

## 3. Explain the work

- DSA: show a normal and edge case, then explain time/space complexity and why the algorithm works.
- SQL: show the schema, explain ties and order statuses, then compare actual query results to the synthetic fixture expectations.
- LLD: demonstrate allocation, exit fees, full capacity, duplicate plate, invalid ticket and a failed exit that leaves state intact. Explain Strategy, the vehicle factory method and the process lock.
- HLD: follow the design walkthrough in the separate HLD repository; distinguish design targets from measured results.

## 4. Publish reviewed versions

Review each repository's proposed changes before merging into main. Use ordinary merge commits or squash merges for the new branch without rewriting existing main history. Verify that the preserved training files still open and that the new diagrams render on GitHub.

After merge, submission links are:

- DSA/SQL/LLD and index: https://github.com/Vishwateja-123/DSATraining/tree/main/week-1
- HLD: https://github.com/Vishwateja-123/HLD/tree/main/week-1/HLD

Until merge, use the review branch links rather than claiming these new folders exist on main:

- https://github.com/Vishwateja-123/DSATraining/tree/organize/week-1-review/week-1
- https://github.com/Vishwateja-123/HLD/tree/organize/week-1-review/week-1/HLD

## 5. Reconcile the official tracker

Find your own entry in the official tracker before editing; rows may move. Keep student identifiers and tracker progress details in the private tracker, not in this public repository.

After reviewing this new work and confirming it satisfies the internship's criteria, proposed values are DSA **10**, SQL **10**, HLD **Completed**, LLD **Completed**, and the DSATraining weekly index link (which links to HLD). These are proposed updates, not a claim of teacher approval. Preserve existing values until this review is complete. Update only your own row; do not modify classmates' entries. The tracker has not been edited by this preparation step.

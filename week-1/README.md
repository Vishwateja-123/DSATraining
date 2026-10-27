# Week 1 — Internship submission

**Paidipelly Vishwateja**

| Area | Deliverable | Local validation |
| --- | --- | --- |
| [DSA](DSA/README.md) | 10 numbered Python solutions | Examples, edge cases and independent small-input checks |
| [SQL](SQL/README.md) | 10 numbered PostgreSQL queries | Real PostgreSQL fixtures and expected-result assertions |
| [LLD](LLD/README.md) | Multi-floor parking lot, UML and demo | Lifecycle, pricing, validation and concurrent capacity tests |
| [HLD](HLD/README.md) | Coding assessment platform in HLD repository | Design coverage checklist and API/architecture consistency review |

## Practical demonstration

From the DSATraining repository root:

```bash
python3 -m unittest discover -s week-1/DSA/tests -v
python3 -m unittest discover -s week-1/LLD/tests -v
python3 week-1/LLD/demo.py
```

For SQL, follow the [database setup instructions](SQL/README.md); the demo and tests use transaction-scoped schemas and roll back their synthetic data. Present HLD directly from its GitHub README and diagram.

## What changed

Earlier root files were practice material, not a complete match for the weekly tasks. They remain unchanged under [training](../training/README.md). New solutions/designs were prepared with AI assistance to cover the requested [reference checklist](https://github.com/VarunSuddala/QuantumNique-weekly-tasks/tree/a38d74d391bd5f4d013be8c32277799f13e7e28e/week-1). No original assignment sheet was available; task-specific interpretations are documented in each area.

The tracker previously showed DSA 7 and SQL 7, with HLD/LLD blank. This work does not retrospectively validate those counts. After reviewing the new work and publishing the approved versions, reconcile the tracker using the submission links and the internship's completion rules.

See [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md) for the review-to-submission steps.

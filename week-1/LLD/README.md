# Week 1 — Multi-floor parking lot LLD

Python 3.10+, standard library only. The runnable application supports floors/slots, bikes/cars/trucks, compatible-slot allocation, tickets, hourly/tiered fees, unparking, free-slot display and per-floor occupancy.

From the repository root:

```bash
python3 week-1/LLD/demo.py
python3 -m unittest discover -s week-1/LLD/tests -v
```

See [sample output](sample-output.txt), [class diagram and design](docs/design.md) and the [source package](parking_lot/).

## Behavior

- Match vehicle type exactly; a bike cannot silently consume a truck slot.
- Default allocation is lowest floor, then lexicographic slot ID. Highest-floor allocation is interchangeable.
- Plates are trimmed and uppercased before duplicate detection.
- Tickets returned to callers are immutable; free-slot views are copies.
- Charges use `Decimal` in illustrative INR. Partial hours round up, with a one-hour minimum. Hourly rates: bike 10, car 20, truck 50. Tiered pricing uses those first-hour rates and 5/15/35 per subsequent hour.
- Pricing is chosen when the ticket is issued; switching strategy affects future tickets, not existing ones.
- Exit timestamps must be timezone-aware and no earlier than entry. Fee calculation succeeds before any slot is released. A failed exit leaves the ticket and occupancy unchanged.
- Unknown/already-closed tickets, duplicate floors/slots, unsupported types, empty plates and full compatible capacity are rejected.
- A single process lock makes allocation/release atomic across threads. It is not a multi-server database transaction.

## Scope

This is an in-memory LLD exercise with executable behavior, not a deployed parking/payment service. Restarting loses state; no real payments are taken. Production extensions would need persistent storage, transactions/unique constraints across gates, recovery, authenticated operators and an immutable pricing/version table.

The task coverage and structure follow Varun Suddala's reference. This implementation and its tests were newly prepared with AI assistance; they do not copy his source files.

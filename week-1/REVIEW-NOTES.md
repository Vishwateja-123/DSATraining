# Review follow-up — 27 October 2026

The following responses were independently checked against the code/design. HLD remains a design exercise, not a deployed implementation. Old GitHub comments may remain visible after these changes.

- [🟡 Medium · Database credentials leak on test failure](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226419): Runner uses standard libpq environment/service settings, no connection arguments, and sanitized failure messages; regression test added.

- [🟡 Medium · Student identifier exposed](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226427): Removed tracker identifier, row and progress from current public guide. Existing commit history is retained; this does not erase earlier versions. Public author name remains intentional attribution for the user's own submission.

- [🟡 Medium · Bad allocator corrupts occupied slots](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226430): Allocator receives detached candidates and must return an unchanged member; invalid results cannot alter live occupancy.

- [🟡 Medium · Valid DST exits are rejected](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226436): Entry and exit are normalized to UTC; repeated-hour regression added.

- [🟡 Medium · Parked tickets use changed rates](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226439): Pricing is privately deep-copied per ticket before state changes; built-in rate dictionaries are instance configuration. Custom strategies must honor the documented copy-safe contract.

- [🟡 Medium · Parking fees use wrong elapsed time](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226443): Fee arithmetic uses UTC elapsed time; spring and fall transition regressions added.

- [🟡 Medium · One-shot inputs lose their values](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226449): Intervals and coins are materialized once; one-shot iterator regression added.

- [🟡 Medium · Fractional indices raise wrong error](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226457): Non-integer indices raise IndexError before state access.

- [🟡 Medium · Boolean values pass as numbers](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226459): Boolean floor, amount and denomination inputs are explicitly rejected.

- [🟡 Medium · Employees can manage themselves](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226462): Schema rejects direct self-management; database regression added. Multi-employee managerial cycles are outside this exercise's schema constraints.

- [🟡 Medium · Falsey strategies are ignored](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226471): Constructor distinguishes None from falsey strategies; regression added.

- [⚪ Low · Preservation audit overcounts files](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226475): Clarified nine files across both repositories: eight DSATraining files plus the HLD PDF.

- [🟡 Medium · Failed fee can lose ticket](https://github.com/Vishwateja-123/DSATraining/pull/1#discussion_r4384226477): Failed-fee test now verifies duplicate plate rejection, successful retry, and reuse after exit.



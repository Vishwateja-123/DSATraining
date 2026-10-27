# Week 1 — Ten DSA problems

Python 3.10+, no dependencies. Run any numbered file directly for its example, or run all tests from the repository root:

```bash
python3 -m unittest discover -s week-1/DSA/tests -v
python3 week-1/DSA/01_longest_subarray_sum_k.py
```

| # | Problem | Approach | Time | Extra space |
| --- | --- | --- | --- | --- |
| 01 | [Longest subarray with sum K](01_longest_subarray_sum_k.py) | Prefix sum + earliest index | O(n) | O(n) |
| 02 | [Minimum window substring](02_minimum_window.py) | Sliding window with character counts | O(s+t) | O(distinct target characters) |
| 03 | [Merge intervals](03_merge_intervals.py) | Sort then merge | O(n log n) | O(n) |
| 04 | [Kth largest in a stream](04_kth_largest_stream.py) | Min-heap of k largest values | O(log k) per arrival | O(k) |
| 05 | [Detect and remove linked-list cycle](05_cycle_linked_list.py) | Floyd cycle detection | O(n) | O(1) |
| 06 | [Lowest common ancestor](06_lca_binary_tree.py) | Iterative parent map | O(n) | O(n) |
| 07 | [Shortest path in binary matrix](07_binary_matrix_bfs.py) | Breadth-first search | O(n²) | O(n²) |
| 08 | [Course ordering](08_course_order.py) | Kahn topological sort | O(V+E) | O(V+E) |
| 09 | [Minimum coins](09_minimum_coins.py) | Bottom-up dynamic programming | O(amount × coins) | O(amount) |
| 10 | [Range maximum segment tree](10_segment_tree.py) | Iterative segment tree | O(n) build; O(log n) query/update | O(n) |

## Reasoning and assumptions

**01. Longest subarray with sum K:** Store first position of each prefix sum; retaining a later index would shorten a valid answer.

**02. Minimum window substring:** Count missing occurrences, including duplicates; shrink only while all are present.

**03. Merge intervals:** Sorted starts let the last merged interval absorb every overlapping next interval.

**04. Kth largest in a stream:** The smallest of the retained k values is the kth largest; duplicates count.

**05. Detect and remove linked-list cycle:** After a meeting, locate the cycle entry and cut only its predecessor link.

**06. Lowest common ancestor:** Collect ancestors of one target and walk the other upward; both must exist.

**07. Shortest path in binary matrix:** Every move costs one; the first time the destination is dequeued is shortest.

**08. Course ordering:** Only zero-indegree nodes can be scheduled; an incomplete output means a cycle.

**09. Minimum coins:** A last coin reduces the problem to an already-computed smaller subtotal.

**10. Range maximum segment tree:** Each node is the maximum of its children; use negative infinity as the identity.

Intervals are closed, so touching endpoints merge; input remains unchanged. The stream returns `None` until k values arrive. LCA uses node identity and returns `None` for an absent target; its iterative implementation supports deep trees. Binary matrix paths allow eight directions and count cells, including the start. Course pairs are `[course, prerequisite]`; duplicate edges are ignored. Coin supply is unlimited and denominations must be positive integers. Segment-tree queries use inclusive zero-based endpoints and invalid ranges raise `IndexError`.

Tests compare small cases with independent algorithms: brute-force windows/intervals, sorted stream prefixes, distance relaxation for matrix paths, permutations for course orders, BFS for coins and a plain array for segment trees. Linked-list checks preserve the identity and order of every node. Test success is evidence for these contracts, not proof for every possible input.

## Baseline approaches

The reference presents simple and optimized approaches. The first three problems and cycle removal include executable baseline functions; other simple approaches are documented in module docstrings and implemented independently as test oracles where practical. LCA's path comparison is a straightforward baseline; DFS over all simple matrix paths and recursive coin enumeration are exponential and intentionally not the default execution path.

Task scope follows Varun Suddala's week-1 reference; solutions were freshly prepared with AI assistance. Earlier practice snippets remain in `training/` unchanged.

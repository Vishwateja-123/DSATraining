"""Deterministic examples, edge cases and independent small-input oracles."""
import importlib.util
import itertools
import random
import unittest
from collections import deque
from pathlib import Path


def load(number):
    path = next(Path(__file__).parents[1].glob(f"{number:02}_*.py"))
    spec = importlib.util.spec_from_file_location(f"problem_{number}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DsaTests(unittest.TestCase):
    def test_iterators_and_invalid_numeric_inputs(self):
        self.assertEqual(load(3).merge_intervals(iter([[1, 3], [2, 4]])), [[1, 4]])
        coins = load(9).min_coins_for_amount
        self.assertEqual(coins(iter([1, 2, 5]), 11), 3)
        for values, amount in [([True], 1), ([1], True), ([False, 2], 2)]:
            with self.assertRaises(ValueError):
                coins(values, amount)
        tree = load(10).SegmentTreeRangeMax([2, 4])
        for value in [0.5, True, "0", None]:
            with self.assertRaises(IndexError):
                tree.update(value, 9)
            with self.assertRaises(IndexError):
                tree.query(value, 1)
            with self.assertRaises(IndexError):
                tree.query(0, value)
        self.assertEqual(tree.query(0, 1), 4)

    def test_longest_subarray_exhaustive(self):
        m = load(1)
        for n in range(6):
            for values in itertools.product((-1, 0, 1), repeat=n):
                for k in (-2, 0, 2):
                    self.assertEqual(m.longest_subarray_sum_k(values, k), m.brute_force(values, k))

    def test_minimum_window_duplicates_empty_and_ties(self):
        m = load(2)
        self.assertEqual(m.min_window("ADOBECODEBANC", "ABC"), "BANC")
        for n in range(6):
            for chars in itertools.product("ab", repeat=n):
                s = "".join(chars)
                for t in ("", "a", "aa", "ab", "aba", "c"):
                    self.assertEqual(m.min_window(s, t), m.brute_force(s, t))

    def test_intervals_randomized_and_input_preserved(self):
        m, rng = load(3), random.Random(103)
        for _ in range(150):
            pairs = [sorted([rng.randrange(-5, 6), rng.randrange(-5, 6)]) for _ in range(rng.randrange(10))]
            saved = [x[:] for x in pairs]
            self.assertEqual(m.merge_intervals(pairs), m.brute_force(pairs))
            self.assertEqual(pairs, saved)
        with self.assertRaises(ValueError):
            m.merge_intervals([[3, 1]])

    def test_stream_against_sorted_prefix(self):
        m, rng = load(4), random.Random(104)
        for k in (1, 3, 20):
            stream, values = m.KthLargestStream(k), []
            for _ in range(100):
                value = rng.randrange(-10, 11)
                values.append(value)
                expected = sorted(values, reverse=True)[k - 1] if len(values) >= k else None
                self.assertEqual(stream.add(value), expected)
        for k in (0, -1, 1.5):
            with self.assertRaises(ValueError):
                m.KthLargestStream(k)

    def test_cycle_every_entry_and_no_cycle(self):
        m = load(5)
        self.assertIsNone(m.detect_and_remove_cycle(None))
        for n in range(1, 20):
            for entry in range(-1, n):
                nodes = [m.ListNode(i) for i in range(n)]
                for a, b in zip(nodes, nodes[1:]):
                    a.next = b
                if entry >= 0:
                    nodes[-1].next = nodes[entry]
                node = m.detect_and_remove_cycle(nodes[0])
                for expected in nodes:
                    self.assertIs(node, expected)
                    node = node.next
                self.assertIsNone(node)

    def test_lca_identity_missing_and_same_target(self):
        m = load(6)
        a, b, c = m.TreeNode(1), m.TreeNode(1), m.TreeNode(2)
        root = m.TreeNode(0, a, b)
        a.left = c
        self.assertIs(m.lowest_common_ancestor(root, c, b), root)
        self.assertIs(m.lowest_common_ancestor(root, a, c), a)
        self.assertIs(m.lowest_common_ancestor(root, c, c), c)
        self.assertIsNone(m.lowest_common_ancestor(root, a, m.TreeNode(1)))
        self.assertIsNone(m.lowest_common_ancestor(None, a, b))

    def test_lca_deep_tree(self):
        m = load(6)
        nodes = [m.TreeNode(i) for i in range(2000)]
        for a, b in zip(nodes, nodes[1:]):
            a.right = b
        self.assertIs(m.lowest_common_ancestor(nodes[0], nodes[1500], nodes[-1]), nodes[1500])

    def test_bfs_against_distance_relaxation(self):
        m = load(7)
        for bits in itertools.product((0, 1), repeat=9):
            grid = [list(bits[i:i + 3]) for i in (0, 3, 6)]
            distances = {(0, 0): 1} if grid[0][0] == 0 else {}
            # Independent Bellman-Ford style relaxation on the tiny grid.
            for _ in range(9):
                for r in range(3):
                    for c in range(3):
                        if grid[r][c]:
                            continue
                        near = [d for (a, b), d in distances.items() if max(abs(a-r), abs(b-c)) == 1]
                        if near:
                            distances[r, c] = min(distances.get((r, c), 100), min(near) + 1)
            self.assertEqual(m.shortest_path_binary_matrix(grid), distances.get((2, 2), -1))
            self.assertEqual([x for row in grid for x in row], list(bits))
        self.assertEqual(m.shortest_path_binary_matrix([]), -1)
        self.assertEqual(m.shortest_path_binary_matrix([[0]]), 1)
        with self.assertRaises(ValueError):
            m.shortest_path_binary_matrix([[0, 0]])

    def test_course_order_against_permutations(self):
        m, rng = load(8), random.Random(108)
        for n in range(1, 6):
            for _ in range(25):
                edges = [(a, b) for a in range(n) for b in range(n) if rng.random() < 0.2]
                possible = any(all(p.index(b) < p.index(a) for a, b in edges) for p in itertools.permutations(range(n)))
                result = m.find_course_order(n, edges + edges)
                self.assertEqual(bool(result), possible)
                if result:
                    self.assertEqual(set(result), set(range(n)))
                    self.assertTrue(all(result.index(b) < result.index(a) for a, b in edges))
        self.assertEqual(m.find_course_order(0, []), [])
        with self.assertRaises(ValueError):
            m.find_course_order(2, [[0, 2]])

    def test_coins_against_bfs(self):
        m = load(9)
        for coins in ([], [1], [2], [1, 3, 4], [2, 5, 7], [2, 2]):
            for amount in range(35):
                queue, seen, expected = deque([(0, 0)]), {0}, -1
                while queue:
                    total, count = queue.popleft()
                    if total == amount:
                        expected = count
                        break
                    for coin in coins:
                        if total + coin <= amount and total + coin not in seen:
                            seen.add(total + coin)
                            queue.append((total + coin, count + 1))
                self.assertEqual(m.min_coins_for_amount(coins, amount), expected)
        for coins, amount in [([0], 2), ([-1], 2), ([1], -1)]:
            with self.assertRaises(ValueError):
                m.min_coins_for_amount(coins, amount)

    def test_segment_tree_randomized_updates_and_ranges(self):
        m, rng = load(10), random.Random(110)
        for n in range(1, 30):
            values = [rng.randrange(-100, 1) for _ in range(n)]
            tree = m.SegmentTreeRangeMax(values)
            for _ in range(100):
                if rng.random() < 0.5:
                    i, value = rng.randrange(n), rng.randrange(-100, 101)
                    values[i] = value
                    tree.update(i, value)
                else:
                    left, right = sorted((rng.randrange(n), rng.randrange(n)))
                    self.assertEqual(tree.query(left, right), max(values[left:right + 1]))

    def test_segment_tree_invalid_ranges(self):
        m = load(10)
        for values in ([], [1, 2]):
            tree = m.SegmentTreeRangeMax(values)
            for left, right in ((-1, 0), (1, 0), (0, len(values))):
                with self.assertRaises(IndexError):
                    tree.query(left, right)
            with self.assertRaises(IndexError):
                tree.update(len(values), 4)


if __name__ == "__main__":
    unittest.main()

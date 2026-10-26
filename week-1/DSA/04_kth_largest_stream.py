"""Kth largest with duplicates counted; None until k arrivals.
Min-heap retains largest k values: O(log k) per add, O(k) space.
Baseline: retain and sort all arrivals, O(n log n) per query.
"""
import heapq


class KthLargestStream:
    def __init__(self, k):
        if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
            raise ValueError("k must be a positive integer")
        self.k = k
        self.heap = []

    def add(self, value):
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, value)
        elif value > self.heap[0]:
            heapq.heapreplace(self.heap, value)
        return self.heap[0] if len(self.heap) == self.k else None


if __name__ == "__main__":
    stream = KthLargestStream(3)
    print([stream.add(x) for x in [4, 5, 8, 2, 3]])  # None None 4 4 4

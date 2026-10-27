"""Inclusive range maximum queries and point replacement updates.
Build O(n), update/query O(log n), space O(n). Invalid indices raise IndexError.
Baseline: replace in an array O(1), take max of a slice O(n).
"""
class SegmentTreeRangeMax:
    def __init__(self, nums):
        self.n = len(nums)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [float("-inf")] * (2 * self.size)
        self.tree[self.size:self.size + self.n] = nums
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index, value):
        if type(index) is not int or not 0 <= index < self.n:
            raise IndexError("Update index outside array")
        index += self.size
        self.tree[index] = value
        index //= 2
        while index:
            self.tree[index] = max(self.tree[2 * index], self.tree[2 * index + 1])
            index //= 2

    def query(self, left, right):
        if type(left) is not int or type(right) is not int or not 0 <= left <= right < self.n:
            raise IndexError("Invalid inclusive query range")
        left, right = left + self.size, right + self.size
        result = float("-inf")
        while left <= right:
            if left % 2:
                result = max(result, self.tree[left])
                left += 1
            if not right % 2:
                result = max(result, self.tree[right])
                right -= 1
            left //= 2
            right //= 2
        return result


if __name__ == "__main__":
    tree = SegmentTreeRangeMax([-5, 3, 1, 7])
    print(tree.query(0, 2))  # 3
    tree.update(1, -2)
    print(tree.query(0, 2))  # 1

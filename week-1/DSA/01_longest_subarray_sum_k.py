"""Longest contiguous subarray summing to k; negatives and zero are allowed.
Prefix sums: O(n) time and O(n) space. Return 0 if no nonempty match.
"""
def longest_subarray_sum_k(nums, k):
    first = {0: -1}
    total = best = 0
    for end, value in enumerate(nums):
        total += value
        if total - k in first:
            best = max(best, end - first[total - k])
        first.setdefault(total, end)  # Earliest index gives the longest window.
    return best


def brute_force(nums, k):
    best = 0
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):
            total += nums[end]
            if total == k:
                best = max(best, end - start + 1)
    return best


if __name__ == "__main__":
    print(longest_subarray_sum_k([1, -1, 5, -2, 3], 3))  # 4

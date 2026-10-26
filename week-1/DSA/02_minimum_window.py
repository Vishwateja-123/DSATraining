"""Shortest substring covering all target characters, including repetitions.
Return earliest minimum on ties, or empty string if absent/target empty.
Sliding window: O(len(s)+len(t)) time, O(distinct target chars) space.
"""
from collections import Counter


def min_window(s, t):
    if not t:
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best_start, best_length = 0, len(s) + 1
    for right, char in enumerate(s):
        if char in need:
            missing -= need[char] > 0
            need[char] -= 1
        while missing == 0:
            if right - left + 1 < best_length:
                best_start, best_length = left, right - left + 1
            old = s[left]
            if old in need:
                need[old] += 1
                missing += need[old] > 0
            left += 1
    return "" if best_length > len(s) else s[best_start:best_start + best_length]


def brute_force(s, t):
    if not t:
        return ""
    target = Counter(t)
    best = ""
    for i in range(len(s)):
        counts = Counter()
        for j in range(i, len(s)):
            counts[s[j]] += 1
            if all(counts[c] >= n for c, n in target.items()):
                if not best or j - i + 1 < len(best):
                    best = s[i:j + 1]
                break
    return best


if __name__ == "__main__":
    print(min_window("ADOBECODEBANC", "ABC"))  # BANC

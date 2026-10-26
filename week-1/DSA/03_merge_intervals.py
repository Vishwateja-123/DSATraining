"""Merge closed intervals, including touching endpoints; leave input unchanged.
Sorting: O(n log n) time, O(n) space. Reject reversed/invalid pairs.
"""
def merge_intervals(intervals):
    if any(len(pair) != 2 or pair[0] > pair[1] for pair in intervals):
        raise ValueError("Each interval must have start <= end")
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def brute_force(intervals):
    pending = [list(pair) for pair in intervals]
    while True:
        for i in range(len(pending)):
            for j in range(i + 1, len(pending)):
                a, b = pending[i], pending[j]
                if max(a[0], b[0]) <= min(a[1], b[1]):
                    pending[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    pending.pop(j)
                    break
            else:
                continue
            break
        else:
            return sorted(pending)


if __name__ == "__main__":
    print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))

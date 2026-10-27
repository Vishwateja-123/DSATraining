"""Shortest 8-direction path in a square 0/1 grid, measured in cells.
Zero is open; return -1 when blocked/empty/unreachable. Input is not mutated.
BFS: O(n squared) time/space. Baseline enumerates simple paths (exponential).
"""
from collections import deque


def shortest_path_binary_matrix(grid):
    n = len(grid)
    if any(len(row) != n or any(v not in (0, 1) for v in row) for row in grid):
        raise ValueError("Expected a square binary matrix")
    if not n or grid[0][0] or grid[-1][-1]:
        return -1
    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}
    while queue:
        row, col, distance = queue.popleft()
        if (row, col) == (n - 1, n - 1):
            return distance
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = row + dr, col + dc
                if (dr or dc) and 0 <= nr < n and 0 <= nc < n:
                    if not grid[nr][nc] and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc, distance + 1))
    return -1


if __name__ == "__main__":
    print(shortest_path_binary_matrix([[0, 1], [1, 0]]))  # 2

"""Order courses with [course, prerequisite] edges; [] if cyclic.
Kahn's algorithm: O(V+E) time/space. Duplicate edges are ignored.
Baseline checks all course permutations (factorial).
"""
from collections import deque


def find_course_order(num_courses, prerequisites):
    if num_courses < 0:
        raise ValueError("Course count must be nonnegative")
    edges = [[] for _ in range(num_courses)]
    seen = set()
    indegree = [0] * num_courses
    for course, prerequisite in prerequisites:
        if not 0 <= course < num_courses or not 0 <= prerequisite < num_courses:
            raise ValueError("Course id outside range")
        if (course, prerequisite) not in seen:
            seen.add((course, prerequisite))
            edges[prerequisite].append(course)
            indegree[course] += 1
    ready = deque(i for i, degree in enumerate(indegree) if degree == 0)
    result = []
    while ready:
        current = ready.popleft()
        result.append(current)
        for child in edges[current]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    return result if len(result) == num_courses else []


if __name__ == "__main__":
    print(find_course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))

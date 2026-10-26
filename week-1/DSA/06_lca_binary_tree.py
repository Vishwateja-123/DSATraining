"""LCA by node identity in a binary tree (not necessarily a BST).
Return None if either target is absent. Iterative parent map avoids recursion
limits: O(n) time/space. Baseline stores both root-to-target paths.
"""
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def lowest_common_ancestor(root, p, q):
    if root is None or p is None or q is None:
        return None
    parents = {root: None}
    stack = [root]
    while stack and (p not in parents or q not in parents):
        node = stack.pop()
        for child in (node.left, node.right):
            if child is not None:
                parents[child] = node
                stack.append(child)
    if p not in parents or q not in parents:
        return None
    ancestors = set()
    while p is not None:
        ancestors.add(p)
        p = parents[p]
    while q not in ancestors:
        q = parents[q]
    return q


if __name__ == "__main__":
    a, b = TreeNode(5), TreeNode(1)
    root = TreeNode(3, a, b)
    print(lowest_common_ancestor(root, a, b).val)  # 3

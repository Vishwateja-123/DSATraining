"""Detect and remove a cycle while preserving every reachable node once.
Floyd: O(n) time, O(1) space. Returns original head. Baseline uses a set.
"""
class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next


def detect_and_remove_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            entry = head
            while entry is not slow:
                entry, slow = entry.next, slow.next
            tail = entry
            while tail.next is not entry:
                tail = tail.next
            tail.next = None
            break
    return head


def brute_force(head):
    seen = set()
    previous, node = None, head
    while node is not None:
        if node in seen:
            previous.next = None
            break
        seen.add(node)
        previous, node = node, node.next
    return head


if __name__ == "__main__":
    a, b = ListNode(1), ListNode(2)
    a.next, b.next = b, a
    detect_and_remove_cycle(a)
    print(a.val, a.next.val, a.next.next)  # 1 2 None

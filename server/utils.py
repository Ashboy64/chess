class LIFO(object):
    """LIFO."""

    def __init__(self):
        super(LIFO, self).__init__()
        self.queue = []

    def push(self, el):
        self.queue.append(el)

    def pop(self):
        return self.queue.pop()

    def contains(self, element, equality_func=None):
        """If equality_func is specified, it will be used to check if anything in queue equals element"""
        if equality_func is None:
            return element in self.queue
        for el in self.queue:
            if equality_func(element, el):
                return True
        return False


def are_equal(a, b):
    """Checks equality between two board states"""
    equal = True
    for r_prev in range(len(a)):
        for c_prev in range(len(a[0])):
            if a[r_prev][c_prev] != b[r_prev][c_prev]:
                equal = False
    return equal

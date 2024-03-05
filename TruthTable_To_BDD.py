class Node:
    def __init__(self, value=None, low=None, high=None):
        self.value = value
        self.low = low
        self.high = high


def build_bdd(truth_table):
    """
        Constructs a binary decision diagram (BDD) from a given reversible truth table.
    """
    max_input = max(truth_table, key=lambda x: x[0])[0]
    num_bits = len(bin(max_input)) - 2

    memo = {}

    def build_bdd_recursive(table, depth):
        if depth == num_bits:
            return Node(value=table[0][1])

        zeros = tuple((x, y) for x, y in table if (x >> (num_bits - depth - 1)) & 1 == 0)
        ones = tuple((x, y) for x, y in table if (x >> (num_bits - depth - 1)) & 1 == 1)
        if (zeros, ones) in memo:
            return memo[(zeros, ones)]

        node = Node(value=depth)
        if all(y == zeros[0][1] for _, y in zeros):
            node.low = Node(value=zeros[0][1])
        else:
            node.low = build_bdd_recursive(zeros, depth + 1)
        if all(y == ones[0][1] for _, y in ones):
            node.high = Node(value=ones[0][1])
        else:
            node.high = build_bdd_recursive(ones, depth + 1)

        memo[(zeros, ones)] = node
        return node

    return build_bdd_recursive(truth_table, 0)
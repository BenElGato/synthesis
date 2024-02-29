from graphviz import Digraph


class Node:
    def __init__(self, value=None, low=None, high=None):
        self.value = value
        self.low = low
        self.high = high


def build_bdd(truth_table):
    """
        Constructs a binary decision diagram (BDD) from a given reversible truth table.

        Parameters:
        - truth_table: A list of tuples representing the truth table. Each tuple consists of two integers, where the first integer represents the input value and the second integer represents the corresponding output value.

        Returns:
        - The root node of the constructed BDD.

        Description:
        This function takes a reversible truth table and constructs a BDD recursively.
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


def visualize_bdd_with_graphviz(node, num_variables, name = "", depth=0, graph=None):
    """
        Parameters:
        - node: node where the visualization should start
        - num_variables: Number of output varaibles
        - name: Keep default, used for naming the nodes internally
        - depth: start depth
        - graph: Graph object for visualization
        Returns:
        - The graph that represents the binary decission diagram

        Description:
        This function takes a BDD and creates a graph representation for it
    """
    if graph is None:
        graph = Digraph()
    if node.value is not None:
        graph.node(name=name, label=f"x_{depth}")
        if node.low:
            new_name = name + "0"
            visualize_bdd_with_graphviz(node.low, num_variables=num_variables,name=new_name,depth=depth + 1, graph=graph)
            graph.edge(name, new_name, label='0')
        if node.high:
            new_name = name + "1"
            visualize_bdd_with_graphviz(node.high, num_variables=num_variables,name=new_name, depth=depth + 1, graph=graph)
            graph.edge(name, new_name, label='1')
        if not node.low and not node.high:
            graph.node(name=name, label=format(node.value, f'0{num_variables}b'))
    return graph

from enum import Enum
from Gate_Elements import Element

class NODE(Enum):
    INNER_NODE = 2
    ONE = 1
    ZERO = 0
class EDGE(Enum):
    N = 0
    P_DOT = 1
    N_DOT = 2
    P = 3
class QMDD:
    def __init__(self, n:NODE, p_dot:NODE, n_dot:NODE, p:NODE, type:NODE):
        if type == NODE.INNER_NODE:
            self.p_dot = p_dot
            self.n_dot = n_dot
            self.n = n
            self.p = p
            # Variables begin at x1 and end at xn
            self.node_type = type
        elif type == NODE.ONE or type == NODE.ZERO:
            self.node_type = type
            self.p_dot = None
            self.n_dot = None
            self.n = None
            self.p = None
        else:
            raise Exception("Invalid initialization of a QMDD object")
    '''
    Executes the swap operation on a node. Does not adapt the circuit
    '''
    def swap(self, circuit: list, num_variables: int):
        return None
        '''
        if self.node_type == NODE.INNER_NODE:
            safe = self.n
            self.n = self.p_dot
            self.p_dot = safe

            safe = self.n_dot
            self.n_dot = self.p
            self.p = safe

            gate = []
            for i in range(num_variables):
                if i == self.variable:
                    gate.append(Element.FLIP)
                else:
                    gate.append(Element.NULL_GATE)
            circuit.append(gate)
            '''

    '''
    Executes the conditional swap on a node. Does not adapt the circuit
    '''
    def cond_swap(self, edge: EDGE):
        # TODO: What if a child node is a leaf?
        if self.node_type == NODE.INNER_NODE:
            if edge == EDGE.N:
                self.n.swap(circuit)
            elif edge == EDGE.P_DOT:
                self.p_dot.swap(circuit)
            elif edge == EDGE.N_DOT:
                self.n_dot.swap(circuit)
            elif edge == EDGE.P:
                self.p.swap(circuit)
            else:
                raise ValueError("Not a valid Edge object")
    '''
    Executes the shift opearation. shift_right is a bool and determines the direction teh shifting is executed
    '''
    def shift(self, shift_right: bool, circuit: list, num_variables: int):
        if circuit is None:
            raise ValueError("Circuit passed as None!")
        if not (num_variables == len(circuit[0]) or len(circuit) == 0):
            raise ValueError("Circuit does not contain the number of variables as claimed!")

        if self.node_type == NODE.INNER_NODE:
            n_has_paths = self.n.has_vertexes()
            p_dot_has_paths = self.p_dot.has_vertexes()
            n_dot_has_paths = self.n_dot.has_vertexes()
            p_has_paths = self.p.has_vertexes()

            safe_n = self.n
            safe_p_dot = self.p_dot
            safe_n_dot = self.n_dot
            safe_p = self.p

            if shift_right:
                relevant_pos1 = 1
                relevant_pos2 = 3
            else:
                relevant_pos1 = 0
                relevant_pos2 = 2

            if n_has_paths[relevant_pos1] == True or n_has_paths[relevant_pos2 ] == True:
                self.p_dot = safe_n
            if p_dot_has_paths[relevant_pos1] == True or p_has_paths[relevant_pos2 ] == True:
                self.n = safe_p_dot
            if n_dot_has_paths[relevant_pos1] == True or n_dot_has_paths[relevant_pos2 ] == True:
                self.p = safe_n_dot
            if p_has_paths[relevant_pos1] == True or p_has_paths[relevant_pos2 ] == True:
                self.n_dot = safe_p

    '''
    Returns a list of booleans. Every Bool describes if the node has a non Terminal vertex at this position
    --> [Bool n, Bool p_dot, Bool n_dot, Bool p] 
    '''
    def has_vertexes(self):
        if self.node_type == NODE.ONE or self.node_type == NODE.ZERO:
            return [False, False, False, False]
        elif self.node_type == NODE.INNER_NODE:
            bool_n: bool = (self.n.node_type == NODE.INNER_NODE)
            bool_p_dot: bool = (self.p_dot.node_type == NODE.INNER_NODE)
            bool_n_dot: bool = (self.n_dot.node_type == NODE.INNER_NODE)
            bool_p: bool = (self.p.node_type == NODE.INNER_NODE)
            return [bool_n, bool_p_dot, bool_n_dot, bool_p]
        else:
            raise ValueError("Not a valid Node object")
    '''
    Returns a list with the count of 1-paths for each vertex.
    '''
    def get_amount_1_paths(self):
        if self.node_type == NODE.ONE:
            return 1
        elif self.node_type == NODE.ZERO:
            return 0
        else:
            n_count: int = self.n.get_amount_1_paths()
            p_dot_count: int = self.p_dot.get_amount_1_paths()
            n_dot_count: int = self.n_dot.get_amount_1_paths()
            p_count: int = self.p.get_amount_1_paths()
            return n_count + p_count + n_dot_count + p_dot_count
    def get_paths(self):
        if self.node_type == NODE.ONE:
            return [" "]
        elif self.node_type == NODE.ZERO:
            return None
        else:
            n_paths: list = []
            p_paths: list = []
            n_dot_paths: list = []
            p_dot_paths: list = []
            if self.n.node_type is not NODE.ZERO:
                n_paths = self.n.get_paths()
                for i in range(len(n_paths)):
                    path = n_paths[i]
                    if path is not None:
                        path = "N" + path
                        n_paths[i] = path
            if self.p.node_type is not NODE.ZERO:
                p_paths = self.p.get_paths()
                for i in range(len(p_paths)):
                    path = p_paths[i]
                    if path is not None:
                        path = "P" + path
                        p_paths[i] = path
            if self.n_dot.node_type is not NODE.ZERO:
                n_dot_paths = self.n_dot.get_paths()
                for i in range(len(n_dot_paths)):
                    path = n_dot_paths[i]
                    if path is not None:
                        path = "N-" + path
                        n_dot_paths[i] = path
            if self.p_dot.node_type is not NODE.ZERO:
                p_dot_paths = self.p_dot.get_paths()
                for i in range(len(p_dot_paths)):
                    path = p_dot_paths[i]
                    if path is not None:
                        path = "P-" + path
                        p_dot_paths[i] = path
            return n_paths + p_paths + n_dot_paths + p_dot_paths
    '''
    Gets 
    '''
    def get_unique_paths(self):
        pass


    def p1(self, circuit: list, num_variables: int):
        one_paths = self.get_amount_1_paths()
        if one_paths[1] > one_paths[0]:
            circuit = self.swap(circuit, num_variables)
    def p2(self, circuit: list, num_variables: int):
        pass
    def q2(self, circuit: list, variables: int):
        circuit = self.p1(circuit, variables)
        circuit = self.p2(circuit, variables)
        pass

    def qmdd_based_synthesis(self, circuit: list, num_variables: int):
        self.q2(circuit, num_variables)

        self.n = self.n.q2(circuit, num_variables)
        self. p_dot = self.p_dot.q2(circuit, num_variables)
        self.n_dot = self.n_dot.q2(circuit, num_variables)
        self.p = self.p.q2(circuit, num_variables)
        # TODO Rückgabe

circuit = []
num_variables = 2

one = QMDD(None,None,None,None,NODE.ONE)
zero = QMDD(None,None,None,None,NODE.ZERO)


x3_1 = QMDD(zero,one,one,zero,NODE.INNER_NODE)
x3_2 = QMDD(one,zero,zero,one,NODE.INNER_NODE)

x2_1 = QMDD(x3_1,zero,zero,zero, NODE.INNER_NODE)
x2_2 = QMDD(zero, zero, zero, x3_2, NODE.INNER_NODE)
x2_3 = QMDD(x3_2,zero,zero,zero, NODE.INNER_NODE)

x1= QMDD(x2_2,x2_1,x2_3,x2_2, NODE.INNER_NODE)

paths = x1.get_paths()
print(paths)

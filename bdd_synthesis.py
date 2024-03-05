from math import log2

from TruthTable_To_BDD import build_bdd
from Gate_Elements import *
def add_gates_rec(node, num_inputs):
    if isOneLeaf(node) or isZeroLeaf(node):
        return ([], [], [], None)
    if isOneLeaf(node.low):
        if isZeroLeaf(node.high):
            # Base case
            var_lines = add_input_cond([], num_inputs,node.value)
            one_lines = [[Element.FLIP]]
            pointer = (1,0) # Points to where the current output lies --> (tuple_index, pos)
            return (var_lines, one_lines, None, pointer)
        else:
            (var_lines, one_lines, zero_lines, pointer) = add_gates_rec(node.high, num_inputs)
            return case_4(var_lines,one_lines,zero_lines,pointer,num_inputs,node)
    elif isZeroLeaf(node.low):
        if isOneLeaf(node.high):
            # Base case
            var_lines = add_input_cond([], num_inputs, node.value)
            zero_lines = [[Element.FLIP]]
            pointer = (2, 0)  # Points to where the current output lies --> (tuple_index, pos)
            return (var_lines, None, zero_lines, pointer)
        else:
            (var_lines, one_lines, zero_lines, pointer) = add_gates_rec(node.high, num_inputs)
            return case_3(var_lines, one_lines, zero_lines, pointer, num_inputs, node)
    else:
        if isOneLeaf(node.high):
            (var_lines, one_lines, zero_lines, pointer) = add_gates_rec(node.low, num_inputs)
            return case_2(var_lines, one_lines, zero_lines, pointer, num_inputs, node)
        elif isZeroLeaf(node.high):
            (var_lines, one_lines, zero_lines, pointer) = add_gates_rec(node.low, num_inputs)
            return case_1(var_lines, one_lines, zero_lines, pointer, num_inputs, node)
        else:
            (var_lines_low, one_lines_low, zero_lines_low, pointer_low) = add_gates_rec(node.low, num_inputs)
            (var_lines_high, one_lines_high, zero_lines_high, pointer_high) = add_gates_rec(node.high, num_inputs)
            return case_0(var_lines_low, one_lines_low, zero_lines_low, pointer_low,var_lines_high, one_lines_high, zero_lines_high, pointer_high , num_inputs, node)
def case_0(var_lines_low, one_lines_low, zero_lines_low, pointer_low, var_lines_high, one_lines_high, zero_lines_high, pointer_high, num_inputs, node):
    # Concatenate lists
    if zero_lines_low is not None:
        assert all(len(inner_list) == len(zero_lines_low[0]) for inner_list in zero_lines_low[1:]), "Inner lists have different lengths"
    if zero_lines_high is not None:
        assert all(len(inner_list) == len(zero_lines_high[0]) for inner_list in zero_lines_high[1:]), "Inner lists have different lengths"
    var_lines = merge_variable_lines(var_lines_low,var_lines_high)
    (one_lines, zero_lines) = merge_constant_lines(one_lines_low, one_lines_high, zero_lines_low, zero_lines_high)
    (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)

    # Update pointers
    if pointer_high[0] == 1 and one_lines_low is not None:
        pointer_high = (1, pointer_high[1] + len(one_lines_low[0]))
    elif pointer_high[0] == 2 and zero_lines_low is not None:
        pointer_high = (2, pointer_high[1] + len(zero_lines_low[0]))
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    # Add gates
    # First timestep
    var_lines.append([Element.NULL_GATE] * (len(var_lines[0])))
    if zero_lines is not None:
        new_zeros = []
        for i in range(len(zero_lines[0])):
            if i == pointer_low[1] and pointer_low[0] == 2:
                new_zeros.append(Element.ONE_COND)
            elif i == pointer_high[1] and pointer_high[0] == 2:
                new_zeros.append(Element.FLIP)
            else:
                new_zeros.append(Element.NULL_GATE)
        zero_lines.append(new_zeros)
    if one_lines is not None:
        new_ones = []
        for i in range(len(one_lines[0])):
            if i == pointer_low[1] and pointer_low[0] == 1:
                new_ones.append(Element.ONE_COND)
            elif i == pointer_high[1] and pointer_high[0] == 1:
                new_ones.append(Element.FLIP)
            else:
                new_ones.append(Element.NULL_GATE)
        one_lines.append(new_ones)
    # Second timestep
    var_lines = add_input_cond(var_lines, num_inputs, node.value)
    if zero_lines is not None:
        new_zeros = []
        for i in range(len(zero_lines[0])):
            if i == pointer_low[1] and pointer_low[0] == 2:
                new_zeros.append(Element.FLIP)
            elif i == pointer_high[1] and pointer_high[0] == 2:
                new_zeros.append(Element.ONE_COND)
            else:
                new_zeros.append(Element.NULL_GATE)
        zero_lines.append(new_zeros)
    if one_lines is not None:
        new_ones = []
        for i in range(len(one_lines[0])):
            if i == pointer_low[1] and pointer_low[0] == 1:
                new_ones.append(Element.FLIP)
            elif i == pointer_high[1] and pointer_high[0] == 1:
                new_ones.append(Element.ONE_COND)
            else:
                new_ones.append(Element.NULL_GATE)
        one_lines.append(new_ones)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    return (var_lines, one_lines, zero_lines, (pointer_low[0], pointer_low[1]))

def merge_constant_lines(low_ones, high_ones, low_zeros, high_zeros):
    if low_ones is None and low_zeros is None:
        return (high_ones, high_zeros)
    elif high_ones is None and high_zeros is None:
        return (low_ones, low_zeros)
    # Determine the length
    if low_ones is not None:
        length_low = len(low_ones[0])
        time_low = len(low_ones)
    else:
        length_low = len(low_zeros[0])
        time_low = len(low_zeros)
    if high_ones is not None:
        length_high = len(high_ones[0])
        time_high = len(high_ones)
    else:
        length_high = len(high_zeros[0])
        time_high = len(high_zeros)
    # Temporal adjustment
    if low_ones is not None:
        post_low_ones = [[Element.NULL_GATE] * len(low_ones[0])] * time_high
        low_ones = low_ones + post_low_ones
    if high_ones is not None:
        pre_high_ones = [[Element.NULL_GATE] * len(high_ones[0])] * time_low
        high_ones = pre_high_ones + high_ones
    if low_zeros is not None:
        post_low_zeros = [[Element.NULL_GATE] * len(low_zeros[0])] * time_high
        low_zeros = low_zeros + post_low_zeros
    if high_zeros is not None:
        pre_high_zeros = [[Element.NULL_GATE] * len(high_zeros[0])] * time_low
        high_zeros = pre_high_zeros + high_zeros

    # Combine lines
    if low_ones is None:
        ones = high_ones
    elif high_ones is None:
        ones = low_ones
    else:
        assert (len(low_ones) == len(high_ones) )
        len_low = len(low_ones)
        for i in range(len_low):
            low_ones[i] = low_ones[i] + high_ones[i]
        ones = low_ones
    if low_zeros is None:
        zeros = high_zeros
    elif high_zeros is None:
        zeros = low_zeros
    else:
        assert (len(low_zeros) == len(high_zeros))
        len_low = len(low_zeros)
        for i in range(len_low):
            low_zeros[i] = low_zeros[i] + high_zeros[i]
        zeros = low_zeros
    return (ones, zeros)
def merge_variable_lines(var_lines_low, var_lines_high):
    if var_lines_low == None:
        return var_lines_high
    elif var_lines_high == None:
        return var_lines_low
    while len(var_lines_low[0]) < len(var_lines_high[0]):
        for i in range(len(var_lines_low)):
            var_lines_low[i].append(Element.NULL_GATE)
    while len(var_lines_low[0]) > len(var_lines_high[0]):
        for i in range(len(var_lines_high)):
            var_lines_high[i].append(Element.NULL_GATE)
    var_lines_low.extend(var_lines_high)
    return var_lines_low
def case_1(var_lines, one_lines, zero_lines, pointer, num_inputs, node):
    (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    # Add new zero_line with Null Gates until now
    zero_lines = add_new_line(var_lines, zero_lines)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    # Add new gates
    # First timestep
    var_lines = add_input_cond(var_lines, num_inputs, node.value)
    (var_lines, one_lines, zero_lines) = addZeroFlip_AndControlLines(var_lines, one_lines, zero_lines, pointer)
    # Second timestep
    new_timestep = []
    for i in range(num_inputs):
        new_timestep.append(Element.NULL_GATE)
    var_lines.append(new_timestep)
    (var_lines, one_lines, zero_lines) = addZeroFlip_AndControlLines(var_lines, one_lines, zero_lines, pointer)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    return (var_lines, one_lines, zero_lines, (2, len(zero_lines[0]) - 1))
def case_2(var_lines, one_lines, zero_lines, pointer, num_inputs, node):
    (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    # Add new zero_line with Null Gates until now
    zero_lines = add_new_line(var_lines, zero_lines)
    # Add new gates
    # First timestep
    var_lines = add_input_cond(var_lines, num_inputs, node.value)
    (var_lines, one_lines, zero_lines) = addZeroFlip_AndControlLines(var_lines,one_lines,zero_lines,pointer)
    # Second timestep
    new_timestep = []
    for i in range(num_inputs):
        new_timestep.append(Element.NULL_GATE)
    var_lines.append(new_timestep)
    (var_lines, one_lines, zero_lines) = addZeroFlip_AndControlLines(var_lines, one_lines, zero_lines, pointer)
    # Third timestep
    var_lines = add_input_cond(var_lines, num_inputs, node.value)
    zero_line_timestep = [Element.NULL_GATE] * (len(zero_lines[0]) - 1)
    zero_line_timestep.append(Element.FLIP)
    zero_lines.append(zero_line_timestep)
    if one_lines is not None:
        one_line_timestep = [Element.NULL_GATE] * (len(one_lines[0]))
        one_lines.append(one_line_timestep)
    (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    return (var_lines, one_lines, zero_lines, (2, len(zero_lines[0]) - 1))
def addZeroFlip_AndControlLines(var_lines, one_lines, zero_lines, pointer):
    if pointer[0] == 1:
        # Pointer in onelines
        one_line_timestep = []
        for i in range(len(one_lines[0])):
            if i == pointer[1]:
                one_line_timestep.append(Element.ONE_COND)
            else:
                one_line_timestep.append(Element.NULL_GATE)
        one_lines.append(one_line_timestep)

        zero_line_timestep = [Element.NULL_GATE] * (len(zero_lines[0]) - 1)
        zero_line_timestep.append(Element.FLIP)
        zero_lines.append(zero_line_timestep)
    else:
        # Pointer in zero lines
        zero_line_timestep = []
        for i in range(len(zero_lines[0]) - 1):
            if i == pointer[1]:
                zero_line_timestep.append(Element.ONE_COND)
            else:
                zero_line_timestep.append(Element.NULL_GATE)
        zero_line_timestep.append(Element.FLIP)
        zero_lines.append(zero_line_timestep)
        (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    return (var_lines, one_lines, zero_lines)
def case_3(var_lines, one_lines, zero_lines, pointer, num_inputs, node):
    (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    # Add new zero_line with Null Gates until now
    zero_lines = add_new_line(var_lines, zero_lines)
    # Add new gates
    var_lines = add_input_cond(var_lines, num_inputs, node.value)
    if pointer[0] == 1:
        # Pointer in onelines
        one_line_timestep = []
        for i in range(len(one_lines[0])):
            if i == pointer[1]:
                one_line_timestep.append(Element.ONE_COND)
            else:
                one_line_timestep.append(Element.NULL_GATE)
        one_lines.append(one_line_timestep)

        zero_line_timestep = [Element.NULL_GATE] * (len(zero_lines[0]) - 1)
        zero_line_timestep.append(Element.FLIP)
        zero_lines.append(zero_line_timestep)
    else:
        # Pointer in zero lines
        zero_line_timestep = []
        for i in range(len(zero_lines[0]) - 1):
            if i == pointer[1]:
                zero_line_timestep.append(Element.ONE_COND)
            else:
                zero_line_timestep.append(Element.NULL_GATE)
        zero_line_timestep.append(Element.FLIP)
        zero_lines.append(zero_line_timestep)
        (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    return (var_lines, one_lines, zero_lines, (2, len(zero_lines[0]) - 1))
def case_4(var_lines, one_lines, zero_lines, pointer, num_inputs, node):
    (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    # Add new one_line with Null Gates until now
    one_lines = add_new_line(var_lines, one_lines)
    # Add new gates
    one_line_timestep = [Element.NULL_GATE] * (len(one_lines[0]) - 1) + [Element.FLIP]
    one_lines.append(one_line_timestep)
    var_lines = add_input_cond(var_lines, num_inputs, node.value)
    (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)

    var_lines = add_input_cond(var_lines, num_inputs, node.value)
    if pointer[0] == 1:
        # Pointer in onelines
        one_line_timestep = []
        for i in range(len(one_lines[0]) - 1):
            if i == pointer[1]:
                one_line_timestep.append(Element.ONE_COND)
            else:
                one_line_timestep.append(Element.NULL_GATE)
        one_line_timestep.append(Element.FLIP)
        one_lines.append(one_line_timestep)
        (var_lines, one_lines, zero_lines) = pad_lists(var_lines, one_lines, zero_lines)
    else:
        # Pointer in zero lines
        one_line_timestep = [Element.NULL_GATE] * (len(one_lines[0]) - 1)
        one_line_timestep.append(Element.FLIP)
        one_lines.append(one_line_timestep)

        zero_line_timestep = []
        for i in range(len(zero_lines[0])):
            if i == pointer[1]:
                zero_line_timestep.append(Element.ONE_COND)
            else:
                zero_line_timestep.append(Element.NULL_GATE)
        zero_lines.append(zero_line_timestep)
    if zero_lines is not None:
        assert all(len(inner_list) == len(zero_lines[0]) for inner_list in zero_lines[1:]), "Inner lists have different lengths"
    return (var_lines, one_lines, zero_lines, (1, len(one_lines[0]) - 1))
def pad_lists(var_lines, one_lines, zero_lines):
    # Pad one_lines
    if one_lines is not None:
        while len(one_lines) < len(var_lines):
            one_lines.append([Element.NULL_GATE] * len(one_lines[0]))
    # Pad zero_lines
    if zero_lines is not None:
        while len(zero_lines) < len(var_lines):
            zero_lines.append([Element.NULL_GATE] * len(zero_lines[0]))

    return var_lines, one_lines, zero_lines
def add_new_line(var_lines, lines):
    """
    Takes a line list and adds a new line which has just NULL Gates until the current timestep
    """
    if lines == None:
        return [[Element.NULL_GATE]] * len(var_lines)
    assert (len(var_lines) == len(lines))
    '''
    for i in range(len(var_lines)):
        lines[i].append(Element.NULL_GATE)
    '''
    seen = set()
    for inner_list in lines:
        if tuple(inner_list) not in seen:
            inner_list.append(Element.NULL_GATE)
            seen.add(tuple(inner_list))
    return lines
def add_input_cond(var_lines, num_variables, node_val):
    '''
    Adds a one control line at the next timestep to the right variable line
    '''
    new_timestep = []
    for i in range(num_variables):
        if i == node_val:
            new_timestep.append(Element.ONE_COND)
        else:
            new_timestep.append(Element.NULL_GATE)
    var_lines.append(new_timestep)
    return var_lines

def isOneLeaf(node):
    """
    Check if the given node is a one leaf (terminal node with output value 1).
    """
    return node.low is None and node.high is None and node.value == 1
def isZeroLeaf(node):
    """
    Check if the given node is a zero leaf (terminal node with output value 0).
    """
    return node.low is None and node.high is None and node.value == 0
def count_terminal_nodes(node):
    """
    Returns:
    - A tuple containing the counts of terminal nodes with output value 1 and 0.
    """
    # Base case: If the node is a terminal node, return the count accordingly
    if node.low is None and node.high is None:
        return (1, 0) if node.value == 1 else (0, 1)

    # Recursive case: Traverse the low and high branches
    count_low = count_terminal_nodes(node.low) if node.low else (0, 0)
    count_high = count_terminal_nodes(node.high) if node.high else (0, 0)

    # Aggregate the counts from the low and high branches
    total_ones = count_low[0] + count_high[0]
    total_zeros = count_low[1] + count_high[1]

    return total_ones, total_zeros
def get_bdds(tt):
    """
    - Returns the binary decision diagrams for all output bits
    - Input: Truth table
    """
    bdds = []
    binary_length = len(bin(max([t[1] for t in tt]))) - 2
    for i in range(binary_length):
        copied_list = [(x, extract_bit((y,), i)[0]) for x, y in tt]
        bdds.append(build_bdd(copied_list))
    return bdds
def bdd_based_synthesis(tt):
    """
    - Takes a reverseible truth table and returns the resulting circuit, as well as the line indices of the output variables
    """
    num_inputs = int(log2(len(tt)))
    bdds = get_bdds(tt)
    circuits = []
    for bdd in bdds:
        circuits.append(add_gates_rec(bdd,num_inputs))
    pointers = [circuits[0][3]]
    while len(circuits) >= 2:
        circuitA = circuits.pop(0)
        circuitB = circuits.pop(0)

        pointerA = circuitA[3]
        pointerB = circuitB[3]

        # Update pointers
        if pointerB[0] == 1 and circuitA[1] is not None:
            pointerB = (1, pointerB[1] + len(circuitA[1][0]))
        elif pointerB[0] == 2 and circuitA[2] is not None:
            pointerB = (2, pointerB[1] + len(circuitA[2][0]))
        pointers.append(pointerB)

        (ones, zeros) = merge_constant_lines(circuitA[1], circuitB[1], circuitA[2], circuitB[2])
        variable_lines = merge_variable_lines(circuitA[0], circuitB[0])
        circuits.insert(0, (variable_lines, ones, zeros, pointerB))
    return (circuits[0], pointers)

def extract_bit(data, i):
    """Extract the i-th bit from each integer in the data."""
    return [(num >> i) & 1 for num in data]
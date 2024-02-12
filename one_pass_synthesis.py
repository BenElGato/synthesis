from Gate_Elements import Element
from math import log2
from circuitToString import *

def one_pass_synthesis(truth_table: list[(int, int)]) -> list[list[Element]]:
    bit_count = int(log2(len(truth_table)))
    result_gates = []
    reverse_gates = []#get_reverse_change_gates(bit_count)
    change_gates = get_change_gates(truth_table, bit_count, reverse_gates)
    transformation_gates = get_transformation_gates(truth_table, bit_count)
    result_gates = change_gates + transformation_gates + reverse_gates
    print(circuitToString(result_gates))
    return result_gates

def get_change_gates(truth_table: list[(int, int)], bit_count: int, reverse_gates: list[list[Element]]):
    gates = []
    existing_output = set()
    for i, (current_input, current_output) in enumerate(truth_table):
        if current_output in existing_output:
            new_output = find_closest_number(current_output, existing_output, bit_count)
            #for new_output in range(2**bit_count):
            #    if not new_output in existing_output:
            truth_table[i] = (current_input, new_output)
            existing_output.add(new_output)
            gates.extend(create_change_gates(current_input, current_output, new_output, bit_count, reverse_gates))
            #        break
        else:
            existing_output.add(current_output)

    return gates


def create_change_gates(input: int, old: int, new:int, bit_count: int, reverse_gates: list[list[Element]]) -> list[list[Element]]:
    gates = []
    for bit_pos in range(bit_count):
        if not get_bit(old, bit_pos) is get_bit(new, bit_pos):
            gate = [Element.NULL_GATE for _ in range(bit_count*2)]
            gate[bit_count - (bit_pos+1)] = Element.FLIP
            for bit_index in range(bit_count):
                gate[bit_count*2 - (bit_index + 1)] = Element(get_bit(input, bit_index))
            gates.append(gate)
            reverse_gates.append(get_reverse_change_gate_refactored(bit_count, bit_pos))

    return gates

def get_reverse_change_gates(bit_count: int) -> list[list[Element]]:
    gates = []
    for bit in range(bit_count):
        gate = [Element.NULL_GATE for _ in range(bit_count*2)]
        gate[bit] = Element.ONE_COND
        gate[bit + bit_count] = Element.FLIP
        gates.append(gate)
    return gates

def get_reverse_change_gate_refactored(bit_count: int, index: int) -> list[list[Element]]:
    gate = [Element.NULL_GATE for _ in range(bit_count*2)]
    gate[bit_count-1-index] = Element.ONE_COND
    gate[bit_count*2-1-index] = Element.FLIP
    return gate

def get_transformation_gates(truth_table: list[(int, int)], bit_count: int) -> list[list[Element]]:
    gates = []
    z_o = truth_table[0][1]
    if not z_o == 0:
        bin_of_output = bin(z_o)[2:]
        for i, c in enumerate(bin_of_output):
            if c == "1":
                gates.append(build_gate(bit_count, [], len(bin_of_output)-(i+1)))
                update_truth_table(len(bin_of_output)-(i+1), [], truth_table)
                table_to_string(truth_table, bit_count)

    for i in range(len(truth_table)):
        input = truth_table[i][0]
        output = truth_table[i][1]
        if input == output:
            continue
        else:
            add_bitstr, remove_bitstr = find_all_incorrect_bits(input, output, bit_count)
            gates.extend(create_transf_gates_and_update(add_bitstr, remove_bitstr, truth_table, bit_count, i))
            table_to_string(truth_table, bit_count)
            #print(circuitToString(gates))

    gates.reverse()
    return gates

def create_transf_gates_and_update(addstr: str, remstr: str, tt: list[(int, int)], bit_count: int, tt_i: int):
    gates = []
    if "1" in addstr:
        for i, b in enumerate((addstr[::-1])):
            if b == "1":
                set_bits = find_set_bits_indices(tt[tt_i][1])
                update_truth_table(i, set_bits, tt)
                gates.append(build_gate(bit_count, set_bits, i))
            
    if "1" in remstr:
        for i, b in enumerate((remstr[::-1])):
            if b == "1":
                set_bits = find_set_bits_indices(tt_i)
                update_truth_table(i, set_bits, tt)
                gates.append(build_gate(bit_count, set_bits, i))

    return gates

def update_truth_table(flip_pos: int, condition_indexs: list[int], tt: list[(int,int)]):
    if condition_indexs == []:
        for i, (inp, out) in enumerate(tt):
            tt[i] = (inp, flip_bit(out, flip_pos))
    else:
        for i, (inp, out) in enumerate(tt):
            should_flip = True
            for cond in condition_indexs:
                if get_bit(out, cond) == 0:
                    should_flip = False
            if should_flip:
                tt[i] = (inp, flip_bit(out, flip_pos))
 
def find_all_incorrect_bits(inp: int, out: int, bit_count: int):
    add_bitstr = "0" * bit_count
    remove_bitstr = "0" * bit_count

    for j in range(bit_count):
        if get_bit(out, j) == 0 and get_bit(inp, j) == 1:
            add_bitstr = add_bitstr[:(bit_count-(j+1))] + "1" + add_bitstr[bit_count-j:]

    for j in range(bit_count):
        if get_bit(out, j) == 1 and get_bit(inp, j) == 0:
            remove_bitstr = remove_bitstr[:(bit_count-(j+1))] + "1" + remove_bitstr[bit_count-j:]

    return (add_bitstr, remove_bitstr)
    

def build_gate(bit_count: int, condition_indexs: list[int], flip_position):
    gate = [Element.NULL_GATE for _ in range(bit_count*2)]
    gate[bit_count*2 - (flip_position+1)] = Element.FLIP
    for bit_index in condition_indexs:
        gate[bit_count*2 - (bit_index+1)] = Element.ONE_COND
    return gate

def get_bit(number: int, position: int):
    return (number >> position) & 1

def flip_bit(number: int, position: int):
    bitmask = 1 << position
    result = number ^ bitmask
    return result

def find_set_bits_indices(number):
    binary_representation = bin(number)[2:] 
    set_bits_indices = [i for i, bit in enumerate(reversed(binary_representation)) if bit == '1']
    return set_bits_indices 

def hamming_distance(num1, num2):
    bin_str1 = bin(num1)[2:]
    bin_str2 = bin(num2)[2:]
    max_len = max(len(bin_str1), len(bin_str2))
    bin_str1 = bin_str1.zfill(max_len)
    bin_str2 = bin_str2.zfill(max_len)
    distance = sum(b1 != b2 for b1, b2 in zip(bin_str1, bin_str2))
    return distance

def find_closest_number(x, y, bit_count):
    print([num for num in range(2 ** bit_count) if num not in y])
    closest_number = min((num for num in range(2 ** bit_count) if num not in y),
                         key=lambda num: hamming_distance(x, num))
    return closest_number
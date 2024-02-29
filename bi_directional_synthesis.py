from math import log2
from circuitToString import *
from one_pass_synthesis import get_change_gates,hamming_distance, find_all_incorrect_bits,create_transf_gates_and_update as onepass_create_transf_gates_and_update, find_set_bits_indices, build_gate,flip_bit,get_bit

def bi_one_pass_synthesis(truth_table: list[(int, int)]) -> list[list[Element]]:
    bit_count = int(log2(len(truth_table)))
    result_gates = []
    reverse_gates = []#get_reverse_change_gates(bit_count)
    change_gates = get_change_gates(truth_table, bit_count, reverse_gates)
    transformation_gates = get_transformation_gates(truth_table, bit_count)
    result_gates = change_gates + transformation_gates + reverse_gates
    print(tt_circuit_To_String(result_gates))
    return result_gates


def get_transformation_gates(truth_table: list[(int, int)], bit_count: int) -> list[list[Element]]:
    input_gates = []
    output_gates = []
    for i in range(len(truth_table)):
        input = truth_table[i][0]
        output = truth_table[i][1]
        if input == output:
            continue
        else:
            index = get_j(i,truth_table,bit_count)
            j = truth_table[index][0]
            if (hamming_distance(input,output) <= hamming_distance(input, j)):
                add_bitstr, remove_bitstr = find_all_incorrect_bits(input, output, bit_count)
                output_gates.extend(onepass_create_transf_gates_and_update(add_bitstr, remove_bitstr, truth_table, bit_count, i))
                table_to_string(truth_table, bit_count)
            else:
                add_bitstr, remove_bitstr = find_all_incorrect_bits(input, j, bit_count)
                input_gates.extend(create_transf_gates_and_update(add_bitstr, remove_bitstr, truth_table, bit_count, i,j))

                truth_table.sort(key=lambda x: x[0])
                table_to_string(truth_table, bit_count)
    output_gates.reverse()
    gates = input_gates + output_gates
    return gates

def get_j(i:int, truth_table: list[(int, int)], bit_count: int)->int:
    input = truth_table[i][0]
    for j in range(i + 1, len(truth_table)):
        if truth_table[j][1] == input:
            return j
    return None


def create_transf_gates_and_update(addstr: str, remstr: str, tt: list[(int, int)], bit_count: int, tt_i: int, j: int):
    gates = []
    if "1" in addstr:
        for i, b in enumerate((addstr[::-1])):
            if b == "1":
                set_bits = find_set_bits_indices(j)
                update_truth_table(i, set_bits, tt)
                gates.append(build_gate(bit_count, set_bits, i))
    if "1" in remstr:
        for i, b in enumerate((remstr[::-1])):
            if b == "1":
                set_bits = find_set_bits_indices(tt_i)
                update_truth_table(i, set_bits, tt)
                gates.append(build_gate(bit_count, set_bits, i))
    return gates

def update_truth_table(flip_pos: int, condition_indexs: list[int], tt: list[(int, int)]):
    if condition_indexs == []:
        for i, (inp, out) in enumerate(tt):
            tt[i] = (flip_bit(inp, flip_pos), out)
    else:
        for i, (inp, out) in enumerate(tt):
            should_flip = True
            for cond in condition_indexs:
                if get_bit(inp, cond) == 0:
                    should_flip = False
            if should_flip:
                tt[i] = (flip_bit(inp, flip_pos), out)

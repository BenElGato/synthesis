from math import log2
from circuitToString import *
from one_pass_synthesis import get_change_gates,hamming_distance, find_all_incorrect_bits,create_transf_gates_and_update

def one_pass_synthesis(truth_table: list[(int, int)]) -> list[list[Element]]:
    bit_count = int(log2(len(truth_table)))
    result_gates = []
    reverse_gates = []#get_reverse_change_gates(bit_count)
    change_gates = get_change_gates(truth_table, bit_count, reverse_gates)
    transformation_gates = get_transformation_gates(truth_table, bit_count)
    result_gates = change_gates + transformation_gates + reverse_gates
    print(circuitToString(result_gates))
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
            j = truth_table[get_j(i,truth_table,bit_count)][0]
            if (hamming_distance(input,output) <= hamming_distance(input, j)):
                #TODO: Apply Toffoli gates to the outputs, so that f+(i) = input
                add_bitstr, remove_bitstr = find_all_incorrect_bits(input, output, bit_count)
                output_gates.extend(create_transf_gates_and_update(add_bitstr, remove_bitstr, truth_table, bit_count, i))
                table_to_string(truth_table, bit_count)
            else:
                #TODO: Apply Toffoli gates to the inputs, so that j --> i
                add_bitstr, remove_bitstr = find_all_incorrect_bits(j, input, bit_count)
                input_gates.extend(create_transf_gates_and_update(add_bitstr, remove_bitstr, truth_table, bit_count, i))
                table_to_string(truth_table, bit_count)
                continue
    output_gates.reverse()
    gates = input_gates + output_gates
    return gates

'''
Returns the row j which output is equals to the input of i
'''
def get_j(i:int, truth_table: list[(int, int)], bit_count: int)->int:
    input = truth_table[i][0]
    for j in range(i + 1, len(truth_table)):
        if truth_table[j][1] == input:
            return j
    return None
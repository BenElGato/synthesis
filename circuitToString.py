from Gate_Elements import Element
def add_char_to_ith_line(original_string, char, i):
    lines = original_string.split('\n')
    if 0 <= i < len(lines):
        lines[i] += char
    else:
        raise IndexError("The specified index is out of range.")
    return '\n'.join(lines)
def remove_empty_lines(original_string):
    lines = original_string.split('\n')
    return '\n'.join([s for s in lines if not all(c == '─' for c in s[5:])])

def add_lable (original_string):
    lines = original_string.split('\n')
    labled_lines = []
    half_length = len(lines) // 2
    lables = iter([f'b_{chr(ord("a") + i)}' for i in range(26)])
    
    for i, string in enumerate(lines):
        label = next(lables) if i < half_length else (str(chr(ord("a") + i - half_length)) + "  ")
        labled_string = f'{label}: {string}'
        labled_lines.append(labled_string)

    return '\n'.join(labled_lines)


def circuitToString(circuit):
    if not circuit or circuit == []:
        return "Empty circuit"
    variables = len(circuit[0])
    s = '─\n' * (variables - 1) + '─'
    for i in range(len(circuit)):
        for j in range(variables):
            #assert (len(circuit[i]) == variables)
            if circuit[i][j] == Element.ZERO_COND:
                s = add_char_to_ith_line(s,'○', j)
            elif circuit[i][j] == Element.ONE_COND:
                s = add_char_to_ith_line(s, '●', j)
            elif circuit[i][j] == Element.NULL_GATE:
                s = add_char_to_ith_line(s, '─', j)
            elif circuit[i][j] == Element.FLIP:
                s = add_char_to_ith_line(s, '\u2A01', j)
            else:
                raise ValueError("Shouldnt happen")
            s = add_char_to_ith_line(s, '─', j)
            s = add_char_to_ith_line(s, '─', j)

    return s

def tt_circuit_To_String(circuit):
    '''
    Use this function to print a truth table based function
    '''
    s = circuitToString(circuit)
    s = add_lable(s)
    s = remove_empty_lines(s)
    return s
def bdd_circuit_to_string(circuit, pointers):
    '''
        Use this function to print a decission diagram based function
    '''
    var_string  = circuitToString(circuit[0])
    one_string = circuitToString(circuit[1])
    zero_string = circuitToString(circuit[2])

    var_lines = var_string.split("\n")
    one_lines = one_string.split("\n")
    zero_lines = zero_string.split("\n")

    for i in range(len(pointers)):
        if pointers[i][0] == 1:
            one_lines[pointers[i][1]] = one_lines[pointers[i][1]] + f" x_{len(pointers) - 1 - i}"
        elif pointers[i][0] == 2:
            zero_lines[pointers[i][1]] = zero_lines[pointers[i][1]] + f" x_{len(pointers) - 1 - i}"
    labeled_var_lines = [f"x_{i} " + var_lines[i] for i in range(len(var_lines))]
    labeled_one_lines = [ "1   " + line for line in one_lines]
    labeled_zero_lines = ["0   " + line for line in zero_lines]
    result_var_lines = "\n".join(labeled_var_lines)
    result_one_lines = "\n".join(labeled_one_lines)
    result_zero_lines = "\n".join(labeled_zero_lines)
    if circuit[1] == None:
        result_one_lines = ""
    if circuit[2] == None:
        result_zero_lines = ""
    result_string = result_var_lines + "\n" + result_one_lines + "\n" + result_zero_lines
    return result_string
def table_to_string(table: list((int, int)), bit_count: int):
    for (inp, out) in table:
        print(binary_representation_with_min_bits(inp, bit_count) +  " | " + binary_representation_with_min_bits(out, bit_count))

    print("------------------------------")


def binary_representation_with_min_bits(number, n):
    binary_string = bin(number)[2:]
    formatted_binary = format(number, f'0{n}b')
    return formatted_binary


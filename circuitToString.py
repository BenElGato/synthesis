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
        for j in range(len(circuit[i])):
            if circuit[i][j] == Element.ZERO_COND:
                s = add_char_to_ith_line(s,'○', j)
            elif circuit[i][j] == Element.ONE_COND:
                s = add_char_to_ith_line(s, '●', j)
            elif circuit[i][j] == Element.NULL_GATE:
                s = add_char_to_ith_line(s, '─', j)
            elif circuit[i][j] == Element.FLIP:
                s = add_char_to_ith_line(s, '\u2A01', j)
            s = add_char_to_ith_line(s, '─', j)
            s = add_char_to_ith_line(s, '─', j)
    s = add_lable(s)
    s = remove_empty_lines(s)
    return s

def table_to_string(table: list((int, int))):
    for (inp, out) in table:
        print(binary_representation_with_min_bits(inp, 3) +  " | " + binary_representation_with_min_bits(out, 3))

    print("------------------------------")


def binary_representation_with_min_bits(number, n):
    binary_string = bin(number)[2:]
    formatted_binary = format(number, f'0{n}b')
    return formatted_binary


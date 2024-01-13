from Gate_Elements import Element
def add_char_to_ith_line(original_string, char, i):
    lines = original_string.split('\n')
    if 0 <= i < len(lines):
        lines[i] += char
    else:
        raise IndexError("The specified index is out of range.")
    return '\n'.join(lines)
def circuitToString(circuit):
    if not circuit or circuit == []:
        return "Empty circuit"
    variables = len(circuit[0])
    s = '-\n' * (variables - 1) + '-'
    for i in range(len(circuit)):
        for j in range(len(circuit[i])):
            if circuit[i][j] == Element.ZERO_COND:
                s = add_char_to_ith_line(s,'0', j)
            elif circuit[i][j] == Element.ONE_COND:
                s = add_char_to_ith_line(s, '1', j)
            elif circuit[i][j] == Element.NULL_GATE:
                s = add_char_to_ith_line(s, '-', j)
            elif circuit[i][j] == Element.FLIP:
                s = add_char_to_ith_line(s, 'X', j)
            s = add_char_to_ith_line(s, '-', j)
            s = add_char_to_ith_line(s, '-', j)
    return s


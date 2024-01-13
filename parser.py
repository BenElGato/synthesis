import string


def getTruthTable(filepath):
    with open(filepath, 'r') as file:
        truth_table = []
        lines = [line.strip() for line in file]
        for i in range(len(lines)):
            line = lines[i]
            if i == 0:
                try:
                    number = int(line)
                except ValueError:
                    raise ValueError("Invalid number")
            else:
                parts = line.split('|')
                if len(parts) != 2:
                    raise ValueError(f"Line {i} is invalid!")
                binary_str_input = parts[0].replace(" ", "")
                binary_str_output = parts[1].replace(" ", "")
                if len(binary_str_input) != number or len(binary_str_output) != number:
                    raise ValueError(f"Line {i} is invalid!")
                if not (all(char in '01' for char in binary_str_input) and all(char in '01' for char in binary_str_output)):
                    raise ValueError("Line {i} is invalid!")
                input = int(binary_str_input,2)
                output = int(binary_str_output, 2)
                truth_table.append((input,output))
        if len(lines) != 2**number + 1:
            raise ValueError(f"Wrong amount of lines in {filepath}!")
        return truth_table
table = getTruthTable("table.txt")
print(table)

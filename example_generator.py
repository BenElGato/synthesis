import itertools


def generate_all_reversible_truth_tables():
    inputs = list(itertools.product([0, 1], repeat=3))
    all_permutations = itertools.permutations(inputs)

    return all_permutations


def save_all_truth_tables():
    all_permutations = generate_all_reversible_truth_tables()

    for i, permutation in enumerate(all_permutations, start=1):
        file_path = f"/home/benedikt/PycharmProjects/synthesis/examples/3_variables/{i}.txt"
        with open(file_path, "w") as file:
            file.write("3\n")  # Write the number of variables at the top of the file
            for input, output in zip(itertools.product([0, 1], repeat=3), permutation):
                line = f"{input[0]} {input[1]} {input[2]} | {output[0]} {output[1]} {output[2]}"
                file.write(line + "\n")
        print(f"All permutations truth table {i} saved to {file_path}")


if __name__ == "__main__":
    save_all_truth_tables()


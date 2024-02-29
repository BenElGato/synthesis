from circuitToString import *
from tt_parser import getTruthTable
from bi_directional_synthesis import one_pass_synthesis as one_pass_bi
from one_pass_synthesis import one_pass_synthesis as one_pass_uni
from Gate_Elements import *
from template_matching import reduce
from TruthTable_To_BDD import build_bdd, visualize_bdd_with_graphviz, Node
from bdd_synthesis import get_bdds, bdd_based_synthesis
def avg_gates_3_inputs():
    gates_uni = []
    gates_bi  = []
    gates_uni_pattern = []
    gates_bi_pattern = []
    gates_bdd = []

    for i in range(1,40320):
        file = f"/home/benedikt/PycharmProjects/synthesis/examples/3_variables/{i}.txt"
        tt = getTruthTable(file)
        circuit_bi = one_pass_bi(tt)
        gates_bi.append(len(circuit_bi))
        circuit_bdd = bdd_based_synthesis(tt, 3)
        gates_bdd.append(len(circuit_bdd[0][0]))

        tt = getTruthTable(file)
        circuit_uni = one_pass_uni(tt)
        gates_uni.append(len(circuit_uni))

        reduced_uni = reduce(circuit_uni)
        reduced_bi = reduce(circuit_bi)
        gates_bi_pattern.append(len(reduced_bi))
        gates_uni_pattern.append(len(reduced_uni))

    total_tests = 40320.0

    avg_gates_uni = sum(gates_uni) / total_tests
    avg_gates_bi = sum(gates_bi) / total_tests
    avg_gates_reduced_uni = sum(gates_uni_pattern)/ total_tests
    avg_gates_reduced_bi = sum(gates_bi_pattern)/ total_tests
    avg_gates_bdd = sum(gates_bdd) / total_tests


    print(f"Average gates unidirectional: {avg_gates_uni}\nAverage gates bidirectional: {avg_gates_bi}\nAverage gates unidirectional pattern: {avg_gates_reduced_uni}\nAverage gates bidirectional pattern: {avg_gates_reduced_bi}\nAverage gates binary decision diagram based: {avg_gates_bdd}")
#avg_gates_3_inputs()

file = "examples/reversible_truth_table_3_variables.txt"
tt = getTruthTable(file)

bdds = get_bdds(tt)
#bdd = build_bdd(tt)
#bdd = build_bdd(tt)
#max_value = max(tt, key=lambda x: x[1])[1]
bdd_graph = visualize_bdd_with_graphviz(bdds[2],num_variables=1)
bdd_graph.render('bdd_graph', format='png', cleanup=True)
(circuit, pointers) = bdd_based_synthesis(tt, 3)
print(bdd_circuit_to_string(circuit,pointers))


'''
circuit_bi = one_pass_bi(tt)
tt = getTruthTable(file)
circuit_uni = one_pass_uni(tt)
uni_gate_amount = len(circuit_uni)
bi_gate_amount = len(circuit_bi)

reduced1 = reduce(circuit_uni)
reduced2 = reduce(circuit_bi)

print(f"Amount of gates with unidirectional approach: {uni_gate_amount}\nAmount of gates with bidirectional approach: {bi_gate_amount}")
print(f"Unidirectional approach with pattern matches just needs {len(reduced1)} gates:")
print(tt_circuit_To_String((reduced1)))
print("\n")
print(f"Bidirectional approach with pattern matches just needs {len(reduced2)} gates:")
print(tt_circuit_To_String((reduced2)))
'''

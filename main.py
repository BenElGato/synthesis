from circuitToString import *
from parser import getTruthTable
from bi_directional_synthesis import one_pass_synthesis as one_pass_bi
from one_pass_synthesis import one_pass_synthesis as one_pass_uni
from Gate_Elements import *
from template_matching import reduce
'''
file = "bidirectional_example.txt"

tt = getTruthTable(file)

circuit_bi = one_pass_bi(tt)

tt = getTruthTable(file)
circuit_uni = one_pass_uni(tt)


uni_gate_amount = len(circuit_uni)
bi_gate_amount = len(circuit_bi)

reduced1 = reduce(circuit_uni)
reduced2 = reduce(circuit_bi)

print(f"Amount of gates with unidirectional approach: {uni_gate_amount}\nAmount of gates with bidirectional approach: {bi_gate_amount}")
print(len(reduced1))
print(circuitToString(circuit_uni))
print("\n")
print(circuitToString(reduced1))
print(len(reduced2))
'''

gates_uni = []
gates_bi  = []
gates_uni_pattern = []
gates_bi_pattern = []

for i in range(1,40320):
    file = f"/home/benedikt/PycharmProjects/synthesis/examples/3_variables/{i}.txt"
    tt = getTruthTable(file)
    circuit_bi = one_pass_bi(tt)
    gates_bi.append(len(circuit_bi))
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


print(f"Average gates unidirectional: {avg_gates_uni}\nAverage gates bidirectional: {avg_gates_bi}\nAverage gates unidirectional pattern: {avg_gates_reduced_uni}\nAverage gates bidirectional pattern: {avg_gates_reduced_bi}\n")

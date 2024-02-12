from collections import Counter

import circuitToString
from Gate_Elements import *
def reduce(circuit: list)-> list:
    finished = False
    while not finished:
        finished = True
        for i, gate in enumerate(circuit):
            if i + 2 < len(circuit):
                one_count = Counter(gate)[Element.ONE_COND]
                next_gate = circuit[i+1]
                next_one_count = Counter(next_gate)[Element.ONE_COND]
                next_next_gate = circuit[i + 2]
                next_next_one_count = Counter(next_next_gate)[Element.ONE_COND]
                if one_count == 0:
                    if next_one_count == 1:
                        if next_next_one_count == 2:
                            # Match 3.1
                            pos_flip = gate.index(Element.FLIP)
                            pos_next_flip = next_gate.index(Element.FLIP)
                            pos_next_one = next_gate.index(Element.ONE_COND)
                            if next_gate[pos_flip] == Element.NULL_GATE and next_next_gate[pos_flip] == Element.ONE_COND and next_next_gate[pos_next_one] == Element.ONE_COND and next_next_gate[pos_next_flip] == Element.FLIP:
                                gate[pos_flip] = Element.ONE_COND
                                gate[pos_next_one] = Element.ONE_COND
                                gate[pos_next_flip] = Element.FLIP

                                next_gate[pos_flip] = Element.FLIP
                                next_gate[pos_next_one] = Element.NULL_GATE
                                next_gate[pos_next_flip] = Element.NULL_GATE

                                circuit.pop(i+2)
                                finished = False
                    elif next_one_count == 2:
                        if next_next_one_count == 0:
                            # Match 4.4
                            pos_flip = gate.index(Element.FLIP)
                            pos_next_flip = next_gate.index(Element.FLIP)
                            indexes = [index for index, value in enumerate(next_gate) if value == Element.ONE_COND]
                            if next_gate[pos_flip] == Element.ONE_COND and next_next_gate[pos_flip] == Element.FLIP:
                                gate[pos_flip] = Element.ONE_COND
                                gate[pos_next_flip] = Element.FLIP
                                indexes.remove(pos_flip)
                                gate[indexes[0]] = Element.ONE_COND

                                next_gate[pos_flip] = Element.NULL_GATE
                                circuit.pop(i+2)
                                finished = False

                elif one_count == 1:
                    if next_one_count == 1:
                        if next_next_one_count == 1:
                            pos_flip = gate.index(Element.FLIP)
                            pos_one = gate.index(Element.ONE_COND)

                            pos_next_flip = next_gate.index(Element.FLIP)
                            pos_next_one = next_gate.index(Element.ONE_COND)

                            pos_next_next_flip = next_next_gate.index(Element.FLIP)
                            pos_next_next_one = next_next_gate.index(Element.ONE_COND)

                            if pos_one == pos_next_flip and pos_one == pos_next_next_one and pos_flip != pos_next_one and pos_flip == pos_next_next_flip:
                                # Match 4.1
                                gate[pos_one] = Element.FLIP
                                gate[pos_next_one] = Element.ONE_COND
                                gate[pos_flip] = Element.NULL_GATE

                                next_gate[pos_one] = Element.NULL_GATE
                                next_gate[pos_next_one] = Element.ONE_COND
                                next_gate[pos_flip] = Element.FLIP
                                circuit.pop(i + 2)
                                finished = False
                            elif pos_one != pos_next_one and pos_one != pos_next_flip and pos_one == pos_next_next_flip and pos_flip == pos_next_flip and pos_flip != pos_next_next_one and pos_flip != pos_next_next_flip and pos_next_one == pos_next_next_one:
                                # Match 3.2
                                gate[pos_one] = Element.FLIP
                                gate[pos_flip] = Element.NULL_GATE
                                gate[pos_next_one] = Element.ONE_COND

                                next_gate[pos_one] = Element.ONE_COND
                                next_gate[pos_next_one] = Element.NULL_GATE
                                next_gate[pos_next_flip] = Element.FLIP

                                circuit.pop(i + 2)
                                finished = False
                            elif pos_one != pos_next_one and pos_one != pos_next_flip and pos_one == pos_next_next_one and pos_flip == pos_next_one and pos_flip == pos_next_next_flip and pos_next_flip != pos_next_next_flip and pos_next_flip != pos_next_next_one:
                                # Match 4.6
                                gate[pos_one] = Element.NULL_GATE
                                gate[pos_flip] = Element.ONE_COND
                                gate[pos_next_flip] = Element.FLIP

                                next_gate[pos_one] = Element.ONE_COND
                                next_gate[pos_next_one] = Element.NULL_GATE
                                next_gate[pos_next_flip] = Element.FLIP

                                circuit.pop(i + 2)
                                finished = False
                        elif next_next_one_count == 2:
                            # Match 3.3
                            pos_flip = gate.index(Element.FLIP)
                            pos_one = gate.index(Element.ONE_COND)

                            pos_next_one = next_gate.index(Element.ONE_COND)
                            pos_next_flip = next_gate.index(Element.FLIP)
                            indexes = [index for index, value in enumerate(next_next_gate) if value == Element.ONE_COND]

                            pos_next_next_flip = next_next_gate.index(Element.FLIP)

                            if pos_flip != pos_next_flip and pos_flip != pos_next_one and (pos_flip == indexes[0] or pos_flip == indexes[1]) and pos_one == pos_next_one and (pos_one == indexes[0] or pos_one == indexes[1]) and pos_next_flip == pos_next_next_flip:
                                gate[pos_flip] = Element.ONE_COND
                                gate[pos_next_flip] = Element.FLIP

                                next_gate[pos_flip] = Element.FLIP
                                next_gate[pos_next_flip] = Element.NULL_GATE
                                circuit.pop(i + 2)
                                finished = False
                    elif next_one_count == 2:
                        if next_next_one_count == 1:
                            # Match 4.5
                            pos_flip = gate.index(Element.FLIP)
                            pos_one = gate.index(Element.ONE_COND)
                            pos_next_flip = next_gate.index(Element.FLIP)
                            indexes = [index for index, value in enumerate(next_gate) if value == Element.ONE_COND]
                            pos_next_next_flip = next_next_gate.index(Element.FLIP)
                            pos_next_next_one = next_next_gate.index(Element.ONE_COND)

                            if (pos_one == indexes[0] or pos_one == indexes[1]) and pos_one == pos_next_next_one and (pos_flip == indexes[0] or pos_flip == indexes[1]) and pos_flip == pos_next_next_flip:
                                gate[pos_one] = Element.ONE_COND
                                gate[pos_flip] = Element.ONE_COND
                                gate[pos_next_flip] = Element.FLIP

                                next_gate[pos_one] = Element.ONE_COND
                                next_gate[pos_flip] = Element.NULL_GATE

                                circuit.pop(i + 2)
                                finished = False
                elif one_count == 2:
                    if next_one_count == 0:
                        if next_next_one_count == 2:
                            # Match 4.3
                            pos_flip = gate.index(Element.FLIP)
                            indexes = [index for index, value in enumerate(gate) if value == Element.ONE_COND]

                            pos_next_flip = next_gate.index(Element.FLIP)
                            next_next_indexes = [index for index, value in enumerate(next_next_gate) if value == Element.ONE_COND]
                            pos_next_next_flip = next_next_gate.index(Element.FLIP)

                            if indexes[0] in next_next_indexes and indexes[1] in next_next_indexes and pos_flip == pos_next_next_flip and pos_next_flip in indexes and pos_next_flip in next_next_indexes:
                                filtered_indexes = [value for value in indexes if value != pos_next_flip]

                                gate[pos_next_flip] = Element.FLIP
                                gate[filtered_indexes[0]] = Element.NULL_GATE
                                gate[pos_flip] = Element.NULL_GATE

                                next_gate[pos_next_flip] = Element.NULL_GATE

                                next_gate[filtered_indexes[0]] = Element.ONE_COND
                                next_gate[pos_flip] = Element.FLIP

                                circuit.pop(i + 2)
                                finished = False
                    elif next_one_count == 1:
                        if next_next_one_count == 2:
                            # Match 4.2
                            pos_flip = gate.index(Element.FLIP)
                            indexes = [index for index, value in enumerate(gate) if value == Element.ONE_COND]

                            pos_next_flip = next_gate.index(Element.FLIP)
                            pos_next_one = next_gate.index(Element.ONE_COND)

                            next_next_indexes = [index for index, value in enumerate(next_next_gate) if
                                                 value == Element.ONE_COND]
                            pos_next_next_flip = next_next_gate.index(Element.FLIP)
                            if (indexes[0] in next_next_indexes and indexes[1] in next_next_indexes and pos_flip == pos_next_next_flip and pos_next_one in indexes and pos_next_flip in indexes):
                                gate[pos_next_flip] = Element.FLIP
                                gate[pos_flip] = Element.NULL_GATE


                                next_gate[pos_next_flip] = Element.NULL_GATE
                                next_gate[pos_flip] = Element.FLIP
                                circuit.pop(i + 2)
                                finished = False
                    elif next_one_count == 2:
                        if next_next_one_count == 2:
                            # MAtch 5.1
                            pos_flip = gate.index(Element.FLIP)
                            indexes = [index for index, value in enumerate(gate) if value == Element.ONE_COND]

                            pos_next_flip = next_gate.index(Element.FLIP)
                            next_indexes = [index for index, value in enumerate(next_gate) if value == Element.ONE_COND]

                            pos_next_next_flip = next_next_gate.index(Element.FLIP)
                            next_next_indexes = [index for index, value in enumerate(next_next_gate) if value == Element.ONE_COND]

                            if (((indexes[0] in next_indexes and indexes[0] in next_next_indexes and (indexes[1] == pos_next_flip and indexes[1] in next_next_indexes)) or (indexes[1] in next_indexes and indexes[1] in next_next_indexes and (indexes[0] == pos_next_flip and indexes[0] in next_next_indexes)) and pos_flip == pos_next_next_flip and pos_flip in next_indexes)):
                                filtered_indexes = [value for value in indexes if value != pos_next_flip]
                                gate[filtered_indexes[0]] = Element.NULL_GATE

                                next_next_gate[filtered_indexes[0]] = Element.NULL_GATE
                                finished = False
    return circuit
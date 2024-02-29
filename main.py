import sys
from tt_parser import *
from one_pass_synthesis import *
from bi_directional_synthesis import *
from template_matching import *
from bdd_synthesis import *

if __name__ == '__main__':
    (file_path, method) = sys.argv[1:]
    tt = getTruthTable(file_path)
    if method == "uni":
        one_pass_synthesis(tt, False)
    elif method == "uni_opt":
        one_pass_synthesis(tt)
    elif method == "uni_temp":
        tt_circuit_To_String(reduce(bi_one_pass_synthesis(tt)))
    elif method == "bi":
        bi_one_pass_synthesis(tt)
    elif method == "bi_temp":
        tt_circuit_To_String(reduce(bi_one_pass_synthesis(tt)))
    elif method == "bdd":
        bdd_circuit_to_string(bdd_based_synthesis(tt))
    else:
        print("method does not exist")
        exit(1)



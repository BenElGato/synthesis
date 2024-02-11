from parser import getTruthTable
from one_pass_synthesis import *

tt = getTruthTable("bidirectional_example.txt")

one_pass_synthesis(tt)
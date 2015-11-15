import sys
import naturalSelection as ns
if len(sys.argv) < 2:
    print("usage is: " + sys.argv[0] + " <graphFilename>")
    sys.exit(1)
with open(sys.argv[1]) as f:
    simulation = ns.loadGraph(f)
print(ns.MRCA(simulation))
# TODO testcase
#print([(i, simulation["graph"].node[i]["descendants"]) for i in simulation["graph"].node])
# TODO testcase
#print([(i, simulation["graph"].node[i]["genotype"]) for i in simulation["graph"].node])
#for key in simulation["graph"].node:
#   print(simulation["graph"].node[key]["descendants"])

#for key in simulation["graph"].node:
#   print(simulation["graph"].node[key]["visitedBy"])

#print(len(simulation["lastGeneration"]))

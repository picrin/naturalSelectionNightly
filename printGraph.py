import sys
import naturalSelection as ns
import networkx as nx
import matplotlib.pyplot as plt
if len(sys.argv) < 2:
    print("usage is: " + sys.argv[0] + " <graphFilename>")
    sys.exit(1)
with open(sys.argv[1]) as f:
    simulation = ns.loadGraph(f)

nx.draw_networkx(simulation['graph'])
print(ns.MRCA(simulation))
plt.show()


# TODO testcase
# print([(i, simulation["graph"].node[i]["descendants"]) for i in simulation["graph"].node])
# print([(i, simulation["graph"].node[i]["genotype"]) for i in simulation["graph"].node])
# TODO testcase
# for key in simulation["graph"].node:
#   print(simulation["graph"].node[key]["descendants"])

#for key in simulation["graph"].node:
#   print(simulation["graph"].node[key]["visitedBy"])

#print(len(simulation["lastGeneration"]))

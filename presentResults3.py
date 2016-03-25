from naturalSelection import *
import matplotlib.pyplot as plt
import sys, csv

proportions = []
mrca = []
i = 0

with open(sys.argv[1], "r") as sims:
    g = loadGraph(sims)
    for genNo, _ in enumerate(g["generations"]):
        ap = alleleProportion(g, genNo)
        m = quickMRCA(g, i, 200)[1]
        i += 1
        proportions.append(ap)
        mrca.append(m)
        print(ap)

plt.plot(proportions)
plt.plot(mrca)
plt.ylim([0,250])
plt.show()

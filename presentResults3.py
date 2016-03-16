from naturalSelection import *
import matplotlib.pyplot as plt
import sys, csv

proportions = []
with open(sys.argv[1], "r") as sims:
    g = loadGraph(sims)
    for genNo, _ in enumerate(g["generations"]):
        ap = alleleProportion(g, genNo)
        proportions.append(ap)
        print(ap)

plt.plot(proportions)
plt.show()

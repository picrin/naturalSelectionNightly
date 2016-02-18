import matplotlib.pyplot as plt
import sys, csv
with open(sys.argv[1], "r") as csvFile:
    parsed = csv.reader(csvFile, delimiter=" ")
    print parsed
    hasFeature = [row[1] for row in parsed]
    print hasFeature

plt.plot(hasFeature)
plt.show()

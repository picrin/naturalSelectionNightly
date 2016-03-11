import csv, os, os.path
resultDir = "wandererResults"

def splitAndKeep(string, delimiters):
    currentLeft = 0
    for i, char in enumerate(string):
        if char in delimiters:
            yield string[currentLeft:i]
            yield string[i:i+1]
            currentLeft = i+1
    yield string[currentLeft:]

def processLines(lines):
    for line in lines:
        twoElem = line.rstrip("\n").split(",")
        if twoElem[0] != "None":
            yield list(map(int, twoElem))

lsresult = os.listdir(resultDir)
unlucky = {}
lucky = {}

for result in lsresult:
    terms = list(splitAndKeep(result, ["_", ":"]))
    typeIndex = terms.index("typ")
    if terms[typeIndex + 2] == "mrca":
        sizIndex = terms.index("siz")
        sizNo = int(terms[sizIndex + 2])
        mrcaPath = os.path.join(resultDir, "".join(terms))
        with open(mrcaPath, "r") as csvFile:
            lines = csvFile.readlines()
            assert(len(lines) == 101)
            lines = list(processLines(lines))
            lastBit = lines[-1][1]
            #print(lastBit)
            if lastBit == 0:
                try:
                    unlucky[sizNo]
                except KeyError as e:
                    unlucky[sizNo] = []
                finally:
                    unlucky[sizNo].append([line[0] for line in lines])
            else:
                try:
                    lucky[sizNo]
                except KeyError as e:
                    lucky[sizNo] = []
                finally:
                    lucky[sizNo].append([line[0] for line in lines])
                #print(mrcaPath)
import scipy.stats
for key in lucky:
    print("population size", key)
    size = 2*len(lucky[key])
    luckyPoints = lucky[key]
    unluckyPoints = unlucky[key][:size]
    bothPoints = luckyPoints + unluckyPoints[:size/2]
    #print(bothPoints)
    assert(2*len(luckyPoints) == len(unluckyPoints))
    _, baseline = scipy.stats.kruskal(*unluckyPoints)
    _, experiment = scipy.stats.kruskal(*bothPoints)
    print("sample size:", size)
    print("baseline (controls) p-value", baseline, "50% selective sweep, 50% controls p-value", experiment, "is baseline > experiment*20", baseline > experiment*20)


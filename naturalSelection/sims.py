from pointPicking import *
import random
import math

def createGenotype():
    return {"isDominant":None, "hasCopy1":None, "hasCopy2":None}

def createSim():
    return {"genotype":{None, None, None}, "pos":{None, None}, "parentA":None, "parentB":None, "isMale":None}

def createRandomlyPositionedSim():
    sim = createSim()
    sim["genotype"] = {False, False, False}
    sim["isMale"] = random.randint(0, 1)
    sim["pos"] = pickPoint()
    return sim

def getRandomCopy(sim):
    if random.randint(0, 1):
        return sim["genotype"]["hasCopy1"]
    return sim["genotype"]["hasCopy2"]

def createSimFromParents(parentA, parentB):
    sim = createSim()
    sim["genotype"]["hasCopy1"] = getRandomCopy(parentA)
    sim["genotype"]["hasCopy2"] = getRandomCopy(parentB)
    sim["isMale"] = random.randint(0, 1)

def makeSimWanderer(sim):
    sim["pos"] = pickPoint()

def makeSimHomebody(sim, maximumDistance):
    sim["pos"] = moveOnSphere(sim["pos"], random.uniform(0, 2 * math.pi), random.uniform(0, maximumDistance))

def hasFeature(genotype):
    if genotype is None or genotype["isDominant"] is None or genotype["hasCopy1"] is None or genotype["hasCopy2"] is None:
        raise ValueError("genotype has not been initialised")
    if genotype["isDominant"]:
        return genotype["hasCopy1"] and genotype["hasCopy2"]
    elif genotype["isRecessive"]:
        return genotype["hasCopy1"] or genotype["hasCopy2"]


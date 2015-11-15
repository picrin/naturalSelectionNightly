from .pointPicking import *
import random
import math

def createGenotype():
    return {"isDominant": None, "hasCopy1": False, "hasCopy2": False}

uid = 0

def changeUID(newUID):
    global uid
    uid = newUID

def createSim():
    global uid
    sim = {"genotype": createGenotype(), "pos": (None, None), "parentA": None, "parentB": None, "isMale": None, "uid": uid}
    uid += 1
    return sim
        
def makeDominant(sim):
    sim["genotype"]["isDominant"] = True
    return sim

def makeRecessive(sim):
    sim["genotype"]["isDominant"] = False
    return sim

def hasFeature(sim):
    genotype = sim["genotype"]
    if genotype["isDominant"] is None or genotype["hasCopy1"] is None or genotype["hasCopy2"] is None:
        raise ValueError("gene dominance or genotype have not been initialised")
    if genotype["isDominant"]:
        return genotype["hasCopy1"] or genotype["hasCopy2"]
    else:
        return genotype["hasCopy1"] and genotype["hasCopy2"]

def createRandomlyPositionedSim():
    sim = createSim()
    sim["isMale"] = random.randint(0, 1)
    sim["pos"] = pickPoint()
    return sim

def getRandomGeneCopy(sim):
    if random.randint(0, 1):
        return sim["genotype"]["hasCopy1"]
    return sim["genotype"]["hasCopy2"]

def setRandomGeneCopy(sim, val):
    if random.randint(0, 1):
        sim["genotype"]["hasCopy1"] = val
    else:
        sim["genotype"]["hasCopy2"] = val

def createSimFromParents(parentA, parentB):
    if parentA["isMale"] == parentB["isMale"]:
        raise ValueError("can't breed sims of the same gender")
    if parentA["isMale"]:
        mother = parentB
    else:
        mother = parentA
    sim = createSim()
    sim["pos"] = mother["pos"]
    sim["parentA"] = parentA
    sim["parentB"] = parentB
    sim["genotype"]["hasCopy1"] = getRandomGeneCopy(parentA)
    sim["genotype"]["hasCopy2"] = getRandomGeneCopy(parentB)
    assert(parentA["genotype"]["isDominant"] == parentB["genotype"]["isDominant"])
    sim["genotype"]["isDominant"] = parentA["genotype"]["isDominant"]
    sim["isMale"] = random.randint(0, 1)
    return sim

def moveWanderer(sim):
    if sim["pos"] == None:
        raise ValueError("sim's position need not be None if the sim is a Wanderer. You can get an initialised sim by creating it with createRandomlyPositionedSim()") 
    sim["pos"] = pickPoint()
    return sim["pos"]

def moveHomebody(sim, maximumDistance):
    if sim["pos"] == None:
        raise ValueError("sim's position need not be None if the sim is a Homebody. You can get an initialised sim by creating it with createRandomlyPositionedSim()")
    randomBearing = random.uniform(0, 2 * math.pi)
    randomDistance = random.uniform(0, maximumDistance)
    sim["pos"] = moveOnSphere(sim["pos"], randomBearing, randomDistance)
    return sim["pos"]

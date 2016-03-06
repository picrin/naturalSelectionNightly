import json
import collections
import random
#networkx is imported lazily so that pypy doesn't complain.

def loadGraph(fileObj, fromVar=None):
    """
    fileObj is a file representation of the population graph generated and written to disk by one of
    generatePopulation* functions from generateGraph module.
    Returns a simulation: a set of all sims represented as a networkx graph, and lists of uids of
    respectively first and last generation sims, to facilitate navigation of the graph.
    """
    import networkx
    simsGraph = networkx.DiGraph()
    if fileObj is not None:
        sims = json.load(fileObj)
    else:
        if fromVar is not None:
            sims = fromVar
    first = []
    last = []
    generations = []
    for sim in sims:
        sim["visitedBy"] = -1
        sim["descendants"] = 0
        sim["children"] = []
        simsGraph.add_node(sim["uid"], sim)
        for parent in ["parentA", "parentB"]:
            if sim[parent] is not None:
                simsGraph.add_edge(sim[parent], sim["uid"])
        if sim["generation"] == "last":
            last.append(sim["uid"])
        if sim["generation"] == "first":
            first.append(sim["uid"])
        genNo = sim["generationNo"]
        if genNo >= len(generations):
            generations.append([])
        generations[genNo].append(sim["uid"])
    simulation = {"graph": simsGraph, "firstGeneration": first, "lastGeneration": last, "generations": generations}
    return simulation

def getSimByID(simulation, ID):
    return simulation["graph"].node[ID]

def reinitialiseSims(simulation):
    for simUID in simulation["graph"]:
        sim = getSimByID(simulation, simUID)
        sim["visitedBy"] = -1
        sim["descendants"] = 0

def countDescendants(simulation):
    def countDescendantsInner(nodeID, uid):
        node = getSimByID(simulation, nodeID)
        if node["visitedBy"] == uid:
            return
        else:
            node["descendants"] += 1
            node["visitedBy"] = uid
            if node["parentA"] is not None:
                countDescendantsInner(node["parentA"], uid)
            if node["parentB"] is not None:
                countDescendantsInner(node["parentB"], uid)
    for nodeID in simulation["lastGeneration"]:
        countDescendantsInner(nodeID, nodeID)

def MRCA(simulation):
    """
    Finds an ancestor of entire population, whose distance from all sims in the last generation is the smallest,
    with the distance between any two sims defined only when they are related, and is an integer equal to 
    the number of generations that separate them.
    
    For example, assume that A -> B means that A is a parent of B. Then if A -> B and B -> C we can say that the distance
    between A and A is 0, A and B is 1 and A and C is 2.
    Returns the value 
    """
    countDescendants(simulation)
    fifo = {}
    for i in simulation["lastGeneration"]:
        fifo[i] = True
    lastGenerationCount = len(simulation["lastGeneration"])
    generationNo = 0
    while len(fifo) != 0:
        newFifo = {}
        for key in fifo:
            exploreNode = getSimByID(simulation, key)
            if exploreNode["descendants"] == lastGenerationCount:
                return key, generationNo
            A = exploreNode["parentA"]
            B = exploreNode["parentB"]
            for parent in [A, B]:
                if parent is not None and parent not in newFifo:
                    newFifo[parent] = True
        fifo = newFifo
        generationNo += 1
    return None

def computeTracer(simulation, simID):
    sim = getSimByID(simulation, simID)
    childrenIDs = sim["children"]
    if childrenIDs:
        currentTracer = []
        for childID in childrenIDs:
            childTracer = getSimByID(simulation, childID)["tracers"]
            if not currentTracer:
                currentTracer = childTracer 
            else:
                currentTracer = [i or j for i, j in zip(currentTracer, childTracer)]
        sim["tracers"] = currentTracer
    elif sim["tracers"]:
        pass
    else:
        raise Exception("children empty ?!")

def initTracers(simulation, simIDs):
    translation = [0] * len(simIDs)
    reverseTranslation = {}
    for i, simID in enumerate(simIDs):
        sim = getSimByID(simulation, simID)
        translation[i] = simID
        reverseTranslation[simID] = i
        tracers = [False] * len(simIDs)
        tracers[i] = True
        sim["tracers"] = tracers
    return translation, reverseTranslation
    
def cleanupTracers(simulation, simIDs):
    for i, simID in enumerate(simIDs):
        sim = getSimByID(simulation, simID)
        sim["tracers"] = None

def quickMRCA(simulation, generationNo, tracersNo):
    if generationNo < 0:
        generationNo = len(simulation["generations"]) + generationNo
    frontier = simulation["generations"][generationNo]
    oldFrontier = []
    random.shuffle(frontier)
    frontier = frontier[:tracersNo]
    for simID in frontier:
        initTracers(simulation, frontier)
    currentGen = generationNo
    while True:
        nextFrontier = {}
        #print("Frontier")
        #print(frontier)
        #print("Old Frontier")
        #print(oldFrontier)
        for simID in frontier:
            sim = getSimByID(simulation, simID)
            computeTracer(simulation, simID)
            #print(sim["tracers"])
            if all(sim["tracers"]):
                returnGen = sim["generationNo"]
                return simID, generationNo - returnGen
            for parentID in [sim["parentA"], sim["parentB"]]:
                nextFrontier[parentID] = True
                parent = getSimByID(simulation, parentID)
                #if simID not in parent["children"]:
                parent["children"].append(simID)
        cleanupTracers(simulation, oldFrontier)            
        oldFrontier = frontier
        frontier = [key for key in nextFrontier]
        currentGen -= 1
        if currentGen == 0:
            return None

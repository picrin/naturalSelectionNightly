import random, sys, pickle
import naturalSelection.testModule
filename = ".randomstate"
if len(sys.argv) > 1:
    if sys.argv[1] == "load":
        with open(filename, "rb") as randomstate:
            random.setstate(pickle.load(randomstate))
        print ("random state loaded from " + filename)
with open(filename, "wb") as randomstate:
    pickle.dump(random.getstate(), randomstate, 2)
print("random state dumped to " + filename)
naturalSelection.testModule.runAll()

from naturalSelection import *
initialSize = 1000
step = 100
steps = 0
repetitions = 5
results = []

def estimateGenerations(size):
    return int(math.ceil(math.log(500 * size + 1000)))

for size in range(initialSize, initialSize + steps * step + 1, step):
    for i in range(repetitions):
        print(estimateGenerations(size))
        results.append({"initialSize": size, "sizePerGeneration": None, "MRCA": None, "filename": None, "generations": estimateGenerations(size)})
print(len(results))


def noGenesWanderers(size, generations):
    def firstGeneration():
       return simsFrame(populationSize = size, mutator = oneDominantAlleleMutator)
    def nextGeneration(nextFrame):
       return nextFrame(migrator=wandererMigrator, breeder=simpleProximityBreeder)
    return generatePopulationPure(generations, firstGeneration, nextGeneration)

def noGenesHomebodies():
    pass

filenameSuffix = 1
print results
for result in results:
    print(result["initialSize"], result["generations"])
    simulation = list(noGenesWanderers(result["initialSize"], result['generations']))
    sizePerGeneration = []
    for generation in simulation:
        sizePerGeneration.append(len(generation))
    path = "./results/noGenesWanderers" + str(filenameSuffix)
    filenameSuffix += 1
    with open(path, "w") as fileobj:
        writePopulation(fileobj, (generation for generation in simulation))
    with open(path, "r") as fileobj:
        simulation = loadGraph(fileobj)
    result["sizePerGeneration"] = sizePerGeneration
    result["MRCA"] = MRCA(simulation)[1]
    result["filename"] = path
    
print(results)

"""
[{'MRCA': 6, 'sizePerGeneration': [100, 77, 79, 82, 73, 68, 71, 81, 83, 79, 66, 62, 69, 72, 73, 73], 'initialSize': 100, 'filename': './data/noGenesWanderers1'}, {'MRCA': 5, 'sizePerGeneration': [100, 96, 60, 56, 47, 42, 42, 44, 55, 43, 33, 22, 28, 21, 15, 14], 'initialSize': 100, 'filename': './data/noGenesWanderers2'}, {'MRCA': 7, 'sizePerGeneration': [100, 109, 101, 100, 105, 114, 113, 106, 121, 132, 128, 132, 126, 132, 133, 134], 'initialSize': 100, 'filename': './data/noGenesWanderers3'}, {'MRCA': 6, 'sizePerGeneration': [100, 103, 84, 90, 90, 86, 66, 63, 66, 48, 52, 50, 40, 45, 35, 31], 'initialSize': 100, 'filename': './data/noGenesWanderers4'}, {'MRCA': 5, 'sizePerGeneration': [100, 87, 81, 89, 76, 75, 73, 72, 54, 46, 45, 36, 38, 47, 28, 21], 'initialSize': 100, 'filename': './data/noGenesWanderers5'}, {'MRCA': 6, 'sizePerGeneration': [100, 98, 105, 104, 95, 98, 83, 87, 80, 73, 73, 84, 82, 72, 68, 51], 'initialSize': 100, 'filename': './data/noGenesWanderers6'}, {'MRCA': 5, 'sizePerGeneration': [100, 80, 80, 83, 77, 70, 82, 84, 80, 75, 60, 50, 45, 47, 38, 28], 'initialSize': 100, 'filename': './data/noGenesWanderers7'}, {'MRCA': 4, 'sizePerGeneration': [100, 96, 74, 68, 51, 46, 41, 43, 32, 35, 33, 27, 23, 20, 12, 6], 'initialSize': 100, 'filename': './data/noGenesWanderers8'}, {'MRCA': 6, 'sizePerGeneration': [100, 108, 98, 95, 99, 96, 90, 95, 87, 77, 64, 61, 54, 54, 54, 34], 'initialSize': 100, 'filename': './data/noGenesWanderers9'}, {'MRCA': 5, 'sizePerGeneration': [100, 111, 92, 81, 82, 74, 81, 85, 66, 58, 40, 38, 42, 42, 31, 31], 'initialSize': 100, 'filename': './data/noGenesWanderers10'}, {'MRCA': 7, 'sizePerGeneration': [300, 293, 285, 308, 275, 275, 256, 244, 208, 197, 215, 222, 216, 218, 212, 205], 'initialSize': 300, 'filename': './data/noGenesWanderers11'}, {'MRCA': 8, 'sizePerGeneration': [300, 302, 294, 288, 294, 281, 273, 262, 252, 255, 253, 216, 203, 208, 173, 197], 'initialSize': 300, 'filename': './data/noGenesWanderers12'}, {'MRCA': 7, 'sizePerGeneration': [300, 299, 255, 260, 220, 190, 188, 176, 170, 176, 152, 129, 125, 125, 115, 106], 'initialSize': 300, 'filename': './data/noGenesWanderers13'}, {'MRCA': 8, 'sizePerGeneration': [300, 274, 247, 236, 219, 202, 199, 182, 159, 163, 136, 137, 138, 118, 102, 92], 'initialSize': 300, 'filename': './data/noGenesWanderers14'}, {'MRCA': 8, 'sizePerGeneration': [300, 300, 294, 292, 287, 258, 225, 236, 226, 220, 227, 226, 226, 205, 196, 176], 'initialSize': 300, 'filename': './data/noGenesWanderers15'}, {'MRCA': 9, 'sizePerGeneration': [300, 297, 344, 337, 333, 352, 371, 374, 337, 312, 325, 281, 283, 278, 301, 290], 'initialSize': 300, 'filename': './data/noGenesWanderers16'}, {'MRCA': 9, 'sizePerGeneration': [300, 314, 320, 334, 326, 309, 327, 315, 312, 309, 299, 298, 312, 291, 305, 302], 'initialSize': 300, 'filename': './data/noGenesWanderers17'}, {'MRCA': 9, 'sizePerGeneration': [300, 292, 313, 339, 323, 324, 293, 298, 304, 350, 341, 317, 305, 278, 277, 284], 'initialSize': 300, 'filename': './data/noGenesWanderers18'}, {'MRCA': 8, 'sizePerGeneration': [300, 260, 253, 247, 241, 221, 219, 221, 214, 190, 222, 231, 240, 207, 200, 196], 'initialSize': 300, 'filename': './data/noGenesWanderers19'}, {'MRCA': 7, 'sizePerGeneration': [300, 277, 236, 233, 231, 205, 148, 135, 117, 118, 114, 112, 117, 123, 106, 98], 'initialSize': 300, 'filename': './data/noGenesWanderers20'}, {'MRCA': 8, 'sizePerGeneration': [500, 480, 444, 365, 384, 380, 364, 326, 315, 314, 303, 307, 291, 272, 277, 304], 'initialSize': 500, 'filename': './data/noGenesWanderers21'}, {'MRCA': 10, 'sizePerGeneration': [500, 504, 537, 535, 516, 511, 492, 486, 468, 458, 462, 470, 478, 433, 410, 387], 'initialSize': 500, 'filename': './data/noGenesWanderers22'}, {'MRCA': 10, 'sizePerGeneration': [500, 507, 489, 513, 537, 572, 558, 526, 523, 528, 545, 541, 527, 521, 572, 560], 'initialSize': 500, 'filename': './data/noGenesWanderers23'}, {'MRCA': 9, 'sizePerGeneration': [500, 511, 555, 579, 573, 560, 524, 474, 440, 445, 415, 396, 402, 413, 384, 397], 'initialSize': 500, 'filename': './data/noGenesWanderers24'}, {'MRCA': 10, 'sizePerGeneration': [500, 520, 491, 475, 470, 465, 496, 490, 507, 532, 509, 499, 523, 532, 519, 456], 'initialSize': 500, 'filename': './data/noGenesWanderers25'}, {'MRCA': 9, 'sizePerGeneration': [500, 501, 472, 425, 374, 368, 384, 365, 342, 309, 293, 305, 320, 275, 299, 249], 'initialSize': 500, 'filename': './data/noGenesWanderers26'}, {'MRCA': 10, 'sizePerGeneration': [500, 524, 508, 501, 487, 473, 480, 469, 457, 482, 468, 476, 501, 540, 504, 463], 'initialSize': 500, 'filename': './data/noGenesWanderers27'}, {'MRCA': 9, 'sizePerGeneration': [500, 509, 507, 523, 551, 570, 511, 479, 461, 463, 444, 434, 400, 431, 391, 367], 'initialSize': 500, 'filename': './data/noGenesWanderers28'}, {'MRCA': 10, 'sizePerGeneration': [500, 480, 455, 453, 442, 447, 460, 500, 501, 510, 531, 535, 583, 585, 603, 565], 'initialSize': 500, 'filename': './data/noGenesWanderers29'}, {'MRCA': 9, 'sizePerGeneration': [500, 495, 490, 460, 447, 434, 408, 446, 449, 427, 365, 340, 341, 348, 302, 286], 'initialSize': 500, 'filename': './data/noGenesWanderers30'}, {'MRCA': 10, 'sizePerGeneration': [700, 695, 724, 703, 695, 668, 668, 677, 681, 671, 653, 650, 634, 616, 549, 548], 'initialSize': 700, 'filename': './data/noGenesWanderers31'}, {'MRCA': 10, 'sizePerGeneration': [700, 712, 778, 791, 791, 802, 779, 810, 828, 828, 885, 958, 938, 1012, 990, 989], 'initialSize': 700, 'filename': './data/noGenesWanderers32'}, {'MRCA': 10, 'sizePerGeneration': [700, 694, 674, 614, 616, 580, 554, 574, 575, 598, 567, 551, 534, 548, 540, 552], 'initialSize': 700, 'filename': './data/noGenesWanderers33'}, {'MRCA': 10, 'sizePerGeneration': [700, 737, 686, 667, 668, 654, 679, 657, 618, 621, 631, 614, 650, 647, 638, 667], 'initialSize': 700, 'filename': './data/noGenesWanderers34'}, {'MRCA': 10, 'sizePerGeneration': [700, 718, 745, 761, 779, 753, 781, 804, 824, 841, 885, 881, 887, 913, 967, 959], 'initialSize': 700, 'filename': './data/noGenesWanderers35'}, {'MRCA': 10, 'sizePerGeneration': [700, 744, 723, 721, 693, 684, 684, 710, 712, 710, 777, 743, 751, 767, 790, 815], 'initialSize': 700, 'filename': './data/noGenesWanderers36'}, {'MRCA': 10, 'sizePerGeneration': [700, 686, 692, 665, 690, 713, 676, 628, 646, 660, 649, 666, 687, 695, 652, 686], 'initialSize': 700, 'filename': './data/noGenesWanderers37'}, {'MRCA': 10, 'sizePerGeneration': [700, 700, 682, 725, 759, 726, 711, 762, 742, 736, 719, 740, 749, 792, 841, 845], 'initialSize': 700, 'filename': './data/noGenesWanderers38'}, {'MRCA': 10, 'sizePerGeneration': [700, 723, 712, 706, 707, 757, 783, 754, 698, 721, 729, 719, 713, 714, 709, 679], 'initialSize': 700, 'filename': './data/noGenesWanderers39'}, {'MRCA': 10, 'sizePerGeneration': [700, 660, 684, 663, 685, 700, 698, 689, 681, 679, 719, 713, 736, 749, 762, 748], 'initialSize': 700, 'filename': './data/noGenesWanderers40'}]
"""

import math
def sigmaBinomial(n, p, howManySigma):
    return howManySigma * math.sqrt(n * (1 - p) * (p))

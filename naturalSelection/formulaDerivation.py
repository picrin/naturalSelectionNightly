from sage.all import *

#lambda is geographic longitude
lam = var('lam')
#psi is geographic latitude
psi = var('psi')

theta = var('theta')
delta = var('delta')

p = vector([sin(lam)*cos(psi), sin(psi), cos(lam)*cos(psi)])

t = vector([sin(lam)*sin(psi), -cos(psi), cos(lam)*sin(psi)])

def crossMatrix(vector):
    return matrix([[0, -vector[2], vector[1]],
                   [vector[2], 0, -vector[0]],
                   [-vector[1], vector[0], 0]])

def rotatePointAroundUnitVector(point, unitVector, angle, clockwise=True):
    if clockwise:
        sineDirection = -1
    else:
        sineDirection = +1
    K = crossMatrix(unitVector)
    Id = Matrix.identity(3)
    R = Id + sineDirection * sin(angle) * K + (1 - cos(angle)) * K * K
    return R * point 
    
def rotatePointDifferent(point, unitVector, angle):
    return point*cos(angle) + unitVector.cross_product(point)*sin(angle) + unitVector * (unitVector.dot_product(point)) * (1 - cos(angle))

# that's the bearing
b = rotatePointAroundUnitVector(t, p, theta, clockwise=True).simplify_full()

# this is the new coordinate
n = rotatePointAroundUnitVector(p, crossMatrix(b) * p, delta, clockwise=False).simplify_full()
psi_n = asin(n[1]).simplify_full()
lam_n = (acos(n[2]/cos(psi_n))).simplify_full()

print("formula for psi_new, where psi is the geographical latitude, theta is the bearing and delta is the distance on a unit sphere", str(psi_n))
print("formula for lam_new, where lam is the geographical longitude, theta is the bearing and delta is the distance on a unit sphere", str(lam_n))

#import inspect
#print(inspect.getfile(lam_n.__str__))

# psi = 53 N
# lam = 22 E
# delta = 1
# theta = 96
# psi_n ?= 22 (0.38)
# lamb_n ?= 65 (1.13)

rtd = (180/pi).n()
dtr = (pi/180).n()

example_kwargs = {"lam":22*dtr, "psi":53*dtr, "theta":96*dtr, "delta":1}
def evaluateCoords(kwargs):
    print("psi", psi.subs(**kwargs).n())
    print("psi_deg", psi.subs(**kwargs).n()*rtd)
    print("lam", lam.subs(**kwargs).n())
    print("lam_deg", lam.subs(**kwargs).n()*rtd)
    print("b", b.subs(**kwargs).n())
    print("t", t.subs(**kwargs).n())
    print("n", n.subs(**kwargs).n())
    print("psi_new", psi_n.subs(**kwargs).n())
    print("psi_deg_new", psi_n.subs(**kwargs).n()*rtd)
    print("lam_new", lam_n.subs(**kwargs).n())
    print("lam_new_deg", lam_n.subs(**kwargs).n()*rtd)

# uncomment to test move with parameters example_kwargs
# evaluateCoords(example_kwargs)

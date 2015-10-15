from sage.all import *
#lambda is geogra
lam = var('lam')
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

b = rotatePointAroundUnitVector(t, p, theta, clockwise=True).simplify_full()

n = rotatePointAroundUnitVector(p, crossMatrix(b)*p, delta, clockwise=False).simplify_full()
psi_n = arcsin(n[1]).simplify_full()
lam_n = (arccos(n[2]/cos(psi_n))).simplify_full()

print(psi_n)
print(lam_n)

# psi = 53 N
# lam = 22 E
# delta = 1
# theta = 96
# psi_n ?= 22 (0.38)
# lamb_n ?= 65 (1.13)

rtd = (180/pi).n()
dtr = (pi/180).n()

kwargs_random = {"lam":22*dtr, "psi":53*dtr, "theta":96*dtr, "delta":1}
def evaluateCoords(kwargs):
    print("psi", psi.subs(**kwargs).n())
    print("psi_deg", psi.subs(**kwargs).n()*rtd)
    print("lam", lam.subs(**kwargs).n())
    print("lam_deg", lam.subs(**kwargs).n()*rtd)
    print("b", b.subs(**kwargs).n())
    print("t", t.subs(**kwargs).n())
    print("n", n.subs(**kwargs).n())
    print("psi_n", psi_n.subs(**kwargs).n())
    print("psi_deg_n", psi_n.subs(**kwargs).n()*rtd)
    print("lam_n", lam_n.subs(**kwargs).n())
    print("lam_n_deg", lam_n.subs(**kwargs).n()*rtd)

evaluateCoords(kwargs_random)
#evaluateCoords({"lam":0.0, "psi":0, "theta":3.14/2, "delta":3.14})
#evaluateCoords({"lam":-pi.n()/4, "psi":pi.n()/4, "theta":1500.190, "delta":8})

#unitVector = vector([-1/2.0, sqrt(2)/2, -1/2.0])
#p = vector([1/2.0, sqrt(2)/2, 1/2.0])
#print("p", p.n())
#print("p.t", (p.dot_product(t)).simplify_full())
#print("t.north", (p.dot_product(vector([0,1,0]))).simplify_full())
#print(unitVector.dot_product(p).n())
#print(rotatePointAroundUnitVector(p, unitVector, pi, clockwise=False).n())
#print(rotatePointDifferent(p, unitVector, pi).n())



import random, math
theta = random.uniform(0, 2*math.pi)

def pickPoint():
    lon = random.uniform(0, 2*math.pi)
    lat = math.asin(random.uniform(-1, 1))
    return lon, lat  

def sphereDistance(point1, point2):
    dlat = point2[1] - point1[1]
    dlon = point2[0] - point1[0]
    a = pow(math.sin(dlat/2), 2) + math.cos(point1[1]) * math.cos(point2[1])  * pow(math.sin(dlon/2), 2)
    return 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

p1 = pickPoint()
p2 = pickPoint()

print(sphereDistance(p1,p2))

Katowice = 0.3319, 0.87732 # 19.0167 E 50.2667 N,
Glasgow = -0.07433, 0.97491 # 4.2590 W 55.8580 N, 

print(math.degrees(0.3319))
print(sphereDistance(Katowice, Glasgow) * 6371)

"""just check that it works
def histogram(psiRange, bucketNo, left, right):
    buckets = [0] * (bucketNo)
    compareTo = [0] * (bucketNo)
    length = (right - left)/float(bucketNo + 1)
    for psi in psiRange:
        for i in range(bucketNo):
            if psi > left + length * i and psi < left + length * (i + 1):
                buckets[i] += 1
    for i in range(bucketNo):
        compareTo[i] = math.cos(left + length * (i + 0.5))*len(psiRange)/bucketNo
    for i in range(bucketNo):
        buckets[i] /= compareTo[i]
    return buckets


buckets = histogram([pickPoint()[1] for i in range(1000000)], 10, -math.pi/2, math.pi/2)     
print("buckets", buckets)
"""


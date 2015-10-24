# testing that the distribution is cosine

# testing that the distance between Katowice and Glasgow is right

# testing that

import unittest
import pointPicking
import math

def histogram(psiRange, bucketNo, left, right):
    buckets = [0] * (bucketNo)
    compareTo = [0] * (bucketNo)
    length = (right - left)/float(bucketNo + 1)
    for psi in psiRange:
        for i in range(bucketNo):
            if psi > left + length * i and psi < left + length * (i + 1):
                buckets[i] += 1
    for i in range(bucketNo):
        compareTo[i] = math.cos(left + length * (i + 0.5))*len(psiRange)/float(bucketNo)
    for i in range(bucketNo):
        buckets[i] /= float(compareTo[i])
    return buckets


class TestPointPicking(unittest.TestCase):
    def test_buckets(self):
        buckets = histogram([pointPicking.pickPoint()[1] for i in range(1000)], 10, -math.pi/2, math.pi/2)
        bucketAvg = sum(buckets)/len(buckets)
        squareSum = sum(map(lambda n: (n-bucketAvg)*2, buckets))
        print(squareSum)
    def test_distance(self):
        Katowice = 0.3319, 0.87732 # 19.0167 E 50.2667 N,
        Glasgow = -0.07433, 0.97491 # 4.2590 W 55.8580 N, 
        print(pointPicking.sphereDistance(Katowice, Glasgow) * 6371)


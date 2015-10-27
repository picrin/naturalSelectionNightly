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

def sumElements(arr):
    value = 0.0
    print(list(arr))
    for _, e in enumerate(arr):
        print(e)
        value += e
    print(value)
    return value

class TestPointPicking(unittest.TestCase):
    def test_buckets(self):
        buckets = histogram([pointPicking.pickPoint()[1] for i in range(500)], 10, -math.pi/2, math.pi/2)
        bucketAvg = sum(buckets)/float(len(buckets))
        diffFromAvgSqr = list(map(lambda n: (n-bucketAvg)**2, buckets))
        sqrSum = sum(diffFromAvgSqr)
        self.assertTrue(sqrSum < 2)
    def test_distance(self):
        Katowice = 0.3319, 0.87732 # 19.0167 E 50.2667 N,
        Glasgow = -0.07433, 0.97491 # 4.2590 W 55.8580 N, 
        self.assertAlmostEqual(pointPicking.sphereDistance(Katowice, Glasgow) * 6371, 1665, delta=1)
    def test_move(self):
        kwargs = {"point":[22*pointPicking.dtr, 53*pointPicking.dtr], "bearing":96*pointPicking.dtr, "distance":1}
        expected = (1.51337078352571, 0.388251208045783)
        result = pointPicking.moveOnSphere(**kwargs)
        self.assertAlmostEqual(expected[0], result[0], delta=0.01)
        self.assertAlmostEqual(expected[1], result[1], delta=0.01)

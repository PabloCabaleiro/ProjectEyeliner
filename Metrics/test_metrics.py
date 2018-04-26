import unittest
from Objects.ResultClass import ResultClass
from Metrics.nearest import NearestMetrics
from Metrics.normal import NormalMetrics
from Metrics.vertical import VerticalMetrics
import math

class TestMetrics(unittest.TestCase):

    data1 = {"lens": [(0,2),(1,2),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,2),(9,2)],
             "cornea": [(0,5),(1,5),(2,3),(3,4),(4,5),(5,4),(6,5),(7,3),(8,5),(9,4)]}
    data2 =  {"lens": [(0,2),(1,2),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,2),(9,2)],
              "cornea": [(2,3),(3,4),(4,5),(5,4),(6,5),(7,3),(8,5)]}
    data3 =  {"lens": [(0,1),(1,2),(2,2),(3,3),(4,5),(5,5),(6,5),(7,3),(8,2),(9,2),(10,1)],
              "cornea": [(0,5),(1,6),(2,6),(3,7),(4,7),(5,6),(6,6),(7,7),(8,5),(9,4),(10,6)]}

    ############################################NEAREST TEST#########################################################

    def test_nearest_normal_case(self):
        expected_results = [math.sqrt(5),math.sqrt(2),2,math.sqrt(5),math.sqrt(8),math.sqrt(8),math.sqrt(5),2,math.sqrt(2),2]
        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i])

    def test_nearesst_different_sizes(self):
        expected_results = [math.sqrt(5),math.sqrt(2),2,math.sqrt(5),math.sqrt(8),math.sqrt(8),math.sqrt(5),2,math.sqrt(2),math.sqrt(5)]
        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i])

    def test_nearest_second_case(self):
        expected_results = [4,math.sqrt(10),math.sqrt(13),math.sqrt(10),math.sqrt(2),1,1,math.sqrt(5),math.sqrt(5),
                            2,math.sqrt(10)]
        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)
        self.assertEqual(len(expected_results), len(metrics.distances))
        for i in range(0, len(expected_results)):
            self.assertAlmostEqual(expected_results[i], metrics.distances[i])

    ###############################################NORMAL TEST########################################################

    def test_normal_normal_case(self):
        expected_results = [3,math.sqrt(2),math.sqrt(20),3,4,3,4,math.sqrt(13),math.sqrt(2),2]
        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = NormalMetrics(result)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i])

    def test_normal_different_sizes(self):
        expected_results = [-1,-1,math.sqrt(20),3,4,3,4,math.sqrt(13),math.sqrt(2),-1]
        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = NormalMetrics(result)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i])

    def test_normal_second_case(self):
        expected_results = [-1, -1, math.sqrt(13), math.sqrt(13), math.sqrt(5), 1, 2, math.sqrt(5),
                            math.sqrt(5), -1, -1]
        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = NormalMetrics(result)
        self.assertEqual(len(expected_results), len(metrics.distances))
        for i in range(0, len(expected_results)):
            self.assertAlmostEqual(expected_results[i], metrics.distances[i])

    ###############################################VERTICAL TEST########################################################

    def test_vertical_case(self):
        expected_results = [3,3,2,3,4,3,4,2,3,2]
        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = VerticalMetrics(result)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i])

    def test_vertical_different_sizes(self):
        expected_results = [-1,-1,2,3,4,3,4,2,3,-1]
        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = VerticalMetrics(result)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i])

    def test_vertical_second_case(self):
        expected_results = [4,4,4,4,2,1,1,4,3,2,5]
        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = VerticalMetrics(result)
        self.assertEqual(len(expected_results), len(metrics.distances))
        for i in range(0, len(expected_results)):
            self.assertAlmostEqual(expected_results[i], metrics.distances[i])

if __name__ == '__main__':
    unittest.main()
import unittest
from Objects.ResultClass import ResultClass
from Metrics.nearest import NearestMetrics
from Metrics.normal import NormalMetrics
from Metrics.vertical import VerticalMetrics
import math

class TestMetrics(unittest.TestCase):

    data1 = {"lens": [(0,4),(1,4),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,4),(9,4)],
             "cornea": [(0,1),(1,1),(2,3),(3,2),(4,1),(5,2),(6,1),(7,3),(8,1),(9,2)]}
    data2 =  {"lens": [(0,4),(1,4),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,4),(9,4)],
              "cornea": [(2,3),(3,2),(4,1),(5,2),(6,1),(7,3),(8,1)]}
    data3 =  {"lens": [(0,7),(1,6),(2,6),(3,5),(4,3),(5,3),(6,3),(7,5),(8,6),(9,6),(10,7)],
              "cornea": [(0,3),(1,2),(2,2),(3,1),(4,1),(5,2),(6,2),(7,1),(8,3),(9,4),(10,2)]}

    ############################################NEAREST TEST#########################################################

    def test_nearest_normal_case(self):
        expected_results = [math.sqrt(5),math.sqrt(2),2,math.sqrt(5),math.sqrt(8),math.sqrt(8),math.sqrt(5),2,math.sqrt(2),2]
        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i]["dist"])

    def test_nearesst_different_sizes(self):
        expected_results = [math.sqrt(5),math.sqrt(2),2,math.sqrt(5),math.sqrt(8),math.sqrt(8),math.sqrt(5),2,math.sqrt(2),math.sqrt(5)]
        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i]["dist"])

    def test_nearest_second_case(self):
        expected_results = [4,math.sqrt(10),math.sqrt(13),math.sqrt(10),math.sqrt(2),1,1,math.sqrt(5),math.sqrt(5),
                            2,math.sqrt(10)]
        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)
        self.assertEqual(len(expected_results), len(metrics.distances))
        for i in range(0, len(expected_results)):
            self.assertAlmostEqual(expected_results[i], metrics.distances[i]["dist"])

    ###############################################NORMAL TEST########################################################

    def test_normal_normal_case(self):
        expected_results = [math.sqrt(2),math.sqrt(20),3,4,3,4,math.sqrt(13),math.sqrt(2)]
        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = NormalMetrics(result)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i]["dist"])

    def test_normal_different_sizes(self):
        expected_results = [-1,math.sqrt(20),3,4,3,4,math.sqrt(13),math.sqrt(2)]
        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = NormalMetrics(result)
        self.assertEqual(len(expected_results),len(metrics.distances))
        for i in range(0,len(expected_results)):
            self.assertAlmostEqual(expected_results[i],metrics.distances[i]["dist"])

    def test_normal_second_case(self):
        expected_results = [-1, math.sqrt(13), math.sqrt(13), math.sqrt(5), 1, math.sqrt(2), math.sqrt(5),
                            math.sqrt(5), math.sqrt(5), -1]
        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = NormalMetrics(result)
        self.assertEqual(len(expected_results), len(metrics.distances))
        for i in range(0, len(expected_results)):
            self.assertAlmostEqual(expected_results[i], metrics.distances[i]["dist"])

    ###############################################VERTICAL TEST########################################################



if __name__ == '__main__':
    unittest.main()
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

        expected_results_top2bot = [math.sqrt(5),math.sqrt(2),2,math.sqrt(5),math.sqrt(8),math.sqrt(8),math.sqrt(5),2,math.sqrt(2),2]
        expected_points_top2bot = [(2,3), (2,3), (2,3), (2,3), (2,3), (7,3), (7,3), (7,3), (7,3), (9,4)]
        expected_results_bot2top = [3, 3, math.sqrt(2), math.sqrt(8), 4, 3, math.sqrt(13), math.sqrt(2), 3, 2]
        expected_points_bot2top = [(0,2), (1,2), (1,2), (1,2), (4,1), (5,1), (8,2), (8,2), (8,2), (9,2)]

        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)


    def test_nearesst_different_sizes(self):

        expected_results_top2bot = [math.sqrt(5),math.sqrt(2),2,math.sqrt(5),math.sqrt(8),math.sqrt(8),math.sqrt(5),2,math.sqrt(2),math.sqrt(5)]
        expected_points_top2bot = [(2,3), (2,3), (2,3), (2,3), (2,3), (7,3), (7,3), (7,3), (7,3), (7,3)]
        expected_results_bot2top = [math.sqrt(2), math.sqrt(8), 4, 3, math.sqrt(13), math.sqrt(2), 3]
        expected_points_bot2top = [(1,2), (1,2), (4,1), (5,1), (8,2), (8,2), (8,2)]

        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)

    def test_nearest_second_case(self):

        expected_results_top2bot = [4,math.sqrt(10),math.sqrt(13),math.sqrt(10),math.sqrt(2),1,1,math.sqrt(5),math.sqrt(5),2,math.sqrt(10)]
        expected_points_top2bot = [(0,5),(0,5),(0,5),(2,6),(5,6),(5,6),(6,6),(8,5),(9,4),(9,4),(9,4)]
        expected_results_bot2top = [math.sqrt(10),math.sqrt(10),math.sqrt(5),math.sqrt(5),2,1,1,math.sqrt(5),2,2,math.sqrt(17)]
        expected_points_bot2top = [(1,2),(4,5),(4,5),(4,5),(4,5),(5,5),(6,5),(6,5),(6,5),(9,2),(6,5)]

        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = NearestMetrics(result,100,10,0.05)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)

    ###############################################NORMAL TEST########################################################

    def test_normal_normal_case(self):
        expected_results_top2bot = [3,math.sqrt(2),math.sqrt(20),3,4,3,4,math.sqrt(13),math.sqrt(2),2]
        expected_points_top2bot = [(0,5),(2,3),(4,5),(3,4),(4,5),(5,4),(6,5),(5,4),(7,3),(9,4)]
        expected_results_bot2top = [3,-1, math.sqrt(2),math.sqrt(18),4,3,math.sqrt(20),2,-1,math.sqrt(18)]
        expected_points_bot2top = [(0,2),None,(1,2),(6,1),(4,1),(5,1),(4,1),(7,1),None,(6,1)]

        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = NormalMetrics(result)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)

    def test_normal_different_sizes(self):

        expected_results_top2bot = [-1,-1,math.sqrt(20),3,4,3,4,math.sqrt(13),math.sqrt(2),-1]
        expected_points_top2bot = [None,None,(4,5),(3,4),(4,5),(5,4),(6,5),(5,4),(7,3),None]
        expected_results_bot2top = [math.sqrt(8),math.sqrt(18),4,3,math.sqrt(20),2,-1]
        expected_points_bot2top = [(4,1),(6,1),(4,1),(5,1),(4,1),(7,1),None]

        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = NormalMetrics(result)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)


    def test_normal_second_case(self):

        expected_results_top2bot = [-1, -1, math.sqrt(13), math.sqrt(13), math.sqrt(5), 1, 2, math.sqrt(5), math.sqrt(5), -1, -1]
        expected_points_top2bot = [None, None, (0,5),(0,5),(2,6),(5,6),(8,5),(8,5),(9,4),None, None]
        expected_results_bot2top = [math.sqrt(13),math.sqrt(13),math.sqrt(5),math.sqrt(5),math.sqrt(29),math.sqrt(2),1,math.sqrt(5),math.sqrt(5),-1,-1]
        expected_points_bot2top = [(3,3),(3,3),(4,5),(4,5),(2,2),(4,5),(6,5),(6,5),(7,3),None,None]

        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = NormalMetrics(result)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)

    ###############################################VERTICAL TEST########################################################

    def test_vertical_case(self):

        expected_results_top2bot = [3, 3, 2, 3, 4, 3, 4, 2, 3, 2]
        expected_results_bot2top = [3, 3, 2, 3, 4, 3, 4, 2, 3, 2]
        expected_points_top2bot = self.data1["cornea"]
        expected_points_bot2top = self.data1["lens"]

        result = ResultClass(self.data1["lens"], self.data1["cornea"], True)
        metrics = VerticalMetrics(result)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)

    def test_vertical_different_sizes(self):

        expected_results_top2bot = [-1,-1,2,3,4,3,4,2,3,-1]
        expected_results_bot2top = [2, 3, 4, 3, 4, 2, 3]
        expected_points_top2bot = [None, None, (2, 3), (3, 4), (4, 5), (5, 4), (6, 5), (7, 3), (8, 5), None]
        expected_points_bot2top = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 2)]

        result = ResultClass(self.data2["lens"], self.data2["cornea"], True)
        metrics = VerticalMetrics(result)

        self.check_metrics(metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot,
                           expected_points_bot2top)

    def test_vertical_second_case(self):

        expected_results_top2bot = [4,4,4,4,2,1,1,4,3,2,5]
        expected_results_bot2top = [4,4,4,4,2,1,1,4,3,2,5]
        expected_points_bot2top = self.data3["lens"]
        expected_points_top2bot = self.data3["cornea"]

        result = ResultClass(self.data3["lens"], self.data3["cornea"], True)
        metrics = VerticalMetrics(result)

        self.check_metrics(metrics,expected_results_top2bot,expected_results_bot2top,expected_points_top2bot,expected_points_bot2top)

    def check_metrics(self, metrics, expected_results_top2bot, expected_results_bot2top, expected_points_top2bot, expected_points_bot2top):
        # Top2bot
        self.assertEqual(len(expected_results_top2bot), len(metrics.top2bot["distances"]))
        self.assertEqual(len(metrics.top2bot["points"]), len(metrics.top2bot["line"]))
        self.assertEqual(len(metrics.top2bot["points"]), len(metrics.top2bot["distances"]))

        for i in range(0, len(expected_results_top2bot)):
            self.assertAlmostEqual(expected_results_top2bot[i], metrics.top2bot["distances"][i])
            self.assertEqual(expected_points_top2bot[i], metrics.top2bot["points"][i])

        # Bot2top
        self.assertEqual(len(expected_results_bot2top), len(metrics.bot2top["distances"]))
        self.assertEqual(len(metrics.bot2top["points"]), len(metrics.bot2top["line"]))
        self.assertEqual(len(metrics.bot2top["points"]), len(metrics.bot2top["distances"]))

        for i in range(0, len(expected_results_bot2top)):
            self.assertAlmostEqual(expected_results_bot2top[i], metrics.bot2top["distances"][i])
            self.assertEqual(expected_points_bot2top[i], metrics.bot2top["points"][i])

if __name__ == '__main__':
    unittest.main()
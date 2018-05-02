from Metrics.nearest import NearestMetrics
from Metrics.normal import NormalMetrics
from Metrics.vertical import VerticalMetrics
import time

NEAREST_WINDOW = 100
NEAREST_SECOND_WINDOW = 10
NEAREST_CHECK_RATE = 0.05

class MetricsClass(object):
    vertical = None
    normal = None
    nearest = None
    verbose = False

    def __init__(self, result, verbose):

        if verbose:
            start_time = time.time()
            self.verbose = verbose
            print("\tMétricas:")

        self.nearest = NearestMetrics(result,NEAREST_WINDOW,NEAREST_SECOND_WINDOW,NEAREST_CHECK_RATE)

        if verbose:
            nearest_time = time.time()
            print("\t\tNearest time: " + str(nearest_time-start_time) + "s")

        self.vertical = VerticalMetrics(result)

        if verbose:
            vertical_time = time.time()
            print("\t\tVertical time: " + str(vertical_time-nearest_time) + "s")

        self.normal = NormalMetrics(result)

        if verbose:
            normal_time = time.time()
            print("\t\tNormal time: " + str(normal_time-vertical_time) + "s")
            print("\t\tTotal time: " + str(normal_time-start_time) + "s")

    def show_distances(self, image):
        if self.verbose:
            start_time = time.time()
            print("\tMostrar métricas:")

        self.nearest.show(image)

        if self.verbose:
            nearest_time = time.time()
            print("\t\tNearest time: " + str(nearest_time-start_time) + "s")

        self.vertical.show(image)

        if self.verbose:
            vertical_time = time.time()
            print("\t\tVertical time: " + str(vertical_time-nearest_time) + "s")

        self.normal.show(image)

        if self.verbose:
            normal_time = time.time()
            print("\t\tNormal time: " + str(normal_time-vertical_time) + "s")
            print("\t\tTotal time: " + str(normal_time-start_time) + "s")


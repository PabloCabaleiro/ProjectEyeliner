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
    time = {"nearest":0,"vertical":0,"normal":0,"global":0}

    def get_time(self):
        return self.time

    def __init__(self, result, verbose = False):

        start_time = time.time()
        if verbose:
            self.verbose = verbose
            print("\tMétricas:")

        self.nearest = NearestMetrics(result,NEAREST_WINDOW,NEAREST_SECOND_WINDOW,NEAREST_CHECK_RATE)

        nearest_time = time.time()
        if verbose:
            print("\t\tNearest time: " + str(nearest_time-start_time) + "s")
        self.time["nearest"] = nearest_time-start_time

        self.vertical = VerticalMetrics(result)

        vertical_time = time.time()
        if verbose:
            print("\t\tVertical time: " + str(vertical_time-nearest_time) + "s")
        self.time["vertical"] = vertical_time-nearest_time

        self.normal = NormalMetrics(result)

        normal_time = time.time()
        if verbose:
            print("\t\tNormal time: " + str(normal_time-vertical_time) + "s")
            print("\t\tTotal time: " + str(normal_time-start_time) + "s")
        self.time["normal"] = normal_time-vertical_time
        self.time["global"] = normal_time-start_time

    def show_distances(self, image):
        if self.verbose:
            start_time = time.time()
            print("\tMostrar métricas:")

        self.vertical.show(image)

        if self.verbose:
            vertical_time = time.time()
            print("\t\tVertical time: " + str(vertical_time-start_time) + "s")

        self.normal.show(image)

        if self.verbose:
            normal_time = time.time()
            print("\t\tNormal time: " + str(normal_time-vertical_time) + "s")
            print("\t\tTotal time: " + str(normal_time-start_time) + "s")

        self.nearest.show(image)

        if self.verbose:
            nearest_time = time.time()
            print("\t\tNearest time: " + str(nearest_time-normal_time) + "s")


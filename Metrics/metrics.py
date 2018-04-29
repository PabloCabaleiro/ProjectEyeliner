from Metrics.nearest import NearestMetrics
from Metrics.normal import NormalMetrics
from Metrics.vertical import VerticalMetrics

NEAREST_WINDOW = 100
NEAREST_SECOND_WINDOW = 10
NEAREST_CHECK_RATE = 0.05

class MetricsClass(object):
    vertical = None
    normal = None
    nearest = None

    def __init__(self, result):
        self.nearest = NearestMetrics(result,NEAREST_WINDOW,NEAREST_SECOND_WINDOW,NEAREST_CHECK_RATE)
        self.vertical = VerticalMetrics(result)
        self.normal = NormalMetrics(result)

    def show_distances(self):
         


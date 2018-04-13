
class ResultMetrics(object):

    distances = None
    start_point = -1
    end_point = -1

    def __init__(self):
        self.distances = []

    def operate(self,result):
        self.start_point = max(result.lens_start_line, result.cornea_start_line)
        self.end_point = min(result.lens_end_line, result.cornea_end_line)
        self.distances = []
        for i in range(self.start_point, self.end_point):
            self.distances.append(result.cornea[i] - result.lens[i])


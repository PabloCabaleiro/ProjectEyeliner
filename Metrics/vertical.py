
class VerticalMetrics(object):

    distances = None

    def __init__(self, result):
        self.distances = []
        self.operate(result)

    def operate(self,result):
        for i in range(result.lens_start_line, result.lens_end_line + 1):
            if i >= result.cornea_start_line and i <= result.cornea_end_line:
                self.distances.append(result.get_lens_value(i) - result.get_cornea_value(i))
            else:
                self.distances.append(-1)


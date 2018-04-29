import matplotlib.pyplot as plt
from Utils import utils

class VerticalMetrics(object):

    bot2top = None
    top2bot = None

    def __init__(self, result):
        self.top2bot = None
        self.bot2top = None
        self.operate(result)

    def operate(self,result):
        self.operate_bot2top(result)
        self.operate_top2bot(result)

    def operate_top2bot(self,result):
        distances = []
        points = []
        for i in range(result.lens_start_line, result.lens_end_line + 1):
            if i >= result.cornea_start_line and i <= result.cornea_end_line:
                distances.append(result.get_cornea_value(i)-result.get_lens_value(i))
                points.append(result.get_cornea_point(i))
            else:
                distances.append(-1)
                points.append(None)
        self.top2bot = {"distances": distances, "points": points, "start": result.lens_start_line, "end": result.lens_end_line, "line": result.lens}

    def operate_bot2top(self,result):
        distances = []
        points = []
        for i in range(result.cornea_start_line, result.cornea_end_line + 1):
            if i >= result.lens_start_line and i <= result.lens_end_line:
                distances.append(result.get_cornea_value(i)-result.get_lens_value(i))
                points.append(result.get_lens_point(i))
            else:
                distances.append(-1)
                points.append(None)
        self.bot2top = {"distances": distances, "points": points, "start": result.cornea_start_line, "end": result.cornea_end_line, "line": result.cornea}


    def show(self, image):
        utils.show_metrics(self,image)
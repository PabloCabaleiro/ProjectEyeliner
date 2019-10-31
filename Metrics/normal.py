from Utils import utils

class NormalMetrics(object):

    bot2top = None
    top2bot = None
    WINDOW = 5

    def __init__(self, result):

        self.operate(result)

    def operate(self, result):
        self.bot2top_operate(result)
        self.top2bot_operate(result)

    def top2bot_operate(self,result):
        distances = []
        points = []

        for i in range(result.lens_start_line, result.lens_end_line):

            # Set as negative beacause top of image is 0 so the order in y axis changes
            if i < result.lens_start_line + self.WINDOW:
                try:
                    dy = (result.get_lens_value(i+self.WINDOW) - result.get_lens_value(result.lens_start_line)) * -1
                except:
                    continue
            elif i > result.lens_end_line-5:
                try:
                    dy = (result.get_lens_value(result.cornea_end_line) - result.get_lens_value(i-self.WINDOW)) * -1
                except:
                    continue
            else:
                # We want to set dx = 1 and we know its allways gonna be 2. So div dy for 2 to normalize.
                try:
                    dy = (result.get_lens_value(i + self.WINDOW) - result.get_lens_value(i - self.WINDOW)) / -2
                except:
                    continue

            finish = False
            cornea_values = [y for _,y in result.cornea]
            lens_point = result.get_lens_point(i)

            for j in range(int(min(cornea_values)),int(max(cornea_values))):
                pos = abs(lens_point[1] - j) * dy + lens_point[0]

                if pos < result.cornea_start_line or int(pos) >= result.cornea_end_line:
                    break

                pos = int(pos)

                cornea_point = result.get_cornea_point(pos)

                if cornea_point[1] <= j:
                    if (dy > 0 and (pos - 1) < result.cornea_start_line) or (dy <0 and (pos + 1) > result.cornea_end_line):
                        break
                    else:
                        #We got a result
                        distances.append(utils.get_dist(cornea_point,lens_point))
                        points.append(cornea_point)
                        finish = True
                        break
                elif pos < result.cornea_end_line and dy > 1 and result.get_cornea_value(pos+1) <= j:
                    point = result.get_cornea_point(pos+1)
                    distances.append(utils.get_dist(lens_point,point))
                    points.append(point)
                    finish = True
                    break
                elif pos > result.cornea_start_line and dy < -1 and result.get_cornea_value(pos-1) <= j:
                    point = result.get_cornea_point(pos - 1)
                    distances.append(utils.get_dist(lens_point, point))
                    points.append(point)
                    finish = True
                    break


            if not finish:
                distances.append(-1)
                points.append(None)

        self.top2bot = {"distances": distances, "points": points, "start": result.lens_start_line, "end": result.lens_end_line, "line": result.lens}

    def bot2top_operate(self, result):
        distances = []
        points = []

        for i in range(result.cornea_start_line, result.cornea_end_line):

            # Set as negative beacause top of image is 0 so the order in y axis changes
            if i < result.cornea_start_line + self.WINDOW:
                try:
                    dy = (result.get_cornea_value(i + self.WINDOW) - result.get_cornea_value(result.cornea_start_line))
                except:
                    continue
            elif i > result.cornea_end_line - self.WINDOW:
                try:
                    dy = (result.get_cornea_value(result.cornea_end_line) - result.get_cornea_value(i - self.WINDOW))
                except:
                    continue
            else:
                # We want to set dx = 1 and we know its allways gonna be 2. So div dy for 2 to normalize.
                try:
                    dy = (result.get_cornea_value(i + self.WINDOW) - result.get_cornea_value(i - self.WINDOW)) / 2
                except:
                    continue

            finish = False
            lens_values = [y for _, y in result.lens]
            max_lens_value = int(max(lens_values))
            min_lens_value = int(min(lens_values))
            cornea_point = result.get_cornea_point(i)

            for j in range(max_lens_value, min_lens_value - 1, -1):

                pos = abs(cornea_point[1] - j) * dy + cornea_point[0]

                if pos < result.lens_start_line or pos >= result.lens_end_line:
                    break

                pos = int(pos)

                lens_point = result.get_lens_point(pos)

                if lens_point[1] >= j:
                    if (dy > 0 and (pos - 1) < result.lens_start_line) or (
                            dy < 0 and (pos + 1) > result.lens_end_line):
                        break
                    else:
                        # We got a result
                        distances.append(utils.get_dist(cornea_point, lens_point))
                        points.append(lens_point)
                        finish = True
                        break
                elif pos < result.lens_end_line and dy > 1 and result.get_lens_value(pos + 1) >= j:
                    point = result.get_lens_point(pos + 1)
                    distances.append(utils.get_dist(cornea_point, point))
                    points.append(point)
                    finish = True
                    break
                elif pos > result.lens_start_line and dy < -1 and result.get_lens_value(pos - 1) >= j:
                    point = result.get_lens_point(pos - 1)
                    distances.append(utils.get_dist(cornea_point, point))
                    points.append(point)
                    finish = True
                    break

            if not finish:
                distances.append(-1)
                points.append(None)

        self.bot2top = {"distances": distances, "points": points, "start": result.cornea_start_line,
                        "end": result.cornea_end_line, "line": result.cornea}

    def show(self, img):
        utils.show_metrics(self, img, "Normal Metrics")






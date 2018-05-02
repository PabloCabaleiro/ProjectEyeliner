from Utils import utils

WINDOW_SEARCH = 100
SECOND_WINDOW_SEARCH = 10
CHECK_RATE = 0.05

class NearestMetrics(object):

    bot2top = None
    top2bot = None

    first_window = None     # Will look for first_window/2 previous and following points on the x axis
    second_window = None    # When we found the min on the first_window, will check one by one the second_window/2 previous and following points
    check_rate = None       # Check rate on the first window

    def __init__(self, result, first_window = 100, second_window = 10, check_rate = 0.05):
        self.first_window = first_window
        self.second_window = second_window
        self.check_rate = check_rate
        self.operate(result)

    def operate(self,result):
        self.top2bot_operate(result)
        self.bot2top_operate(result)

    def top2bot_operate(self,result):

        distances = []
        points = []

        step = int(WINDOW_SEARCH * CHECK_RATE)

        for lens_index in range(result.lens_start_line,result.lens_end_line+1):

            dist_min = {"dist": 10000, "cornea_pos": -1} #max int in pyrhon

            for cornea_index in range(max(result.cornea_start_line,lens_index - int(WINDOW_SEARCH/2)),
                                      min(result.cornea_end_line+1,lens_index + int(WINDOW_SEARCH/2)),
                                      step):

                try:
                    lens_point = result.get_lens_point(lens_index)
                    cornea_point = result.get_cornea_point(cornea_index)
                except:
                    continue

                distance = utils.get_dist(lens_point,cornea_point)

                if distance < dist_min["dist"]:
                    dist_min = {"dist": distance, "cornea_pos": cornea_index}

            for cornea_index in range(max(result.cornea_start_line,dist_min["cornea_pos"] - int(SECOND_WINDOW_SEARCH/2)),
                                      min(result.cornea_end_line+1,dist_min["cornea_pos"] + int(SECOND_WINDOW_SEARCH/2))):

                if cornea_index != dist_min["cornea_pos"]:

                    try:
                        lens_point = result.get_lens_point(lens_index)
                        cornea_point = result.get_cornea_point(cornea_index)
                    except:
                        continue

                    distance = utils.get_dist(lens_point, cornea_point)

                    if distance < dist_min["dist"]:
                        dist_min = {"dist": distance, "cornea_pos": cornea_index}

            if dist_min["cornea_pos"] == -1:
                distances.append(-1)
                points.append(None)
            else:
                distances.append(dist_min["dist"])
                points.append(result.get_cornea_point(dist_min["cornea_pos"]))

        self.top2bot = {"distances": distances, "points": points, "start": result.lens_start_line, "end": result.lens_end_line, "line": result.lens}

    def bot2top_operate(self, result):

        distances = []
        points = []

        step = int(WINDOW_SEARCH * CHECK_RATE)

        for cornea_index in range(result.cornea_start_line, result.cornea_end_line + 1):

            dist_min = {"dist": 10000, "lens_pos": -1}  # max int in pyrhon

            for lens_index in range(max(result.lens_start_line, cornea_index - int(WINDOW_SEARCH / 2)),
                                      min(result.lens_end_line + 1, cornea_index + int(WINDOW_SEARCH / 2)),
                                      step):

                try:
                    cornea_point = result.get_cornea_point(cornea_index)
                    lens_point = result.get_lens_point(lens_index)
                except:
                    continue

                distance = utils.get_dist(cornea_point, lens_point)

                if distance < dist_min["dist"]:
                    dist_min = {"dist": distance, "lens_pos": lens_index}

            for lens_index in range(
                    max(result.lens_start_line, dist_min["lens_pos"] - int(SECOND_WINDOW_SEARCH / 2)),
                    min(result.lens_end_line + 1, dist_min["lens_pos"] + int(SECOND_WINDOW_SEARCH / 2))):

                if lens_index != dist_min["lens_pos"]:

                    try:
                        cornea_point = result.get_cornea_point(cornea_index)
                        lens_point = result.get_lens_point(lens_index)
                    except:
                        continue

                    distance = utils.get_dist(cornea_point, lens_point)

                    if distance < dist_min["dist"]:
                        dist_min = {"dist": distance, "lens_pos": lens_index}



            if dist_min["lens_pos"] == -1:
                distances.append(-1)
                points.append(None)
            else:
                distances.append(dist_min["dist"])
                points.append(result.get_lens_point(dist_min["lens_pos"]))


        self.bot2top = {"distances": distances, "points": points, "start": result.cornea_start_line, "end": result.cornea_end_line, "line": result.cornea}

    def show(self, image):
        utils.show_metrics(self, image, "Nearest Metrics")
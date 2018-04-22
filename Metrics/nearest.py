from Utils import utils

WINDOW_SEARCH = 100
SECOND_WINDOW_SEARCH = 10
CHECK_RATE = 0.05

class NearestMetrics(object):

    start_point = -1
    end_point = -1
    distances = None

    first_window = None     # Will look for first_window/2 previous and following points on the x axis
    second_window = None    # When we found the min on the first_window, will check one by one the second_window/2 previous and following points
    check_rate = None       # Check rate on the first window

    def __init__(self, result, first_window = 100, second_window = 10, check_rate = 0.05):
        self.distances = []
        self.first_window = first_window
        self.second_window = second_window
        self.check_rate = check_rate
        self.operate(result)

    def operate(self,result):
        self.start_point = result.lens_start_line
        self.end_point = result.lens_end_line
        step = int(WINDOW_SEARCH * CHECK_RATE)

        for lens_index in range(result.lens_start_line,result.lens_end_line+1):

            dist_min = {"dist": 1000, "cornea_pos": -1} #max int in pyrhon

            for cornea_index in range(max(result.cornea_start_line,lens_index - int(WINDOW_SEARCH/2)),
                                      min(result.cornea_end_line+1,lens_index + int(WINDOW_SEARCH/2)),
                                      step):

                lens_point = result.get_lens_point(lens_index)
                cornea_point = result.get_cornea_point(cornea_index)
                distance = utils.get_dist(lens_point,cornea_point)

                if distance < dist_min["dist"]:
                    dist_min = {"dist": distance, "cornea_pos": cornea_index}

            for cornea_index in range(max(result.cornea_start_line,dist_min["cornea_pos"] - int(SECOND_WINDOW_SEARCH/2)),
                                      min(result.cornea_end_line+1,dist_min["cornea_pos"] + int(SECOND_WINDOW_SEARCH/2))):

                if cornea_index != dist_min["cornea_pos"]:

                    lens_point = result.get_lens_point(lens_index)
                    cornea_point = result.get_cornea_point(cornea_index)
                    distance = utils.get_dist(lens_point, cornea_point)

                    if distance < dist_min["dist"]:
                        dist_min = {"dist": distance, "cornea_pos": cornea_index}

            self.distances.append(dist_min)



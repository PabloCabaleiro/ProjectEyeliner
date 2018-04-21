from Utils import utils

WINDOW_SEARCH = 100
SECOND_WINDOW_SEARCH = 10
CHECK_RATE = 0.05

class NearestMetrics(object):

    start_point = -1
    end_point = -1
    distances = None

    def __init__(self):
        self.distances = []

    def operate(self,result):
        self.start_point = result.lens_start_line
        self.end_point = result.lens_end_line
        step = WINDOW_SEARCH * CHECK_RATE
        for lens_index in range(0,len(result.lens)):
            min = {"dist": 1000, "cornea_pos": cornea_index} #max int in pyrhon
            for cornea_index in range(max(0,lens_index - WINDOW_SEARCH/2),
                                      min(len(result.cornea),lens_index + WINDOW_SEARCH/2),
                                      step):
                aux = utils.get_dist((lens_index,result.get_lens_pos(lens_index)),
                                    (cornea_index,result.get_cornea_pos(cornea_index)))
                if aux < min.dist:
                    min = {"dist": aux, "cornea_pos": cornea_index}
            for cornea_index in range(max(0,min.cornea_pos - SECOND_WINDOW_SEARCH/2),
                                      min(len(result.cornea),min.cornea_pos + SECOND_WINDOW_SEARCH/2)):
                if cornea_index != min.cornea_pos:
                    aux = utils.get_dist((lens_index, result.get_lens_pos(lens_index)),
                                    (cornea_index, result.get_cornea_pos(cornea_index)))
                    if aux < min.dist:
                        min = {"dist": aux, "cornea_pos": cornea_index}

            self.distances.append(min.dist)



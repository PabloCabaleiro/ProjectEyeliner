from Utils import utils

class NormalMetrics(object):

    start_point = -1
    end_point = -1
    distances = None

    def __init__(self, result):
        self.distances = []
        self.operate(result)

    def operate(self,result):
        self.start_point = result.lens_start_line
        self.end_point = result.lens_end_line
        for i in range(1, len(result.lens)-1):
            # We want to set dy = 1 and we know its allways gonna be 2. So div for 2 to normalize.
            dx = (result.get_lens_value(i + 1) - result.get_lens_value(i - 1)) / 2
            x = i
            lens_y = result.get_lens_value(i)
            finish = False
            for y in range(lens_y,max(result.cornea)):
                cornea_y = result.get_cornea_value(round(x))
                if cornea_y <= y:
                    dist = utils.get_dist((round(x),cornea_y,(i,lens_y)))
                    self.distances.append(dist)
                    finish = True
                    break
                else:
                    x += dx

                if x < result.cornea_start_line or x > result.cornea_end_line:
                    self.distances.append(-1)
                    finish = True
                    break
            if not finish:
                raise("Something went wrong. Didnt find the cornea following the normal direction")



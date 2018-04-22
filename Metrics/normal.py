from Utils import utils

class NormalMetrics(object):
    distances = None

    def __init__(self, result):
        self.distances = []
        self.operate(result)

    def operate(self,result):

        for i in range(result.lens_start_line, result.lens_end_line+1):
            if i == result.lens_start_line:
                dy = result.get_lens_value(i+1) - result.get_lens_value(i)
            elif i == result.lens_end_line:
                dy = result.get_lens_value(i) - result.get_lens_value(i-1)
            else:
                # We want to set dy = 1 and we know its allways gonna be 2. So div for 2 to normalize.
                dy = (result.get_lens_value(i + 1) - result.get_lens_value(i - 1)) / 2

            finish = False
            cornea_values = [y for _,y in result.cornea]

            for j in range(min(cornea_values),max(cornea_values)+1):
                lens_point = result.get_lens_point(i)
                pos = round((j - lens_point[1]) * dy + i)

                if pos < result.cornea_start_line or pos > result.cornea_end_line:
                    break

                cornea_point = result.get_cornea_point(pos)

                if cornea_point[1] <= j:
                    #Tenemos resultado
                    self.distances.append(utils.get_dist(cornea_point,lens_point))
                    finish = True
                    break

            if not finish:
                self.distances.append(-1)




class ResultClass(object):

    lens = None
    lens_start_line = -1
    lens_end_line = -1
    cornea = None
    cornea_start_line = -1
    cornea_end_line = -1
    n_capas = -1

    def __init__(self, lens_line, cornea_line, n_capas):
        self.set_lens_line(lens_line)
        self.set_cornea_line(cornea_line)
        self.n_capas = n_capas

    def set_lens_line(self, lens_line):
        self.lens = lens_line
        self.lens_start_line = lens_line[0][0]
        self.lens_end_line = lens_line[-1][0]

    def get_lens_pos(self, i):
        if -1 < i - self.lens_start_line and i < self.lens_end_line:
            return self.lens[i - self.lens_start_line][1]
        else: return -1

    def get_cornea_pos(self, i):
        if -1 < i - self.cornea_start_line and i < self.cornea_end_line:
            return self.cornea[i - self.cornea_start_line][1]
        else: return -1

    def set_cornea_line(self, cornea_line):
        self.cornea = cornea_line
        self.cornea_start_line = cornea_line[0][0]
        self.cornea_end_line = cornea_line[-1][0]



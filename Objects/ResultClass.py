import matplotlib.pyplot as plt

class ResultClass(object):

    lens = None
    lens_start_line = -1
    lens_end_line = -1
    cornea = None
    cornea_start_line = -1
    cornea_end_line = -1
    has_lens = -1

    def __init__(self, lens_line, cornea_line, has_lens):
        if lens_line is not None and cornea_line is not None:
            self.set_lens_line(lens_line)
            self.set_cornea_line(cornea_line)
        self.has_lens = has_lens

    def set_lens_line(self, lens_line):
        self.lens = lens_line
        self.lens_start_line = int(round(lens_line[0][0]))
        self.lens_end_line = int(round(lens_line[-1][0]))

    def get_lens_pos(self, i):
        if -1 < i - self.lens_start_line and i < self.lens_end_line and i < len(self.lens):
            return self.lens[i - self.lens_start_line][1]
        else: return -1

    def get_cornea_pos(self, i):
        if -1 < i - self.cornea_start_line and i < self.cornea_end_line and i < len(self.cornea)-1:
            return self.cornea[i - self.cornea_start_line][1]
        else: return -1

    def set_cornea_line(self, cornea_line):
        self.cornea = cornea_line
        self.cornea_start_line = int(round(cornea_line[0][0]))
        self.cornea_end_line = int(round(cornea_line[-1][0]))

    def show(self, image):
        if self.has_lens:
            plt.figure("Result")
            top = list(zip(*self.lens))
            plt.plot(top[0],top[1])
            bot = list(zip(*self.cornea))
            plt.plot(bot[0],bot[1])
        else:
            plt.figure("Result has no lens")
        plt.imshow(image)
        plt.show()



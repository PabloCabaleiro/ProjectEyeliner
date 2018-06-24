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

    def get_lens_value(self, i):
        if i >= self.lens_start_line and i <= self.lens_end_line:
            return self.lens[i - self.lens_start_line][1]
        else:
            raise RuntimeError("Trying to access to a non valid position on lens array: " + str(i) + "on [" + str(self.lens_start_line) + "," + str(self.lens_end_line) + "]")

    def get_cornea_value(self, i):
        if i >= self.cornea_start_line and i <= self.cornea_end_line:
            return self.cornea[i - int(self.cornea_start_line)][1]
        else:
            raise RuntimeError("Trying to access to a non valid position on cornea array: " + str(i) + "on [" + str(self.cornea_start_line) + "," + str(self.cornea_end_line) + "]")

    def get_lens_point(self, i):
        if i >= self.lens_start_line and i <= self.lens_end_line:
            return self.lens[i - int(self.lens_start_line)]
        else:
            raise RuntimeError("Trying to access to a non valid position on lens array: " + str(i) + "on [" + str(self.lens_start_line) + "," + str(self.lens_end_line) + "]")

    def get_cornea_point(self, i):
        if i >= self.cornea_start_line and i < self.cornea_end_line:
            return self.cornea[i - self.cornea_start_line]
        else:
            raise RuntimeError("Trying to access to a non valid position on cornea array: " + str(i) + " on [" + str(self.cornea_start_line) + "," + str(self.cornea_end_line) + "]")

    def set_cornea_line(self, cornea_line):
        self.cornea = cornea_line
        self.cornea_start_line = int(round(cornea_line[0][0]))
        self.cornea_end_line = int(round(cornea_line[-1][0]))

    def show(self, image, name = "Result"):
        plt.figure(name)
        top = list(zip(*self.lens))
        plt.plot(top[0],top[1])
        bot = list(zip(*self.cornea))
        plt.plot(bot[0],bot[1])

        plt.imshow(image)
        plt.show()


